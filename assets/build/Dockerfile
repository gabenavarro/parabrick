FROM nvcr.io/nvidia/clara/clara-parabricks:4.5.1-1

# Install OS dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        curl \
        tar \
        git \
        make \
        gcc

# STAR for genome indexing
RUN wget -P /opt https://github.com/alexdobin/STAR/archive/2.7.1a.tar.gz && \
    tar -xzf /opt/2.7.1a.tar.gz -C /opt && \
    rm -rf /opt/2.7.1a.tar.gz

# Fastp for trimming
RUN wget -P /opt http://opengene.org/fastp/fastp && \
    chmod a+x /opt/fastp

# BWA for indexing
RUN git clone https://github.com/lh3/bwa.git /opt/bwa && \
    cd /opt/bwa && make

# Install python dependencies
RUN pip install --no-cache-dir \
    # For local development
    ipykernel \
    ruff \
    nbformat \
    ipywidgets \
    tqdm \
    pysam

# Docker NCCL configuration
ENV NCCL_SOCKET_IFNAME=^docker0,lo

# Set workdir
WORKDIR /workspace

# Healthcheck for GPUs
HEALTHCHECK --interval=30s --timeout=30s --retries=3 \
    CMD nvidia-smi || exit 1
