#!/bin/bash
# run_pipeline.sh
# Nightly inventory reconciliation runner. Cron-invoked at 02:00 local time.

set -e

cd "$(dirname "$0")"

# ENVIRONMENT ASSUMPTION: a virtualenv named `venv` sits next to this script.
# PY3-REVIEW: this venv MUST be rebuilt with Python 3.10
#   (python3.10 -m venv venv && venv/bin/pip install -r requirements.txt).
# Activating a venv that still contains the Python 2 interpreter/packages will
# fail at import time. The bin/activate layout is unchanged between Py2 and Py3
# venvs on Linux, so this line itself does not change.
source venv/bin/activate

# This is what makes inventory_core.py's flat `import stock_router` etc.
# resolve (the modules are not a package). Preserved deliberately.
export PYTHONPATH="$(pwd):$PYTHONPATH"

# PY3-REVIEW [HIGH - routing determinism]: stock_router uses hash(str(sku)),
# which Python 3 randomizes per process. Uncomment the line below to pin the
# hash seed so partition assignment is stable across nightly runs (values will
# still differ from the Python 2 era). See stock_router.py for the alternative
# content-hash fix.
# export PYTHONHASHSEED=0

CONFIG=./warehouse_settings.ini
INPUT=/data/inbound/shipments_$(date +%Y%m%d).csv
OUTPUT=/data/reconciled/output_$(date +%Y%m%d).pkl

# PY3-MIGRATED: `python2.7` -> `python`. After `source venv/bin/activate`,
# `python` is the venv's interpreter (must be Python 3.10 per the note above).
# The original hardcoded `python2.7` bypassed the venv and used the system
# Python 2 - that must not happen post-migration.
# PY3-REVIEW: if the venv cannot be guaranteed active, replace with an absolute
# path to the 3.10 interpreter, e.g. ./venv/bin/python.
python inventory_core.py "$CONFIG" "$INPUT" "$OUTPUT"

echo "Pipeline run complete."
