#!/bin/bash
set -e

echo "Setting up development environment..."

# Install bazelisk
echo "Installing bazelisk..."
BAZELISK_VERSION="v1.20.0"
wget -q "https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-amd64" -O /tmp/bazelisk
chmod +x /tmp/bazelisk
sudo mv /tmp/bazelisk /usr/local/bin/bazel

# Verify bazelisk installation
echo "Verifying bazelisk installation..."
bazel --version

# Pre-download Bazel version specified in .bazelversion
echo "Pre-downloading Bazel $(cat .bazelversion)..."
bazel version || true

# Install build essentials (needed for some Python packages)
echo "Installing build essentials..."
sudo apt-get update -qq
sudo apt-get install -y -qq build-essential

# Install Python development dependencies
echo "Installing Python development tools..."
pip install --quiet --upgrade pip

echo "✅ Development environment setup complete!"
echo ""
echo "You can now run:"
echo "  - bazel build //...     # Build all targets"
echo "  - bazel test //...      # Run all tests"
echo "  - bazel run //:format   # Format code"
echo ""
echo "See DEVELOPMENT.md for more details."
