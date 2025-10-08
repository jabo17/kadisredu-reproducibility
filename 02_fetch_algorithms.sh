#!/usr/bin/env sh

# The permanently archived code is available at https://zenodo.org/records/17174408
git clone https://github.com/jabo17/kadisredu.git kadisredu
cd kadisredu
git submodule update --init --recursive
cd ..

git clone https://github.com/mwis-abc/mwis-source-code.git htwis
patch -p1 -d htwis < htwis.patch
