FROM rama43/mds-base:2026.1 AS builder

RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    tar \
    python3-pip \
    dssp \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN git clone https://github.com/marrink-lab/vermouth-martinize.git && \
    pip3 install --break-system-packages ./vermouth-martinize

RUN git clone https://github.com/marrink-lab/polyply_1.0.git && \
    pip3 install --break-system-packages ./polyply_1.0

RUN git clone https://github.com/Tsjerk/Insane.git /opt/insane

RUN martinize2 -h

COPY scripts/dssp2ss.py /usr/local/bin/dssp2ss

RUN chmod +x /usr/local/bin/dssp2ss

WORKDIR /workspace