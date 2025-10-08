#!/usr/bin/env sh

export PIPENV_PIPFILE=$(pwd)/../kaval/Pipfile
export BUILD_DIR=$(pwd)/../

mkdir -p experiment_out

pipenv install

(( cores=$(nproc)/2 )) # assumes nproc returns hyperthreads

pipenv run ../kaval/run-experiments.py 01_kadisredu_weak \
    --search-dirs ./suites \
    --machine shared \
    --max-cores $cores \
    --output-dir ./experiment_out/kadisredu_weak/output \
    --experiment-data-dir ./experiment_out/
