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


def get_protoc_version():
    """Get the protoc version from grpcio_tools package.
    
    The protoc version is obtained from grpc_version.VERSION in grpcio_tools.
    For versions with 3 components (e.g., "5.28.3"), the first component is
    discarded and the remaining components are used (28.3).
    
    Returns:
        tuple: (major, minor, patch) version numbers, or None if cannot determine
    """
    try:
        # Get version from grpc_tools.grpc_version
        from grpc_tools import grpc_version
        version_string = grpc_version.VERSION
        
        # Parse version string - can be "5.28.3", "28.3", "32.0.0", etc.
        version_match = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?', version_string)
        if version_match:
            components = [int(g) for g in version_match.groups() if g is not None]
            
            # If there are 3 components, discard the first one
            # e.g., "5.28.3" -> use 28.3
            # If there are 2 components, use as-is
            # e.g., "28.3" -> use 28.3 or "32.0" -> use 32.0
            if len(components) == 3:
                protoc_major = components[1]
                protoc_minor = components[2]
            elif len(components) == 2:
                protoc_major = components[0]
                protoc_minor = components[1]
            else:
                return None
            
            return (protoc_major, protoc_minor, 0)
    except Exception:
        pass
    
    return None


def filter_unsupported_flags(args, protoc_version):
    """Filter out flags not supported by the protoc version.
    
    Args:
        args: List of command-line arguments
        protoc_version: tuple of (major, minor, patch) or None
        
    Returns:
        Filtered list of arguments with unsupported flags removed if needed
    """
    # If we can't determine version or version is >= 32.0, don't filter
    if protoc_version is None or protoc_version[0] >= 32:
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

