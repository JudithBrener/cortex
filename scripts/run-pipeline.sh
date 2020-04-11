#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    docker build --tag cortex_server_tag -f cortex/server/Dockerfile .

    docker network create cortex

    DATA_DIR=/tmp/cortex-data/
    mkdir -p $DATA_DIR

    docker run -d --rm -v $DATA_DIR:$DATA_DIR --name cortex_server --network=cortex -p 8000:8000 cortex_server_tag
    docker run -d --rm --name cortex_rabbitmq --network=cortex -p 5672:5672 -p 15672:15672 rabbitmq:3-management
}

sh ./scripts/shutdown.sh
main "$@"