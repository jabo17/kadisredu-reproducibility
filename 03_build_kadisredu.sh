#!/usr/bin/env sh

cd kadisredu
mkdir -p build
cmake --preset=Release -S . -B build
cmake --build build --target kadisredu_app --parallel 
cd ..
