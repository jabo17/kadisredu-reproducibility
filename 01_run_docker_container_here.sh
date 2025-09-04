#!/usr/bin/env sh

# Run the docker container
# NOTE: if you do not have write access while running the docker contaienr to to $(pwd),
# pass -u '${UID}:${GID}' in addition
docker run -it --rm -v $(pwd):/home/kadisredu --shm-size=4gb ghcr.io/jabo17/kadisredu-reproducibility:main
