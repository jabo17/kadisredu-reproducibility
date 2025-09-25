#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../../scripts/Pipfile

pipenv install

mkdir -p soa
rm soa/* 2> /dev/null

pipenv run python ../../scripts/kadisredu_strong_soa.py \
  --kadisredu kadisredu_strong_results.csv \
  --htwis htwis_results.csv \
  --output soa \
  --timelimit 7200 \
  --runs 4 # change this if the number of iterations is changed in the suites
