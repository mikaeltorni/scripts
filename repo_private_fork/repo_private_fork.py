#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys

import requests

API = "https://api.github.com"


def run(cmd, cwd=None):
    print(f"> {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def get_token(args):
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        sys.exit("Error: set --token or env GITHUB_TOKEN")
    return token


def gh_request(method, path, token, data=None):
    url = f"{API}{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {token}",
    }
    resp = requests.request(method, url, headers=headers, json=data)
    if not resp.ok:
        print(resp.text, file=sys.stderr)
        resp.raise_for_status()
    return resp.json()


def create_private_repo(name, token):
    # POST /user/repos
    data = {"name": name, "private": True}
    return gh_request("POST", "/user/repos", token, data)


def get_user(token):
    info = gh_request("GET", "/user", token)
    return info["login"]


def get_default_branch(owner, repo, token):
    info = gh_request("GET", f"/repos/{owner}/{repo}", token)
    return info.get("default_branch", "main")


def main():
    p = argparse.ArgumentParser(
        description="Clone a public repo and make a private fork"
    )
    p.add_argument(
        "--upstream",
        default="openai/codex",
        help="owner/repo of the public upstream (default: openai/codex)",
    )
    p.add_argument(
        "--name",
        default="codex",
        help="name for your private fork (default: codex)",
    )
    p.add_argument(
        "--output-dir",
        default=None,
        help="where to clone (defaults to ./<name>)",
    )
    p.add_argument(
        "--token",
        default=None,
        help="GitHub personal access token (or set GITHUB_TOKEN)",
    )
    args = p.parse_args()

    token = get_token(args)
    owner, repo = args.upstream.split("/", 1)
    your_user = get_user(token)
    default_branch = get_default_branch(owner, repo, token)

    dest = args.output_dir or args.name
    upstream_url = f"https://github.com/{owner}/{repo}.git"
    fork_url = f"https://github.com/{your_user}/{args.name}.git"

    # 1. Clone upstream
    run(["git", "clone", upstream_url, dest])

    # 2. Create private fork on GH
    print("Creating private repo on GitHub…")
    create_private_repo(args.name, token)

    # 3. Rewire remotes
    run(["git", "remote", "rename", "origin", "upstream"], cwd=dest)
    run(["git", "remote", "add", "origin", fork_url], cwd=dest)

    # 4. Push
    run(
        ["git", "push", "-u", "origin", default_branch],
        cwd=dest,
    )

    print("\nDone! Your private fork is ready:")
    print(f"  Upstream: {upstream_url}")
    print(f"  Origin:   {fork_url}")
    print(f"  Default branch: {default_branch}")


if __name__ == "__main__":
    main()
