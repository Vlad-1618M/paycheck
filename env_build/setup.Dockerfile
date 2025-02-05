# Use a locked Ubuntu digest for immutability (ARM & AMD support)
ARG amd_64_version_lock="fad5ba7223f8d87179dfa23211d31845d47e07a474ac31ad5258afb606523c0d"
ARG arm_64_version_lock="133f2e05cb6958c3ce7ec870fd5a864558ba780fb7062315b51a23670bff7e76"

# Choose the correct architecture (modify based on target)
# FROM ubuntu@sha256:${amd_64_version_lock} AS deps
FROM ubuntu@sha256:${arm_64_version_lock} AS deps

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

# __________ leave it as optiuonal ??? _____________
# Create a non-root user (optional security step)
    # RUN useradd -m -s /bin/bash devuser
# Switch to non-root user
    # USER devuser
# __________________________________________________

# Default command (adjust as needed)
CMD ["/bin/bash"]
