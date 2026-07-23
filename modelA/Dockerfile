# Dockerfile
# PY3-MIGRATED: base image python:2.7-slim -> python:3.10-slim.
FROM python:3.10-slim

WORKDIR /app

# PY3-REVIEW [build deps]: mysqlclient (in requirements.txt) is a C extension
# and will FAIL to build on python:3.10-slim without system libraries. If the
# image needs the MySQL driver, install build deps before pip, e.g.:
#   RUN apt-get update && apt-get install -y --no-install-recommends \
#         gcc default-libmysqlclient-dev pkg-config \
#       && rm -rf /var/lib/apt/lists/*
# Alternatively switch requirements.txt to the pure-Python PyMySQL to avoid
# compiling anything. No submitted code opens a DB connection, so this is only
# needed once the (unsubmitted) DB layer is included.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# PY3-REVIEW [HIGH - routing determinism]: uncomment to stabilize SKU->
# partition routing across runs (see stock_router.py / run_pipeline.sh).
# ENV PYTHONHASHSEED=0

# PY3-MIGRATED: interpreter python2.7 -> python (python:3.10-slim provides
# Python 3.10 as `python`).
CMD ["python", "inventory_core.py", "./warehouse_settings.ini", "/data/inbound/shipments.csv", "/data/reconciled/output.pkl"]
