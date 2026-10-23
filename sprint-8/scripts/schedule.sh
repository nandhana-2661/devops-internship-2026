#!/usr/bin/env bash
set -e

velero schedule create critical-app-daily \
  --schedule="0 2 * * *" \
  --include-namespaces critical-app

velero schedule get
