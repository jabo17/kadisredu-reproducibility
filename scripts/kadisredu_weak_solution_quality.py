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
    output = Path(args.output)

    df = pd.read_csv(args.file, header=0)

    for p, p_df in df.groupby('p'):
        best = p_df.groupby('graph').agg({'solution_weight': 'max'})

        p_df['solution_quality'] = p_df.apply(lambda row: row['solution_weight']/best.loc[row['graph'],'solution_weight'].item(), axis=1)
        result = pd.pivot_table(p_df, values="solution_quality", index=['graph'], columns='algo', aggfunc=hmean)
        print("For %s cores: Solution Quality relative to best solution" % str(p))
        print(result)
        result.to_csv(output/(str(p) + ".csv"), index=True)
