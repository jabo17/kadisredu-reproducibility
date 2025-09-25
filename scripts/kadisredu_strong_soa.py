#!/bin/env python

from typing import MutableMapping
import pandas as pd
import json
import yaml
import argparse
from pathlib import Path
from scipy.stats import gmean


if __name__ == "__main__":
    cli = argparse.ArgumentParser(
            prog="",
            description="",
            add_help=True
            )

    cli.add_argument('--kadisredu', help="Path to result CSV of kadisredu")
    cli.add_argument('--htwis', help="Path to result CSV of HtWIS")
    cli.add_argument('--runs', type=int, help="Expected number of runs for each algorithm and graph")
    cli.add_argument('--timelimit', type=int, help="timelimit (seconds)")
    cli.add_argument('-o', '--output', metavar='output', default="", help='Output dir')

    args=cli.parse_args()
    output = Path(args.output)

    k_df = pd.read_csv(args.kadisredu, header=0) \
             .set_index(['algo', 'p', 'iteration', 'seed', 'graph'])
    h_df = pd.read_csv(args.htwis, header=0) \
             .set_index(['algo', 'p', 'iteration', 'seed', 'graph'])

    df = pd.concat([k_df[['solution_weight', 't', 'failed']], h_df[['solution_weight', 't', 'failed']]])

    # excluded graphs which where solved but an algo but at least one run result is missing
    counted_runs = df.reset_index().groupby(['graph', 'algo', 'p']).size()
    print("Counted more or less runs for the following configs (the respective graphs are execluded from the remaining evaluation)\n", counted_runs[counted_runs != args.runs].index)
    # exclude graphs with failed runs
    graphs_with_wrong_num_runs = counted_runs[counted_runs!=args.runs].index.get_level_values("graph");
    df = df.loc[~df.index.get_level_values("graph").isin(graphs_with_wrong_num_runs)]
    run_failed_for_graph = (df['solution_weight'].isna() |  df["t"].isna() | df["t"] > args.timelimit | df["failed"])
    graphs_with_failed_runs = df.index.get_level_values("graph")[run_failed_for_graph]
    print("The following configs failed for these graphs (the resepctive graphs are excluded from the remaining evaluation)\n", df.loc[run_failed_for_graph], df.loc[run_failed_for_graph].index.get_level_values("graph"))
    df = df.loc[~df.index.get_level_values("graph").isin(graphs_with_failed_runs)]
    # exclude graphs which were not solved by all algorithms
    n_algos = df.index.get_level_values("algo").nunique()
    h_df = df.reset_index()
    per_graph = h_df[["graph", "algo"]].drop_duplicates().groupby("graph")["algo"].nunique()
    keep_graphs = per_graph[per_graph == n_algos].index
    print("The following graphs were not solved by at least one algorithm. They are excluded from the remaining evaluation.\n", per_graph[per_graph != n_algos].index)
    df = df[df.index.get_level_values("graph").isin(keep_graphs)]


    # use arithmetic mean per instance
    mean_df = df.reset_index().groupby(['algo', 'p', 'graph']).agg({
            'solution_weight': 'mean',
            't': 'mean'
        })

    # use geometric mean over all instances
    print("Results:")
    # solution quality
    best_solution = df.groupby('graph').agg({'solution_weight':'max'})
    mean_df['solution_quality'] = mean_df.apply(lambda row: row['solution_weight']/best_solution.loc[row.name[2],'solution_weight'], axis=1)
    solution_quality = pd.pivot_table(mean_df, values='solution_quality', index='algo', columns='p', aggfunc=gmean)
    print("Solution Quality\n", solution_quality.round(4))
    solution_quality.to_csv(output/"solution_quality.csv", index=True, sep=" ")

    # running time (seconds)
    running_time_seconds = pd.pivot_table(mean_df, values='t', index='algo', columns='p', aggfunc=gmean)
    print("Running Time [s]\n", running_time_seconds.round(4))
    running_time_seconds.to_csv(output/"running_time_seconds.csv", index=True, sep=" ")

    # speedup over htwis
    mean_df['speed_up_htwis'] = mean_df.apply(lambda row: mean_df.loc[("htwis", 1, row.name[2]), 't']/row['t'], axis=1) 
    speedup_over_htwis = pd.pivot_table(mean_df, values='speed_up_htwis', index='algo', columns='p', aggfunc=gmean)
    print("Speedup over HtWIS\n", speedup_over_htwis.round(2))
    speedup_over_htwis.to_csv(output/"speed_up_over_htwis.csv", index=True, sep=" ")
