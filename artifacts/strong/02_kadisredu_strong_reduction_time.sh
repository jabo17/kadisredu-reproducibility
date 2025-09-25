#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../../scripts/Pipfile

pipenv install

mkdir -p reduction_time
rm reduction_time/* 2> /dev/null

pipenv run python ../../scripts/kadisredu_strong_reduction_time.py \
  -f kadisredu_strong_results.csv \
  --suite ../../experiments/suites/00_kadisredu_strong.suite.yaml \
  --output reduction_time

pdflatex reduction_time.tex > /dev/null
