#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../../scripts/Pipfile

pipenv install

mkdir -p reduction_impact
rm reduction_impact/* 2> /dev/null

pipenv run python ../../scripts/kadisredu_strong_reduction_impact.py \
  -f kadisredu_strong_results.csv \
  --suite ../../experiments/suites/00_kadisredu_strong.suite.yaml \
  --output reduction_impact

pdflatex reduction_impact.tex


