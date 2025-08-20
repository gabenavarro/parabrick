FROM nvcr.io/nvidia/clara/clara-parabricks:4.5.1-1

# Install other dependencies
RUN pip install --no-cache-dir \
    # For local development
    ipykernel \
    ruff \
    nbformat \
    ipywidgets \
    tqdm

ENV NCCL_SOCKET_IFNAME=^docker0,lo

WORKDIR /workspace
# Healthcheck for GPUs
HEALTHCHECK --interval=30s --timeout=30s --retries=3 \
    CMD nvidia-smi || exit 1
