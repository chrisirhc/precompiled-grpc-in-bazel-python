#!/usr/bin/env python3
"""Unit tests for main.py protoc wrapper."""

import unittest
import sys
import os

# Add the current directory to the path to import main
sys.path.insert(0, os.path.dirname(__file__))

import main


class TestFilterUnsupportedFlags(unittest.TestCase):
    """Test filter_unsupported_flags function."""

    def test_filter_with_old_version(self):
        """Test filtering with version < 32."""
        args = ['--proto_path=.', '--option_dependencies', 'file.proto', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, True)
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])

    def test_no_filter_with_new_version(self):
        """Test no filtering with version >= 32."""
        args = ['--proto_path=.', '--option_dependencies', 'file.proto', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, False)
        self.assertEqual(filtered, args)


    def test_filter_option_dependencies_equals_format(self):
        """Test filtering --option_dependencies=value format."""
        args = ['--proto_path=.', '--option_dependencies=file.proto', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, True)
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])

    def test_filter_violation_msg(self):
        """Test filtering --option_dependencies_violation_msg."""
        args = ['--proto_path=.', '--option_dependencies_violation_msg', 'error msg', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, True)
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])

    def test_filter_violation_msg_equals_format(self):
        """Test filtering --option_dependencies_violation_msg=value format."""
        args = ['--proto_path=.', '--option_dependencies_violation_msg=error', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, True)
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])

    def test_filter_both_flags(self):
        """Test filtering both option_dependencies flags."""
        args = [
            '--proto_path=.',
            '--option_dependencies', 'file.proto',
            '--option_dependencies_violation_msg', 'error',
            '--python_out=out'
        ]
        filtered = main.filter_unsupported_flags(args, True)
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])

    def test_no_filtering_needed(self):
        """Test when no flags need filtering."""
        args = ['--proto_path=.', '--python_out=out', 'file.proto']
        filtered = main.filter_unsupported_flags(args, False)
        self.assertEqual(filtered, args)


if __name__ == '__main__':
    unittest.main()
