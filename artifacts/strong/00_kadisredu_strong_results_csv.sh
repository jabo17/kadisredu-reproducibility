#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../../scripts/Pipfile

pipenv install

pipenv run python ../../scripts/kadisredu_strong_results_csv.py \
  --exp_dir ../../experiments/experiment_out/kadisredu_strong/output/ \
  --suite ../../experiments/suites/01_kadisredu_strong.suite.yaml \
  --output kadisredu_strong_results.csv
