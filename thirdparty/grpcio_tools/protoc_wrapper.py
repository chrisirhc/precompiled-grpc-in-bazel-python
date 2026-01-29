#!/usr/bin/env python3
"""Wrapper script for protoc that filters out unsupported flags.

This wrapper filters out flags that are not supported by the legacy protoc
bundled in grpcio-tools (protoc ~28.x), specifically:
- --option_dependencies
- --option_dependencies_violation_msg

These flags were introduced in protoc 32.0 and are used by rules_proto 7.x,
but the grpcio-tools package bundles an older version of protoc.
"""

import sys
import runpy


def filter_unsupported_flags(args):
    """Filter out flags not supported by legacy protoc.
    
    Args:
        args: List of command-line arguments
        
    Returns:
        Filtered list of arguments with unsupported flags removed
    """
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
    # Filter out unsupported flags from sys.argv
    # sys.argv[0] is the script name, keep it
    filtered_argv = [sys.argv[0]] + filter_unsupported_flags(sys.argv[1:])
    
    # Replace sys.argv with filtered arguments
    sys.argv = filtered_argv
    
    # Run the actual protoc from grpc_tools
    runpy.run_module('grpc_tools.protoc', run_name='__main__')


if __name__ == '__main__':
    main()
