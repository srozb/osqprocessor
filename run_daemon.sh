#!/bin/bash

docker run \
  -t \
  -d \
  -v `pwd`/:/usr/src/app/osqprocessor \
  --name osqprocessor \
  --net host \
  srozb/osqprocessor

