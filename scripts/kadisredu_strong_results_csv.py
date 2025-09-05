#!/bin/env python

import pandas as pd
import json
import yaml
import argparse
from pathlib import Path

from utils import extract_fields, extract_iteration_from_filename, extract_config_idx_from_filename

def extract_kadisredu_weak_results(exp_dir, suite):
    exp_dir = Path(exp_dir)
    suite_data = {}
    with open(suite, "r") as f:
        suite_data = yaml.safe_load(f)

    iterations = suite_data["seeds"]
    cores = suite_data["ncores"]
    time_limit = suite_data["time_limit"]

    configs = []
    with open(exp_dir / "config.json") as f:
        data = json.load(f)
        for i, cfg in enumerate(data):
            assert i == len(configs)
            configs.append(Path(cfg["config"]).name)


    rows = []

    files = (f for f in exp_dir.rglob("*") if f.is_file() and not f.name.endswith("log.txt") and f.name != "config.json")

    for file in files:
        print(file.name)
        with open(file, "r") as f:
            result_json = json.load(f)
        config = extract_config_idx_from_filename(file.name)
        iteration = extract_iteration_from_filename(file.name)
        print(config)
        rows.append({"algo": configs[config], "iteration": iteration} | extract_fields(result_json, time_limit, weak=False))

    df = pd.DataFrame(rows)
    df.set_index(['algo', 'p', 'graph', 'iteration'], inplace=True)
    return df


if __name__ == "__main__":
    cli = argparse.ArgumentParser(
            prog="",
            description="",
            add_help=True
            )

    cli.add_argument('-d', '--exp_dir', help="Dir. of the experiment results")
    cli.add_argument('-s', '--suite', help="Path to experiment suite")
    cli.add_argument('-o', '--output', metavar='output', default="", help='Output CSV')

    args=cli.parse_args()
    df = extract_kadisredu_strong_results(args.exp_dir, args.suite)
    df.to_csv(args.output, header=True)



    
    

