# Development Guide

This guide provides instructions for developers and agents working with this repository.

## Project Overview

This repository demonstrates how to use a precompiled gRPC protobuf plugin for compiling Python gRPC stubs in Bazel, providing significantly faster cold start builds (~29X speed-up) by avoiding C++ compilation of dependencies.

## Prerequisites

- **Bazel**: Version 8.5.1 or later (specified in `.bazelversion`)
- **Python**: Version 3.11 (managed by rules_python)
- **Operating System**: Linux, macOS, or Windows (with appropriate tooling)

## Quick Start with Dev Container (Recommended)

The easiest way to get started is using the provided [Dev Container](https://containers.dev/):

1. **Prerequisites**: Install [Docker](https://www.docker.com/products/docker-desktop) and [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Open in Container**: 
   - Open this repository in VS Code
   - Press `F1` and select "Dev Containers: Reopen in Container"
   - Wait for the container to build and configure (first time only)

3. **Start Developing**: Everything is pre-configured! Run:
   ```bash
   bazel build //...
   ```

The dev container includes:
- ✅ Bazel (via bazelisk, automatically uses the correct Bazel version)
- ✅ Python 3.11
- ✅ Persistent Bazel cache for faster rebuilds

## Manual Setup

If you prefer not to use the dev container, follow these steps:

### 1. Install Bazel

The project requires Bazel 8.5.1 or later. The recommended way to install Bazel is using [Bazelisk](https://github.com/bazelbuild/bazelisk), which automatically downloads and uses the correct version specified in `.bazelversion`.

**Install Bazelisk:**
```bash
# macOS (using Homebrew)
brew install bazelisk

# Linux (download binary)
wget https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-amd64
chmod +x bazelisk-linux-amd64
sudo mv bazelisk-linux-amd64 /usr/local/bin/bazel

# Windows (using Chocolatey)
choco install bazelisk
```

### 2. Verify Setup

```bash
# Check Bazel version
bazel version

# Verify MODULE.bazel is valid
bazel mod graph
```

## Building

### Build All Targets

```bash
bazel build //...
```

### Build Specific Targets

```bash
# Build the "thing" Python gRPC stubs
bazel build //:thing_python_grpc

# Build the "greeter" Python gRPC stubs
bazel build //:greeter_python_grpc
```

## Testing

```bash
# Run all tests
bazel test //...

# Run tests with verbose output
bazel test --test_output=all //...
```

## Code Formatting and Linting

This project uses `aspect_rules_lint` and `buildifier_prebuilt` for BUILD file formatting and linting.

### Quick Commands

```bash
# Format and fix lint issues in all BUILD/Starlark files
bazel run //tools/format:buildifier

# Check formatting and lint without making changes (used in CI)
bazel run //tools/format:buildifier.check
```

### Alternative Format Commands

The following targets use `format_multirun` for broader formatting support:

```bash
# Format all BUILD files
bazel run //tools/format:format

# Check formatting without making changes
bazel run //tools/format:format.check
```

### About Buildifier

[Buildifier](https://github.com/bazelbuild/buildtools/tree/master/buildifier) is the standard formatter and linter for Bazel BUILD and `.bzl` files. It enforces consistent style and catches common issues like:

- Unused load statements
- Undocumented public functions
- Deprecated function usage
- Incorrect package ordering

## Dependency Management

### Python Dependencies

Python dependencies are managed using `rules_uv` and locked in `tools/requirements.txt`.

**Update Python dependencies:**

1. Edit `tools/requirements.in` to add/modify dependencies
2. Run the lock file generator:
   ```bash
   bazel run @@//tools:generate_requirements_txt
   ```
3. Commit the updated `tools/requirements.txt`

**Current Python dependencies:**
- `grpcio==1.68.0`
- `grpcio-tools==1.68.0` (provides the precompiled gRPC plugin)
- `protobuf==5.28.3`

### Bazel Module Dependencies

Bazel dependencies are managed in `MODULE.bazel` using Bzlmod (Bazel's modern dependency system).

**Key dependencies:**
- `rules_proto` (v7.0.2) - Protocol buffer compilation rules
- `rules_proto_grpc` (v5.0.1) - gRPC support
- `rules_python` (v0.40.0) - Python toolchain and rules
- `grpc` (v1.65.0) - gRPC framework

## Project Structure

```
.
├── .bazelversion           # Locks Bazel version to 8.5.1
├── .bazelrc                # Bazel configuration flags
├── MODULE.bazel            # Bazel module dependencies (Bzlmod)
├── BUILD.bazel             # Root build file with gRPC compilation targets
├── modules/                # Local Bazel modules
│   └── example_protos/     # Example protocol buffer definitions
├── thirdparty/             # Third-party toolchain configurations
│   └── rules_proto_grpc/   # Prebuilt protoc with gRPC plugin
└── tools/                  # Development tools and scripts
    ├── requirements.in     # Python dependency specifications
    └── requirements.txt    # Locked Python dependencies
```

## How It Works

This project uses a precompiled gRPC plugin extracted from `grpcio-tools` instead of compiling it from C++ source. This approach:

1. **Extracts the plugin**: Uses the gRPC plugin binary bundled in the `grpcio-tools` Python package
2. **Registers toolchains**: Configures Bazel to use the precompiled plugin via custom toolchain registration
3. **Speeds up builds**: Avoids expensive C++ compilation, reducing build times from ~99s to ~3.3s

See `thirdparty/rules_proto_grpc/` for the toolchain implementation details.

## Troubleshooting

### Bazel Version Mismatch

If you encounter version-related errors:
```bash
# Verify .bazelversion matches your installed version
cat .bazelversion

# With Bazelisk, this is handled automatically
bazel version
```

### Module Resolution Issues

```bash
# Clear Bazel cache and rebuild
bazel clean --expunge
bazel build //...
```

### Python Dependency Issues

```bash
# Regenerate Python dependency lock file
bazel run @@//tools:generate_requirements_txt

# Verify the requirements.txt is up to date
git diff tools/requirements.txt
```

## Additional Resources

- [Bazel Documentation](https://bazel.build/)
- [rules_proto_grpc Documentation](https://rules-proto-grpc.com/)
- [Aspect Build's toolchains_protoc](https://github.com/aspect-build/toolchains_protoc) - Inspiration for this approach
- [gRPC Issue #38078](https://github.com/grpc/grpc/issues/38078) - Request for official precompiled plugin distribution

## Contributing

When making changes:
1. Follow the existing code style and structure
2. Update this DEVELOPMENT.md if you change the build process or dependencies
3. Run formatters and linters before committing: `bazel run //tools/format:buildifier`
4. Ensure all tests pass: `bazel test //...`
5. Verify lint checks pass: `bazel run //tools/format:buildifier.check`
