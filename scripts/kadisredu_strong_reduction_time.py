#!/bin/env python

import pandas as pd
import json
import yaml
import argparse
from pathlib import Path
import random
import math

if __name__ == "__main__":
    cli = argparse.ArgumentParser(
            prog="",
            description="",
            add_help=True
            )

    cli.add_argument('-s', '--suite', help="Path to suite yaml")
    cli.add_argument('-f', '--file', help="Path to result csv")
    cli.add_argument('-o', '--output', metavar='output', default="", help='Output dir')

    args=cli.parse_args()
    output = Path(args.output)
    
    used_reducer = {
        "RGA" : "DisReduA",
        "RGS" : "DisReduS"
    }

    df = pd.read_csv(args.file, header=0)
    df = df[df["algo"].isin(used_reducer.keys())]

    suite_data = {}
    with open(args.suite, "r") as f:
        suite_data = yaml.safe_load(f)
    expected_number_of_runs = len(suite_data["seeds"]) if isinstance(suite_data["seeds"], list) else suite_data["seeds"]

    # compute comparison on the commonly solved set of graphs; others are logged
    counted_runs = df.groupby(['graph', 'algo', 'p']).size()
    print("Counted more or less runs for the following configs (the respective graphs are execluded from the further evaluation)", counted_runs[counted_runs != expected_number_of_runs].index)
    graphs_with_wrong_num_runs = counted_runs[counted_runs!=expected_number_of_runs].index.get_level_values("graph");
    df = df.loc[~df["graph"].isin(graphs_with_wrong_num_runs)]
    graph_was_not_always_solved = df["graph"].isin(df.loc[ df["t_reduce"].isna() | (df["failed"]==True), "graph"]) 
    print("The following configs failed for these graphs (the resepctive graphs are excluded from the further evaluation)", df.loc[graph_was_not_always_solved])
    df = df.loc[~graph_was_not_always_solved]
    # exclude graphs which were not solved by all algorithms
    n_algos = df["algo"].nunique()
    per_graph = df[["graph", "algo"]].drop_duplicates().groupby("graph")["algo"].nunique()
    keep_graphs = per_graph[per_graph == n_algos].index
    print("The following graphs were not solved by at least one algorithm. They are excluded from the remaining evaluation.\n", per_graph[per_graph != n_algos].index)
    df = df[df["graph"].isin(keep_graphs)]

    random.seed(0)
    def jitter(i):
        jitter_width=.75
        return random.uniform(i - (jitter_width / 2.0), i + (jitter_width / 2.0))


    cores = dict(zip(sorted(df["p"].unique()), range(len(df["p"].unique()))))

    df["jitter"] = df.apply(lambda row: jitter(cores[row["p"]]+1), axis=1)

    def shift_line(shift):
        return "\\pgfplotsset{cycle list shift = %s}\n" % shift

    for algorithm, a_df in df.groupby('algo'):
        pivot = pd.pivot_table(a_df, values=['t_reduce', 'jitter'], index=['graph', 'iteration', 'seed'], columns=['p'])
        pivot.columns = [f"{col}-jitter" if val=="jitter" else col for val, col in pivot.columns]
        table_path = output/(used_reducer[algorithm] + ".csv")
        pivot.to_csv(table_path, index=True, sep=" ")

        # write pgfplot
        plot_lines = []

        for core in cores:
            plot_lines.append("\\addplot+[myboxplot] table[y=%s]{%s};\n" % (core, table_path))

        num_cores = len(cores)
        plot_lines.append(shift_line(6-num_cores))

        for core in cores:
            plot_lines.append("\\addplot+[only marks] table[x={%s-jitter}, y=%s]{%s};\n" % (core, core, table_path))

        plot_lines.append(shift_line(6-num_cores))

        with open(output/(used_reducer[algorithm] + ".tex"), "w") as plot:
            plot.writelines(plot_lines)
