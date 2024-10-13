#!/bin/bash

source .bashrc
rm -r ../../common/src/models/anode
rm -r ../../common/src/models/mnist
cp -r ./models/* ../../common/src/models/
make renode
