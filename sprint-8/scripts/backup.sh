#!/usr/bin/env bash
set -e

velero backup create critical-app-backup \
  --include-namespaces critical-app \
  --wait

velero backup get
