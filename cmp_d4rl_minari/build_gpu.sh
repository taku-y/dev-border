#!/bin/bash
docker build \
    --build-arg BASE_IMAGE=nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 \
    --build-arg TORCH_URL=https://download.pytorch.org/whl/cu113 \
    -t learn_corl .
