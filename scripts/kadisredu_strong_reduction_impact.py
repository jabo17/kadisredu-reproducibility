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

    # filter out graphs that were not always solved
    suite_data = {}
    with open(args.suite, "r") as f:
        suite_data = yaml.safe_load(f)
    expected_number_of_runs = len(suite_data["seeds"]) if isinstance(suite_data["seeds"], list) else suite_data["seeds"]

    df = pd.read_csv(args.file, header=0)
    df = df[df["algo"].isin(used_reducer.keys())]

    # compute comparison on the commonly solved set of graphs; others are logged
    counted_runs = df.groupby(['graph', 'algo', 'p']).size()
    print("Counted more or less runs for the following configs (the respective graphs are execluded from the further evaluation)", counted_runs[counted_runs != expected_number_of_runs].index)
    graphs_with_wrong_num_runs = counted_runs[counted_runs!=expected_number_of_runs].index.get_level_values("graph");
    df = df.loc[~df["graph"].isin(graphs_with_wrong_num_runs)]
    graph_was_not_always_solved = df["graph"].isin(df.loc[ df["rel_kernel_nodes"].isna() | (df["failed"]==True), "graph"]) 
    print("The following configs failed for these graphs (the resepctive graphs are excluded from the further evaluation)", df.loc[graph_was_not_always_solved])
    df = df.loc[~graph_was_not_always_solved]

    # compute reduction ratios
    df.set_index(['algo', 'p', 'iteration', 'seed', 'graph'], inplace=True)

    df["rel_reduction_ratio_nodes"] = df.apply(lambda row: (row['kernel_nodes']-df.loc[(row.name[0], 1, row.name[2], row.name[3], row.name[4]), 'kernel_nodes']) / row['nodes'], axis =1)
    
    df["rel_reduction_ratio_edges"] = df.apply(lambda row: (row['kernel_edges']-df.loc[(row.name[0], 1, row.name[2], row.name[3], row.name[4]), 'kernel_edges']) / row['edges'], axis =1)

    random.seed(0)
    def jitter(i):
        jitter_width=.75
        return random.uniform(i - (jitter_width / 2.0), i + (jitter_width / 2.0))

    cores = dict(zip(sorted(df.index.get_level_values("p").unique()), range(len(df.index.get_level_values("p").unique()))))
    df["jitter-rel_kernel"] = df.apply(lambda row: jitter(cores[row.name[1]]+1), axis=1)
    df["jitter-rel_reduction_ratio"] = df.apply(lambda row: jitter(cores[row.name[1]]), axis=1)

    metrics = {(a, b) for a in {"rel_kernel", "rel_reduction_ratio"} for b in {"nodes", "edges"}}

    def shift_line(shift):
        return "\\pgfplotsset{cycle list shift = %s}\n" % shift

    for algorithm, a_df in df.groupby('algo'):
        for a,b in metrics:
            metric = a + "_" + b
            print(a_df)
            pivot = pd.pivot_table(a_df, values=[metric, 'jitter-'+a], index=['graph', 'iteration', 'seed'], columns='p')
            pivot.columns = [f"{col}-jitter" if val=="jitter-"+a else col for val, col in pivot.columns]
            table_path = output/(metric + "_" + used_reducer[algorithm] + ".csv")
            pivot.to_csv(table_path, index=True, sep=" ")

            # write pgfplot
            plot_lines = []

            if a == "kernel_edges":
                plot_lines.append(shift_line(1))
            for core in cores:
                if core > 1 or a == "rel_kernel":
                    plot_lines.append("\\addplot+[myboxplot] table[y=%s]{%s};\n" % (core, table_path))

            num_cores = len(cores) if a == "rel_kernel" else len(cores)-1 # do not plot relative reduction ratios for p=1
            plot_lines.append(shift_line(6-num_cores))

            if a == "kernel_edges":
                plot_lines.append(shift_line(1))
            for core in cores:
                if core > 1 or a == "rel_kernel":
                    plot_lines.append("\\addplot+[only marks] table[x={%s-jitter}, y=%s]{%s};\n" % (core, core, table_path))


            plot_lines.append(shift_line(6-num_cores))

            with open(output/(metric + "_" + used_reducer[algorithm] + ".tex"), "w") as plot:
                plot.writelines(plot_lines)
