#!/usr/bin/env bash
set -e

velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.13.0 \
  --bucket k8s-backups \
  --secret-file ./velero/credentials-velero \
  --backup-location-config region=minio,s3ForcePathStyle=true,s3Url=http://minio.default.svc.cluster.local:9000 \
  --use-volume-snapshots=false

velero backup-location get
