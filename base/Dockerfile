FROM nvidia/cuda:12.8.1-devel-ubuntu24.04 AS builder

LABEL maintainer="Ramaraj K"
LABEL image="rama43/MDS-base"
LABEL version="2026.1"
LABEL description="GPU-enabled Molecular Dynamics base platform with GROMACS and analysis tools"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
	openmpi-bin \
    libfftw3-dev \
    python3 \
    python3-pip \
	cmake \
    git \
    wget \
    curl \
    vim \
    nano \
    tree \
    htop \
    rsync \
    zip \
    unzip \
    tar \
    less \
	openmpi-bin \
    libopenmpi-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN wget https://ftp.gromacs.org/gromacs/gromacs-2025.2.tar.gz

RUN tar -xzf gromacs-2025.2.tar.gz

WORKDIR /opt/gromacs-2025.2

RUN mkdir build

WORKDIR /opt/gromacs-2025.2/build

RUN cmake .. \
    -DGMX_BUILD_OWN_FFTW=ON \
    -DGMX_MPI=ON \
    -DGMX_GPU=CUDA \
    -DCMAKE_INSTALL_PREFIX=/usr/local/gromacs

RUN make -j$(nproc)

RUN make install

FROM nvidia/cuda:12.8.1-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openmpi-bin \
    libfftw3-dev \
    python3 \
    python3-pip

COPY --from=builder \
    /usr/local/gromacs \
    /usr/local/gromacs

ENV PATH="/usr/local/gromacs/bin:${PATH}"

RUN ln -s \
/usr/local/gromacs/bin/gmx_mpi \
/usr/local/gromacs/bin/gmx

RUN pip3 install --break-system-packages \
    numpy \
    scipy \
    pandas \
    matplotlib \
    seaborn \
    plotly \
    biopython \
    MDAnalysis \
    mdtraj \
    scikit-learn \
    tqdm \
    jupyterlab \
    nglview \
    ipywidgets \
    py3Dmol

RUN pip3 install --break-system-packages seaborn

EXPOSE 8888

RUN mkdir -p \
    /workspace \
    /examples \
    /scripts \
    /data
	
WORKDIR /workspace

RUN gmx --version

CMD ["/bin/bash"]