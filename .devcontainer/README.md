# Dev Container Configuration

This directory contains the [Development Container](https://containers.dev/) configuration for this project.

## What is a Dev Container?

A dev container is a Docker container specifically configured for development. It provides:

- **Consistent environment** across all developers and CI/CD systems
- **Pre-installed tools** (Bazelisk, Python 3.11, build tools)
- **VS Code integration** with recommended extensions
- **Zero manual setup** - just open and start coding

## Files

- `devcontainer.json` - Main configuration file defining the container
- `setup.sh` - Post-creation script that installs bazelisk and other tools

## Usage

### With VS Code

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Install VS Code [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Open this repository in VS Code
4. Press `F1` → "Dev Containers: Reopen in Container"
5. Wait for initial setup (first time only, ~2-3 minutes)
6. Start developing!

### With GitHub Codespaces

This configuration also works with GitHub Codespaces:

1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Wait for the environment to build
3. Start developing in your browser!

## What's Included

- **Base Image**: Ubuntu 22.04
- **Python**: 3.11 (from devcontainers features)
- **Bazelisk**: v1.20.0 (installed via setup.sh)
- **Build Tools**: gcc, g++, make (for native extensions)
- **Shell**: zsh with Oh My Zsh
- **VS Code Extensions**:
  - Bazel Build Tools
  - Python + Pylance
  - Protocol Buffers (proto3)
  - EditorConfig

## Customization

You can customize the dev container by modifying `devcontainer.json`:

- Add more VS Code extensions to `customizations.vscode.extensions`
- Install additional tools in `setup.sh`
- Add environment variables
- Configure port forwarding
- And more - see [devcontainer.json reference](https://containers.dev/implementors/json_reference/)

## Troubleshooting

**Container fails to build:**
- Ensure Docker is running
- Check Docker has enough resources allocated (4GB RAM minimum)
- Try: "Dev Containers: Rebuild Container" from command palette

**Bazel commands are slow:**
- The container uses a mounted volume for Bazel cache (`.bazel-cache`)
- First builds will be slower; subsequent builds reuse the cache

**Need to reset everything:**
```bash
# Inside the container
bazel clean --expunge
```

Or rebuild the container: `F1` → "Dev Containers: Rebuild Container"
