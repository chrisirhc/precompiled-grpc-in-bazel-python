# Precompiled gRPC in Bazel (Python)

Demonstrates using precompiled gRPC protobuf plugins for ~29x faster Python builds in Bazel by avoiding C++ compilation.

## Build & Test Commands

```bash
# Build all targets
bazel build //...

# Run all tests
bazel test //...

# Run tests with verbose output
bazel test //... --test_output=errors
```

## Code Formatting (Buildifier)

```bash
# Format and fix lint issues in BUILD/Starlark files
bazel run //:format

# Check formatting without making changes (CI uses this)
bazel run //tools/format:format.check
```

## Project Structure

- `MODULE.bazel` - Bazel module dependencies (Bzlmod)
- `BUILD.bazel` - Root build file with gRPC compilation targets
- `modules/example_protos/` - Example protocol buffer definitions
- `thirdparty/rules_proto_grpc/` - Prebuilt protoc with gRPC plugin toolchain
- `tools/` - Development tools, Python requirements

## Key Targets

```bash
# Build specific gRPC stubs
bazel build //:thing_python_grpc
bazel build //:greeter_python_grpc
```

## Python Dependencies

Managed via `rules_uv`. To update:
1. Edit `tools/requirements.in`
2. Run: `bazel run @@//tools:generate_requirements_txt`
3. Commit updated `tools/requirements.txt`

## Troubleshooting

```bash
# Clear cache and rebuild
bazel clean --expunge
bazel build //...

# Check module graph
bazel mod graph
```

## Requirements

- Bazel 8.5.1 (specified in `.bazelversion`, use bazelisk for auto-management)
- Python 3.11 (managed by rules_python)
