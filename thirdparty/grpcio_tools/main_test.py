#!/usr/bin/env python3
"""Unit tests for main.py protoc wrapper."""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the current directory to the path to import main
sys.path.insert(0, os.path.dirname(__file__))

import main


class TestGetProtocVersion(unittest.TestCase):
    """Test get_protoc_version function."""
    
    def test_three_component_version(self):
        """Test version with 3 components - first component is discarded."""
        mock_grpc_version = MagicMock()
        mock_grpc_version.VERSION = "5.28.3"
        mock_grpc_tools = MagicMock()
        mock_grpc_tools.grpc_version = mock_grpc_version
        
        with patch.dict('sys.modules', {
            'grpc_tools': mock_grpc_tools,
            'grpc_tools.grpc_version': mock_grpc_version
        }):
            version = main.get_protoc_version()
            self.assertEqual(version, (28, 3, 0))
    
    def test_three_component_version_6_major(self):
        """Test version with major=6 and 3 components."""
        mock_grpc_version = MagicMock()
        mock_grpc_version.VERSION = "6.30.1"
        mock_grpc_tools = MagicMock()
        mock_grpc_tools.grpc_version = mock_grpc_version
        
        with patch.dict('sys.modules', {
            'grpc_tools': mock_grpc_tools,
            'grpc_tools.grpc_version': mock_grpc_version
        }):
            version = main.get_protoc_version()
            self.assertEqual(version, (30, 1, 0))
    
    def test_two_component_version(self):
        """Test version with 2 components - used as-is."""
        mock_grpc_version = MagicMock()
        mock_grpc_version.VERSION = "28.3"
        mock_grpc_tools = MagicMock()
        mock_grpc_tools.grpc_version = mock_grpc_version
        
        with patch.dict('sys.modules', {
            'grpc_tools': mock_grpc_tools,
            'grpc_tools.grpc_version': mock_grpc_version
        }):
            version = main.get_protoc_version()
            self.assertEqual(version, (28, 3, 0))
    
    def test_future_version_32_three_components(self):
        """Test future version 32.0.0 with 3 components."""
        mock_grpc_version = MagicMock()
        mock_grpc_version.VERSION = "32.0.0"
        mock_grpc_tools = MagicMock()
        mock_grpc_tools.grpc_version = mock_grpc_version
        
        with patch.dict('sys.modules', {
            'grpc_tools': mock_grpc_tools,
            'grpc_tools.grpc_version': mock_grpc_version
        }):
            version = main.get_protoc_version()
            # With 3 components, first is discarded, so we get (0, 0, 0)
            # This means version 32+ should probably use 2-component format
            self.assertEqual(version, (0, 0, 0))
    
    def test_future_version_32_two_components(self):
        """Test future version 32.0 with 2 components."""
        mock_grpc_version = MagicMock()
        mock_grpc_version.VERSION = "32.0"
        mock_grpc_tools = MagicMock()
        mock_grpc_tools.grpc_version = mock_grpc_version
        
        with patch.dict('sys.modules', {
            'grpc_tools': mock_grpc_tools,
            'grpc_tools.grpc_version': mock_grpc_version
        }):
            version = main.get_protoc_version()
            self.assertEqual(version, (32, 0, 0))
    
    def test_missing_grpc_version(self):
        """Test when grpc_version module is not available."""
        # Simulate import failure
        def import_error(*args, **kwargs):
            raise ImportError("No module named 'grpc_tools.grpc_version'")
        
        with patch('builtins.__import__', side_effect=import_error):
            version = main.get_protoc_version()
            self.assertIsNone(version)


class TestFilterUnsupportedFlags(unittest.TestCase):
    """Test filter_unsupported_flags function."""
    
    def test_filter_with_old_version(self):
        """Test filtering with version < 32."""
        args = ['--proto_path=.', '--option_dependencies', 'file.proto', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, (28, 3, 0))
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])
    
    def test_no_filter_with_new_version(self):
        """Test no filtering with version >= 32."""
        args = ['--proto_path=.', '--option_dependencies', 'file.proto', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, (32, 0, 0))
        self.assertEqual(filtered, args)
    
    def test_no_filter_with_none_version(self):
        """Test no filtering when version cannot be determined."""
        args = ['--proto_path=.', '--option_dependencies', 'file.proto', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, None)
        self.assertEqual(filtered, args)
    
    def test_filter_option_dependencies_equals_format(self):
        """Test filtering --option_dependencies=value format."""
        args = ['--proto_path=.', '--option_dependencies=file.proto', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, (28, 3, 0))
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])
    
    def test_filter_violation_msg(self):
        """Test filtering --option_dependencies_violation_msg."""
        args = ['--proto_path=.', '--option_dependencies_violation_msg', 'error msg', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, (28, 3, 0))
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])
    
    def test_filter_violation_msg_equals_format(self):
        """Test filtering --option_dependencies_violation_msg=value format."""
        args = ['--proto_path=.', '--option_dependencies_violation_msg=error', '--python_out=out']
        filtered = main.filter_unsupported_flags(args, (28, 3, 0))
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])
    
    def test_filter_both_flags(self):
        """Test filtering both option_dependencies flags."""
        args = [
            '--proto_path=.',
            '--option_dependencies', 'file.proto',
            '--option_dependencies_violation_msg', 'error',
            '--python_out=out'
        ]
        filtered = main.filter_unsupported_flags(args, (28, 3, 0))
        self.assertEqual(filtered, ['--proto_path=.', '--python_out=out'])
    
    def test_no_filtering_needed(self):
        """Test when no flags need filtering."""
        args = ['--proto_path=.', '--python_out=out', 'file.proto']
        filtered = main.filter_unsupported_flags(args, (28, 3, 0))
        self.assertEqual(filtered, args)


if __name__ == '__main__':
    unittest.main()
