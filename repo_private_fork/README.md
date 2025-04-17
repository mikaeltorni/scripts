# repo_private_fork.py

A small utility to clone a public GitHub repo, create a private fork under your account via the GitHub API, rewire origin/upstream remotes, and push the default branch.

## Features

- Clones any public owner/repo
- Creates a private repo of the given name in your GitHub account (via API)
- Renames the original origin to upstream and adds your fork as origin
- Detects and pushes the default branch (e.g. main or master)

## Requirements

- Python 3.7+
- git on your PATH
- requests (install via pip install requests)
- A GitHub personal access token with repo scope

## Usage
```bash
export GITHUB_TOKEN=YOUR_TOKEN_HERE
python repo_private_fork.py \
  --upstream openai/codex \
  --name    codex \
  --output-dir ./workdir
```

### Arguments
--upstream owner/repo of the public repo (default: openai/codex)
--name name for your private fork (default: codex)
--output-dir where to clone (defaults to ./<name>)
--token GitHub token (or set env GITHUB_TOKEN)
