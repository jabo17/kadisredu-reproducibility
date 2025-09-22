#!/usr/bin/env sh

git clone https://github.com/jabo17/kadisredu.git kadisredu
cd kadisredu
git checkout improvement
git submodule update --init --recursive
cd ..

git clone https://github.com/mwis-abc/mwis-source-code.git htwis
patch -p1 -d htwis < htwis.patch
