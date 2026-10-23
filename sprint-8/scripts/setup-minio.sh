#!/usr/bin/env bash
set -e

kubectl apply -f minio/minio.yaml
kubectl rollout status deployment/minio -n default
kubectl get svc minio -n default
