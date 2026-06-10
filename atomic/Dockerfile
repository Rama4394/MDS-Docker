FROM rama43/mds-base:2026.1 AS builder

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    bzip2

RUN wget -O /tmp/miniforge.sh \
    https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && \
    bash /tmp/miniforge.sh -b -p /opt/conda

ENV PATH=/opt/conda/bin:$PATH

RUN conda create -y -n atomic python=3.12

RUN conda create -y -n atomic \
    -c conda-forge \
    ambertools \
    pdbfixer \
    parmed \
    acpype \
    gmx_MMPBSA

FROM rama43/mds-base:2026.1

COPY --from=builder /opt/conda /opt/conda

ENV PATH=/opt/conda/bin:$PATH

RUN echo "source /opt/conda/etc/profile.d/conda.sh" \
    >> /etc/bash.bashrc

RUN echo "conda activate atomic" \
    >> /etc/bash.bashrc

WORKDIR /workspace