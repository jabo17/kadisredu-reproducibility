#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../../scripts/Pipfile

pipenv install

mkdir -p throughput
rm throughput/* 2> /dev/null

pipenv run python ../../scripts/kadisredu_weak_throughput_csv.py \
  -f kadisredu_weak_results.csv \
  --suite ../../experiments/suites/01_kadisredu_weak.suite.yaml \
  --output throughput

pdflatex throughput.tex
rm throughput.aux throughput.fdb_latexmk throughput.fls throughput.log
