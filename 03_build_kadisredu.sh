#!/usr/bin/env sh

preset=$1

cd kadisredu
mkdir -p build

cmake --preset=$preset -S . -B build
cmake --build build --target kadisredu_app --parallel 
cd ..
