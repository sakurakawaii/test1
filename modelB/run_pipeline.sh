#!/bin/bash
# run_pipeline.sh
# Nightly inventory reconciliation runner. Cron-invoked at 02:00 local time.

set -e

cd "$(dirname "$0")"

# PY3-REVIEW: This activates a virtualenv at ./venv. It MUST be rebuilt with
# Python 3.10 before this runner is used (e.g. `python3.10 -m venv venv &&
# venv/bin/pip install -r requirements.txt`). The bin/activate layout is the same
# under Python 3, so this line does not change, but a venv still containing the
# Python 2 interpreter will run the old code. Environment assumption: venv exists
# and is a Python 3.10 environment.
source venv/bin/activate

# Environment assumption: cwd is prepended to PYTHONPATH so the pipeline's
# top-level modules (stock_router, sku_classifier, warehouse_config, ...) resolve
# as absolute imports. This is why `import stock_router` in inventory_core.py
# still works under Python 3 - the modules are on sys.path, not a package using
# implicit relative imports. Keep this export.
export PYTHONPATH="$(pwd):$PYTHONPATH"

CONFIG=./warehouse_settings.ini
INPUT=/data/inbound/shipments_$(date +%Y%m%d).csv
OUTPUT=/data/reconciled/output_$(date +%Y%m%d).pkl

# PY3-MIGRATED: interpreter python2.7 -> python3. Use the venv's `python` (now
# Python 3.10) rather than a hard-coded minor version so the runner tracks the
# activated environment.
# PY3-REVIEW: the .pkl written here now uses Python 3's default pickle protocol
# and contains str/float values (see inventory_core.py). Any Python 2 consumer of
# /data/reconciled/*.pkl will fail to load it. Confirm all downstream readers are
# Python 3, or pin protocol=2 in inventory_core.py.
python inventory_core.py "$CONFIG" "$INPUT" "$OUTPUT"  # PY3-MIGRATED: python2.7 -> python (venv Python 3.10)

echo "Pipeline run complete."
