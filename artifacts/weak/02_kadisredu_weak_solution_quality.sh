#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../../scripts/Pipfile

pipenv install

mkdir -p solution_quality
rm solution_quality/* 2> /dev/null

pipenv run python ../../scripts/kadisredu_weak_solution_quality.py \
  -f kadisredu_weak_results.csv \
  --suite ../../experiments/suites/01_kadisredu_weak.suite.yaml \
  --output solution_quality

