#!/usr/bin/env python3
"""Wrapper for protoc that filters out unsupported flags for legacy protoc versions.

This wrapper checks the protoc version and filters out flags that are not supported
by protoc versions below 32.0, specifically:
- --option_dependencies
- --option_dependencies_violation_msg

These flags were introduced in protoc 32.0 and are used by rules_proto 7.x.
"""

import re
import sys
import runpy


USING_LEGACY_PROTOC = False


def filter_unsupported_flags(args, should_filter = USING_LEGACY_PROTOC):
    """Filter out flags not supported by the protoc version.

    Args:
        args: List of command-line arguments
        protoc_version: tuple of (major, minor, patch)

    Returns:
        Filtered list of arguments with unsupported flags removed if needed
    """
    if not should_filter:
        return args

    # Protoc version is below 32, filter out unsupported flags
    filtered_args = []
    skip_next = False

    for arg in args:
        if skip_next:
            skip_next = False
            continue

        # Filter out --option_dependencies and its value
        if arg == '--option_dependencies':
            skip_next = True
            continue

        # Filter out --option_dependencies_violation_msg and its value
        if arg == '--option_dependencies_violation_msg':
            skip_next = True
            continue

        # Filter out --option_dependencies=value format
        if arg.startswith('--option_dependencies='):
            continue

        # Filter out --option_dependencies_violation_msg=value format
        if arg.startswith('--option_dependencies_violation_msg='):
            continue

        filtered_args.append(arg)

    return filtered_args


def main():
    # Get protoc version
    protoc_version = get_protoc_version()

    # Filter out unsupported flags from sys.argv if needed
    # sys.argv[0] is the script name, keep it
    filtered_argv = [sys.argv[0]] + filter_unsupported_flags(sys.argv[1:], protoc_version)

    # Replace sys.argv with filtered arguments
    sys.argv = filtered_argv

    # Run the actual protoc from grpc_tools
    runpy.run_module('grpc_tools.protoc', run_name='__main__')


if __name__ == '__main__':
    main()
