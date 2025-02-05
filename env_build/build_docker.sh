#!/bin/bash

# ==========================================================================================
# Script Name  : build_docker.sh
# Description  : Dynamically replaces a placeholder SHA digest in a Dockerfile before build:
#                Predefined `image_digests.ini` file is used to select the correct digest sha:
#                `amd64` or `arm64` architectures:
#
# Usage        : ./build_docker.sh [ amd64 | arm64 ] 
# Example      : ./build_docker.sh amd64    # For Linux/AMD64 architecture
#                ./build_docker.sh arm64    # For macOS/ARM64 architecture
#
# Requirements : - `image_digests.ini` with architecture-specific SHA digests valuse:
#                - A Dockerfile with a `PLACEHOLDER_DIGEST` string to replace:
#
#       Notes  : - The original Dockerfile is restored post build complete: 
#                `sed` method is used to overwrite placeholders dynamically:
#
# Author      : Vlad Menshikov
# Created On  : 2025-01-20
# Version     : 1.0.0
# Contact     : dalvqsec@gmail.com
# ==========================================================================================


# ... color vars for output formatting:
gray='\033[1;90m'
white='\033[1;97m'
yellow='\033[1;93m'
magenta='\033[1;95m'
orange='\033[1;91m'
green='\033[1;92m'
cyan='\033[1;96m'
red="\033[1;31m"
off="\033[0m"

# ... decorators:
decorator_init="echo -e \n${gray}"$(printf '.%.0s' {1..72})"${off}"
decorator_done="echo -e \n\n${gray}"$(printf '=%.0s' {1..72})"${off}"


set -e  # ... sys exit if command exits with > 0 status:

#... repo build/infra paths:
ARCH=$1
INI_FILE="env_build/image_digests.ini"
DOCKERFILE="env_build/setup.Dockerfile"
PLACEHOLDER="PLACEHOLDER_DIGEST"

# ... check sys architecture args:
if [ -z "$1" ]; then
    echo -e "\n${green}$(basename $0)${off} script handles ${yellow}dynamic ${off}overwrites of a ${yellow}${PLACEHOLDER}${off} variable in ${cyan}${DOCKERFILE}${off}:"
    echo -e "${red}required ${magenta}argument: ${gray}--> ${cyan}amd64${off} for ${magenta}linux/amd64${off} architecture:\n${red}required ${magenta}argument: ${gray}--> ${cyan}arm64${off} for ${magenta}macOS/arm64${off} architecture:\n"
    echo -e "\t${magenta}linux ${yellow}call example: ${gray}--> ${green}$(basename $0) ${cyan}amd64${off}"
    echo -e "\t${magenta}macOS ${yellow}call example: ${gray}--> ${green}$(basename $0) ${cyan}arm64${off}"
    $decorator_done
    exit 1
fi


# ... [ image_digests.ini ] digest values read:
DIGEST=$(awk -F ' = ' "/$ARCH/ {print \$2}" "$INI_FILE")

# ... [ image_digests.ini ] digest content check:
if [ -z "$DIGEST" ]; then
    $decorator_init
    echo -e "\n${red}Error:${yellow} No ${off}digest found for architecture ${cyan}'$ARCH' ${off}in ${magenta}$INI_FILE${cyan}\n"
    cat $INI_FILE
    $decorator_done
    exit 1
fi

$decorator_init
echo -e "\n${green}Using Digest: ${magenta}$DIGEST ${off}for architecture ${cyan}$ARCH${off}"

# .... dynamic placeholder Dockerfile overwrite: 
cp "$DOCKERFILE" "$DOCKERFILE.bak"              # ... backup original Dockerfile:
sed -i.bak "s|FROM ubuntu@sha256:$PLACEHOLDER|FROM ubuntu@sha256:$DIGEST|g" "$DOCKERFILE"

# ... Dockerfile modifications check:
echo -e "\nDockerfile ${green}Updated${off}:"
grep "FROM ubuntu@sha256" "$DOCKERFILE"

# ... docker image build:
docker build -t paycheck:$ARCH --progress=plain --no-cache -f "$DOCKERFILE" .

# ... post build Dockerfile reset | restore to original instructions:
mv "$DOCKERFILE.bak" "$DOCKERFILE"
$decorator_done
echo -e "\nDockerfile ${green}restored to original state:${off}"
