Using a precompiled gRPC plugin for Python in Bazel

## Why do this?
* Avoid C++ compilation of dependencies
* See https://github.com/aspect-build/toolchains_protoc?tab=readme-ov-file#bazel-toolchain-for-pre-built-protoc

## How?
* Use the compiled gRPC plugin that's included in grpcio-tools