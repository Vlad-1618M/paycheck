# Start with a base image to parse JSON
FROM ubuntu AS json_parser

# Set working directory
WORKDIR /paycheck

# Copy digest JSON file
COPY env_build/image_lock.json .

# Define an argument for architecture (must be provided at build time)
ARG ARCH

# Extract digest and pass it as a build argument
RUN jq -r ".manifests[\"${ARCH}\"][\"digest\"]" image_lock.json > digest_value.txt

# Read the digest value as a new argument (Docker can't use RUN-time variables in FROM)
ARG DIGEST
RUN export DIGEST=$(cat digest_value.txt) && echo "Using digest: $DIGEST"

# Manually set the FROM statement using the extracted digest value
FROM ubuntu@sha256:${DIGEST} AS deps

# Continue as usual
FROM deps AS dev

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /Vtools

# Ensure Python recognizes project paths
ENV PYTHONPATH="/Vtools/python:Vtools"

# Update, install required dependencies, and clean up in a single step
RUN apt update && \
    apt install -y --no-install-recommends \
    curl nano vim jq net-tools python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Ensure `python` and `pip` commands are available as expected (with condition to prevent errors)
RUN [ ! -e /usr/bin/python ] && ln -s /usr/bin/python3 /usr/bin/python || true && \
    [ ! -e /usr/bin/pip ] && ln -s /usr/bin/pip3 /usr/bin/pip || true

# Upgrade pip using apt instead of pip install
RUN apt update && apt install -y --no-install-recommends python3-pip

FROM dev AS prereqs

COPY . .

RUN ls -asl && \
    python -m pip install --break-system-packages -r deps/requirements.txt

# Default command (adjust as needed)
CMD ["/bin/bash"]
