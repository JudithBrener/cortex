#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    python -m virtualenv .env --prompt "[thoughts-processor] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt

#   Generate protobuf sources:
    protoc -I=app/proto/ --python_out=app/proto/ app/proto/cortex.proto
}


main "$@"