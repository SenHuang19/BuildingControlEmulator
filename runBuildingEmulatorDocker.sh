#!/bin/bash

docker run -it --rm -p="127.0.0.1:5000:5000" \
        --mount type=bind,source=${PWD}/emulatorExamples/,destination=/mnt/examples \
        --name=jmodelica_docker laurmarinovici/building_control_emulator:latest bash