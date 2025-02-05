#!/bin/bash
img=paycheck
DIGEST=$(jq -r '.ubuntu_digest' version-lock.json)
docker build --build-arg version_lock="$DIGEST" -t ${img} .


