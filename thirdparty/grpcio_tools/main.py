#!/usr/bin/env python3
"""Wrapper for protoc that filters out unsupported flags for legacy protoc versions.

This wrapper checks the protoc version and filters out flags that are not supported
by protoc versions below 32.0, specifically:
- --option_dependencies
- --option_dependencies_violation_msg

These flags were introduced in protoc 32.0 and are used by rules_proto 7.x.
"""

import re
import subprocess
import sys
import runpy


def get_protoc_version():
    """Get the protoc version from grpc_tools.
    
    Returns:
        tuple: (major, minor, patch) version numbers, or None if cannot determine
    """
    try:
        # Import grpc_tools to get the protoc version
        import grpc_tools.protoc
        
        # Try to get version by running protoc --version
        # We need to temporarily capture the output
        result = subprocess.run(
            [sys.executable, '-m', 'grpc_tools.protoc', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Parse version from output like "libprotoc 28.3" or "libprotoc 32.0"
        version_match = re.search(r'libprotoc\s+(\d+)\.(\d+)', result.stdout)
        if version_match:
            major = int(version_match.group(1))
            minor = int(version_match.group(2))
            return (major, minor, 0)
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

