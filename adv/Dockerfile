# ==========================================
# STAGE 1: BUILDER
# Uses the heavy development image to compile
# ==========================================
FROM nvidia/cuda:12.8.1-devel-ubuntu24.04 AS builder

# Prevent tzdata and other packages from opening interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    build-essential \
    gcc \
    g++ \
    gfortran \
    make \
    cmake \
    pkg-config \
    openmpi-bin \
    libopenmpi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN git clone https://github.com/plumed/plumed2.git

WORKDIR /opt/plumed2

RUN ./configure \
    --prefix=/usr/local/plumed

RUN make -j$(nproc)

RUN make install && echo "INSTALL OK"

# Set environment paths for CMake and testing
ENV PATH=/usr/local/plumed/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/plumed/lib:$LD_LIBRARY_PATH
ENV PKG_CONFIG_PATH=/usr/local/plumed/lib/pkgconfig

RUN ldconfig

# Verify PLUMED
RUN plumed info --version

WORKDIR /opt

RUN wget https://ftp.gromacs.org/gromacs/gromacs-2025.2.tar.gz && \
    tar -xzf gromacs-2025.2.tar.gz

WORKDIR /opt/gromacs-2025.2

# Patch GROMACS with PLUMED non-interactively
RUN plumed patch -p -e gromacs-2025.2

RUN mkdir build
WORKDIR /opt/gromacs-2025.2/build

# Compile GROMACS with CUDA and MPI
RUN cmake .. \
    -DGMX_BUILD_OWN_FFTW=ON \
    -DGMX_MPI=ON \
    -DGMX_THREAD_MPI=OFF \
    -DGMX_GPU=CUDA \
    -DCMAKE_INSTALL_PREFIX=/usr/local/gromacs-plumed

RUN make -j$(nproc)
RUN make install

# Verify GROMACS (Note: MPI builds output 'gmx_mpi' instead of 'gmx')
RUN /usr/local/gromacs-plumed/bin/gmx_mpi --version

# ==========================================
# STAGE 2: PRODUCTION / RUNTIME
# Uses the slim runtime image to save space
# ==========================================
FROM nvidia/cuda:12.8.1-devel-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openmpi-bin \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 1. Copy the compiled files over FIRST
COPY --from=builder /usr/local/plumed /usr/local/plumed
COPY --from=builder /usr/local/gromacs-plumed /usr/local/gromacs-plumed

# 2. Create the symlink SECOND
RUN ln -s /usr/local/gromacs-plumed/bin/gmx_mpi /usr/local/gromacs-plumed/bin/gmx

# 3. Set your environment variables
ENV PATH=/usr/local/plumed/bin:/usr/local/gromacs-plumed/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/plumed/lib:/usr/local/gromacs-plumed/lib:$LD_LIBRARY_PATH

RUN echo 'export PATH=/usr/local/plumed/bin:/usr/local/gromacs-plumed/bin:$PATH' >> /etc/bash.bashrc && \
    echo 'export LD_LIBRARY_PATH=/usr/local/plumed/lib:/usr/local/gromacs-plumed/lib:$LD_LIBRARY_PATH' >> /etc/bash.bashrc

WORKDIR /workspace

CMD ["/bin/bash"]