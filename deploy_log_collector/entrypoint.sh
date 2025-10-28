#!/bin/bash

set -e

INTERVAL=${INTERVAL:-3600}

echo "Start Python Log Collecotr with interval: $INTERVAL seconds."
while true; do
    echo "[$(date)] Running log collection..."
    python3 mysql_export.py
    echo "[$(date)] Sleeping for $INTERVAL seconds..."
    sleep "$INTERVAL"
done
