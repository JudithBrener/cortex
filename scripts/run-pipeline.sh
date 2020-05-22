#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    docker build --tag cortex_server_tag -f cortex/server/Dockerfile .

    docker network create cortex

    DATA_DIR=/tmp/cortex-data/
    mkdir -p $DATA_DIR

    docker run -d --rm --network=cortex --name mongodb -p 27017-27019:27017-27019 mongo:4.2.6
    docker run -d --rm --network=cortex --name cortex_rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    docker run -d --rm --network=cortex --name cortex_server -p 8000:8000 -v $DATA_DIR:$DATA_DIR cortex_server_tag
}

sh ./scripts/shutdown.sh
main "$@"