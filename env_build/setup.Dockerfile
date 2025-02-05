# ... placeholder line will be overwritten by [ cicd-build.yml ] using correct SHA digest values:
FROM ubuntu@sha256:PLACEHOLDER_DIGEST AS deps

FROM deps AS dev

# ... set environment variables | helps to reduce interactive prompts:
ENV DEBIAN_FRONTEND=noninteractive

# ... work dir path:
WORKDIR /paycheck

# ... Python sys.path() setup:
ENV PYTHONPATH="/paycheck/python:paycheck"

# ... deps check | update, install | clean up:
RUN apt update && \
    apt install -y --no-install-recommends \
    vim jq tree python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# ... `python` & `pip` syms: 
RUN [ ! -e /usr/bin/python ] && ln -s /usr/bin/python3 /usr/bin/python || true && \
    [ ! -e /usr/bin/pip ] && ln -s /usr/bin/pip3 /usr/bin/pip || true

# ... pip upgrade | apt is used instead of pip install dye to debian conditions: 
RUN apt update && apt install -y --no-install-recommends python3-pip

FROM dev AS prereqs

COPY . .

RUN ls -asl && \
    python -m pip install --break-system-packages -r deps/requirements.txt

FROM prereqs AS test

RUN pytest --cache-clear -v -r charts tests/test_paycheck.py

# ... default entrypoint:
CMD ["/bin/bash"]

