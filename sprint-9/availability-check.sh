#!/bin/sh

while true; do
    STATUS=$(curl -s -o /dev/null --max-time 5 -w "%{http_code}" \
      http://sprint9-web.sprint-9.svc.cluster.local/)

    echo "$(date '+%H:%M:%S') HTTP Status: $STATUS"
    sleep 1
done
