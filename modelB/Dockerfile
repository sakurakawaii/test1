# PY3-MIGRATED: base image python:2.7-slim -> python:3.10-slim
FROM python:3.10-slim

WORKDIR /app

# PY3-MIGRATED: mysqlclient (the Python 3 MySQLdb replacement) is a C extension and
# needs system build/runtime libraries that the old pure-wheel install did not.
# default-libmysqlclient-dev provides the client headers/lib; gcc + pkg-config
# build the extension. Without these, `pip install mysqlclient` fails on slim.
# PY3-REVIEW: if the team switches to PyMySQL (pure Python) instead, this apt-get
# layer can be removed entirely. Consider a multi-stage build to drop build tools
# from the final image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        pkg-config \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# PY3-MIGRATED: interpreter python2.7 -> python3 in the container entrypoint.
CMD ["python3", "inventory_core.py", "./warehouse_settings.ini", "/data/inbound/shipments.csv", "/data/reconciled/output.pkl"]
