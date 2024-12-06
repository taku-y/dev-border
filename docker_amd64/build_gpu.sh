#!/bin/bash
docker build \
    --build-arg BASE_IMAGE=nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 \
    --build-arg TORCH_URLhttps://download.pytorch.org/whl/test/cu118 \
    -t border .
