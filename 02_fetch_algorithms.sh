#!/usr/bin/env sh

# The permanently archived code is available at https://doi.org/10.5281/zenodo.17174407
# The permanent release is shiped with all the git submodules and FetchContent dependencies.
git clone https://github.com/jabo17/kadisredu.git kadisredu
cd kadisredu
git submodule update --init --recursive
cd ..

git clone https://github.com/mwis-abc/mwis-source-code.git htwis
patch -p1 -d htwis < htwis.patch
