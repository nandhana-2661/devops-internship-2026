#!/bin/bash

IMAGE_NAME=$1
DOCKERFILE=$2

echo "======================================"
echo " Sprint 2 - Trivy Security Scan"
echo "======================================"

echo "Building Docker image: $IMAGE_NAME"
docker build -f "$DOCKERFILE" -t "$IMAGE_NAME" .

if [ $? -ne 0 ]; then
    echo "Docker build FAILED"
    exit 1
fi

echo ""
echo "Trivy vulnerability report:"
echo "--------------------------------------"

trivy image \
  --severity HIGH,CRITICAL \
  --ignore-unfixed \
  "$IMAGE_NAME"

echo ""
echo "Generating JSON report..."

trivy image \
  --severity HIGH,CRITICAL \
  --ignore-unfixed \
  --format json \
  --output "reports/${IMAGE_NAME}.json" \
  "$IMAGE_NAME"

echo ""
echo "Applying security gate..."

trivy image \
  --severity HIGH,CRITICAL \
  --ignore-unfixed \
  --exit-code 1 \
  "$IMAGE_NAME"

if [ $? -ne 0 ]; then
    echo ""
    echo "SECURITY GATE FAILED"
    echo "HIGH/CRITICAL vulnerabilities detected."
    exit 1
fi

echo ""
echo "SECURITY GATE PASSED"
echo "No HIGH/CRITICAL fixed vulnerabilities found."
