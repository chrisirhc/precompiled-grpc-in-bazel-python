"""Modified python protobuf and grpc rules."""

load(":python_grpc_compile.bzl", _python_grpc_compile = "python_grpc_compile")

# Export python rules
python_grpc_compile = _python_grpc_compile