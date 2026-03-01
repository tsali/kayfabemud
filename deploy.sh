#!/bin/bash
# deploy.sh — Promote evennia-bbs changes to the LIVE Evennia instance.
#
# Run this from /home/tsali/projects/evennia-bbs after committing changes.
# The live Evennia instance symlinks typeclasses/ and commands/ here, so
# a git pull + evennia reload is all that's needed.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIVE_DIR="/opt/evennia/live"
VENV="/opt/evennia/venv/bin/activate"

echo "==> Pulling latest changes..."
cd "$SCRIPT_DIR"
git pull

echo "==> Reloading live Evennia instance..."
cd "$LIVE_DIR"
source "$VENV"
evennia reboot

echo "==> Deploy complete. Live server reloaded."
