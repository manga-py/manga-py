#!/bin/bash

docker buildx build -t "mangadl/manga-py:latest" --platform linux/arm,linux/arm64,linux/amd64 . && docker buildx build -t "mangadl/manga-py:latest" --platform linux/arm,linux/arm64,linux/amd64 . --push
