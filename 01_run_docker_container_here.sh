#!/usr/bin/env sh

docker run -it --rm -v $(pwd):/home/kadisredu --shm-size=4gb ghcr.io/jabo17/kadisredu-reproducibility:main
