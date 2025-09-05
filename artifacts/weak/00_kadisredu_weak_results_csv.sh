#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../../scripts/Pipfile

pipenv install

pipenv run python ../../scripts/kadisredu_weak_results_csv.py \
  --exp_dir ../../experiments/experiment_out/kadisredu_weak/output/ \
  --suite ../../experiments/suites/01_kadisredu_weak.suite.yaml \
  --output kadisredu_weak_results.csv
