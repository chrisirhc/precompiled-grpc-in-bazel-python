# Using a precompiled gRPC plugin for Python in Bazel
This repository is an example of how to use a precompiled gRPC protobuf plugin for compiling Python gRPC stubs.

## Why do this?
* Avoid C++ compilation of dependencies
* See https://github.com/aspect-build/toolchains_protoc?tab=readme-ov-file#bazel-toolchain-for-pre-built-protoc

## Approach
* Use the compiled gRPC plugin that's included in grpcio-tools
