#!/bin/env python

import pandas as pd
import json
import yaml
import argparse
from pathlib import Path
from scipy.stats import hmean

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

    df = pd.read_csv(args.file, header=0)
    # throughput: edges per second
    df['throughput'] = df['edges'] / df['t']
    
    output = Path(args.output)

    for graph, graph_df in df.groupby('graph'):
        print(graph)
        pd.pivot_table(graph_df, values='throughput', index=['p'], columns='algo', aggfunc=hmean) \
                .to_csv(output/(graph + '.csv'), index=True, sep=" ")

