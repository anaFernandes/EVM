#!/bin/bash
DIR=$(pwd)

docker build -t evm:latest $DIR
docker run --link mysql:db -ti --rm -v $DIR/../app:/home/evm/app evm
