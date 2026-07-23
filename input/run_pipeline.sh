#!/bin/bash
# run_pipeline.sh
# Nightly inventory reconciliation runner. Cron-invoked at 02:00 local time.

set -e

cd "$(dirname "$0")"

source venv/bin/activate

export PYTHONPATH="$(pwd):$PYTHONPATH"

CONFIG=./warehouse_settings.ini
INPUT=/data/inbound/shipments_$(date +%Y%m%d).csv
OUTPUT=/data/reconciled/output_$(date +%Y%m%d).pkl

python2.7 inventory_core.py "$CONFIG" "$INPUT" "$OUTPUT"

echo "Pipeline run complete."
