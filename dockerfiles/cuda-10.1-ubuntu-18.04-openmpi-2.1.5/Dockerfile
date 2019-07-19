# Cuda 10.1 + Ubuntu 18.04 + OpenMPI 2.1.5
# Contents:
#     Ubuntu 18.04
#     CUDA version 10.1
#     GNU compilers (upstream)
#     OFED (upstream)
#     OpenMPI version 2.1.5

FROM nvidia/cuda:10.1-devel-ubuntu18.04 AS devel

# Python
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python \
        python-dev \
        python3 \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# GNU compiler
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        g++ \
        gcc && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        fftw3 \
        git \
        python-pip \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# OFED
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        dapl2-utils \
        ibutils \
        ibverbs-utils \
        infiniband-diags \
        libdapl-dev \
        libibmad-dev \
        libibmad5 \
        libibverbs-dev \
        libibverbs1 \
        librdmacm-dev \
        librdmacm1 \
        opensm \
        rdmacm-utils && \
    rm -rf /var/lib/apt/lists/*

# OpenMPI version 2.1.5
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bzip2 \
        file \
        hwloc \
        libnuma-dev \
        make \
        openssh-client \
        perl \
        tar \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.5.tar.bz2 && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/openmpi-2.1.5.tar.bz2 -C /var/tmp -j && \
    cd /var/tmp/openmpi-2.1.5 &&  CC=gcc CXX=g++ ./configure --prefix=/opt/openmpi --enable-mpi-cxx --with-cuda --with-verbs && \
    make -j$(nproc) && \
    make -j$(nproc) install && \
    rm -rf /var/tmp/openmpi-2.1.5.tar.bz2 /var/tmp/openmpi-2.1.5
ENV LD_LIBRARY_PATH=/opt/openmpi/lib:$LD_LIBRARY_PATH \
    PATH=/opt/openmpi/bin:$PATH

RUN pip3 install setuptools && \
    pip3 install wheel && \
    pip3 install cmake && \
    pip3 install cython && \
    pip3 install numpy && \
    pip3 install mpi4py && \
    pip3 install networkx

LABEL Base for gmxapi on Rivanna=0.0.7

WORKDIR /scratch


