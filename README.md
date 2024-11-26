# Using a precompiled gRPC plugin for Python in Bazel
This repository is an example of how to use a precompiled gRPC protobuf plugin for compiling Python gRPC stubs.

## Why do this?
* Faster builds
  * Avoid C++ compilation of dependencies when not editing any C++ files

| Typical compile (with C++ compilation) | Precompiled Binary |
| - | - |
| ![typical compilation](./docs/compile-with-cpp.svg) | ![compilation using precompiled binary](./docs/compile-with-precompiled-binary.svg)

* More reasons at: https://github.com/aspect-build/toolchains_protoc?tab=readme-ov-file#bazel-toolchain-for-pre-built-protoc

## Approach
* Use the compiled gRPC plugin that's built into the executable in grpcio-tools
* Follow the approach laid out in https://github.com/aspect-build/toolchains_protoc for setting up precompiled tooling for protoc.