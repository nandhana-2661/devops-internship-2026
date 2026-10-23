#!/usr/bin/env bash
set -e

velero restore create critical-app-restore \
  --from-backup critical-app-backup \
  --wait

velero restore get

kubectl get all -n critical-app
