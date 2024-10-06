#!/bin/bash

cp -r ./models/* ../../common/src/models/
patch ../../common/src/tflite.cc < ./patches/tflite.cc.patch
patch ../../common/src/models/models.c < ./patches/models.c.patch
