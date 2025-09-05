#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../kaval/Pipfile
export BUILD_DIR=$(pwd)/../

mkdir -p experiment_out

pipenv install

pipenv run ../kaval/run-experiments.py 00_kadisredu_strong \
    --search-dirs ./suites \
    --machine shared \
    --max-cores $(nproc) \
    --output-dir ./experiment_out/kadisredu_strong/output \
    --experiment-data-dir ./experiment_out/
