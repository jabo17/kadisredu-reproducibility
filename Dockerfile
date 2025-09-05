# Based on Intel's intel/hpckit:devel-ubuntu22.04 container (https://hub.docker.com/r/intel/hpckit) and https://github.com/kamping-site/kamping-reproducibility/blob/main/Dockerfile
#
# Copyright (c) 2020-2021 Intel Corporation.
# SPDX-License-Identifier: BSD-3-Clause

FROM ubuntu:22.04
MAINTAINER Jannick Borowitz <jannick.borowitz@kit.edu>
RUN apt-get update && apt-get upgrade -y && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates gpg-agent software-properties-common && \
  rm -rf /var/lib/apt/lists/*
# repository to install Intel(R) oneAPI Libraries
RUN curl -fsSL https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2023.PUB | gpg --dearmor | tee /usr/share/keyrings/intel-oneapi-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/intel-oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main " > /etc/apt/sources.list.d/oneAPI.list

RUN apt-get update && apt-get upgrade -y && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates gpg-agent software-properties-common && \
  rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get upgrade -y && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates build-essential pkg-config gnupg libarchive13 openssh-server openssh-client wget net-tools \
    git \
    libsparsehash-dev \
    intel-oneapi-mpi intel-oneapi-mpi-devel intel-oneapi-tbb-devel && \
    #intel-oneapi-mpi-2021.11 intel-oneapi-mpi-devel-2021.11 intel-oneapi-tbb-devel-2021.4.0 && \
  rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV IMPI_VERSION=latest
ENV TBB_VERSION=latest
ENV CLASSPATH="/opt/intel/oneapi/mpi/${IMPI_VERSION}/share/java/mpi.jar"
ENV CMAKE_PREFIX_PATH="/opt/intel/oneapi/tbb/${TBB_VERSION}"
ENV CPATH="/opt/intel/oneapi/mpi/${IMPI_VERSION}/include"
ENV CPATH="/opt/intel/oneapi/tbb/${TBB_VERSION}/include:${CPATH}"
ENV FI_PROVIDER_PATH="/opt/intel/oneapi/mpi/${IMPI_VERSION}/opt/mpi/libfabric/lib/prov:/usr/lib/x86_64-linux-gnu/libfabric"
ENV I_MPI_ROOT="/opt/intel/oneapi/mpi/${IMPI_VERSION}"
ENV LD_LIBRARY_PATH="/opt/intel/oneapi/mpi/${IMPI_VERSION}/opt/mpi/libfabric/lib:/opt/intel/oneapi/mpi/${IMPI_VERSION}/lib"
ENV LD_LIBRARY_PATH="/opt/intel/oneapi/tbb/${TBB_VERSION}/lib:${LD_LIBRARY_PATH}"
ENV LIBRARY_PATH="/opt/intel/oneapi/mpi/${IMPI_VERSION}/lib"
ENV LIBRARY_PATH="/opt/intel/oneapi/tbb/${TBB_VERSION}/lib:${LIBRARY_PATH}"
ENV MANPATH="/opt/intel/oneapi/mpi/${IMPI_VERSION}/share/man"
ENV ONEAPI_ROOT="/opt/intel/oneapi"
ENV PATH="/opt/intel/oneapi/mpi/${IMPI_VERSION}/bin:${PATH}"
ENV PKG_CONFIG_PATH="/opt/intel/oneapi/mpi/${IMPI_VERSION}/lib/pkgconfig:"
ENV PKG_CONFIG_PATH="/opt/intel/oneapi/tbb/${TBB_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}"
ENV TBBROOT="/opt/intel/oneapi/tbb/${TBB_VERSION}"
ENV SETVARS_COMPLETED='1'

# KaDisRedu specific dependencies

# Install G++13
RUN apt update -y && apt install software-properties-common -y \
 && add-apt-repository ppa:ubuntu-toolchain-r/test -y \
 && apt update -y

RUN apt update -y && apt upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y gcc-13 g++-13

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100 \
 && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 100

# Install CMake
RUN wget https://cmake.org/files/v3.30/cmake-3.30.3-linux-x86_64.sh && \
    sh cmake-3.30.3-linux-x86_64.sh --skip-license --prefix=/usr/local

# Install pyenv
RUN apt update -y && apt upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y pip && \
    pip install pipenv

# Install dependencies for evaluation
ENV TZ="Europe/Berlin"
RUN apt update -y && apt upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y cloc gawk r-base texlive texlive-pictures jq && \
    R -e "install.packages(c('plyr', 'dplyr'))"

# Install some editors to make things simpler
RUN apt update -y && apt upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y vim nano tmux

# create a user `kadisredu`
ARG USERNAME=kadisredu
ARG USER_ID=1000
ARG USER_GID=$USER_ID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_ID --gid $USER_ID -m $USERNAME \
    && apt update \
    && apt install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /home/$USERNAME

VOLUME /repro-scripts
