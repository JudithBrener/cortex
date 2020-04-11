#!/bin/bash

inst=$(docker ps -a -q --filter "name=cortex_")

if [[ -n "${inst// }" ]]; then
  echo "Shutting down old instances..."
  docker kill $inst
  docker rm $inst
  docker network rm cortex
fi
