#!/usr/bin/env sh

git clone git@github.com:jabo17/distributed-kernelization.git kadisredu
cd kadisredu
git checkout improvement
git submodule update --init --recursive
cd ..

git clone https://github.com/mwis-abc/mwis-source-code.git htwis
patch -p1 -d htwis < htwis.patch
