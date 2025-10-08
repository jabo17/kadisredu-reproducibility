#!/usr/bin/env sh

offline="FALSE"
if [ "$1" == "offline" ]; then
  offline="TRUE"
fi

cd kadisredu
mkdir -p build

cmake --preset=Release -S . -B build -DKADISREDU_BUILD_OFFLINE="${offline}"
cmake --build build --target kadisredu_app --parallel 
cd ..
