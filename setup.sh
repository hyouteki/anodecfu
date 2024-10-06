#!/bin/bash

cp -r ./models/* ../../common/src/models/
patch ../../common/src/tflite.cc < ./patches/tflite.cc.patch
patch ../../common/src/models/models.c < ./patches/models.c.patch

python3 -m venv venv

mkdir -p ./third_party
wget -P ./third_party/ https://static.dev.sifive.com/dev-tools/freedom-tools/v2020.08/riscv64-unknown-elf-gcc-10.1.0-2020.08.2-x86_64-linux-ubuntu14.tar.gz
tar xvfz ./third_party/riscv64-unknown-elf-gcc-10.1.0-2020.08.2-x86_64-linux-ubuntu14.tar.gz -C ./third_party
