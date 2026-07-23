FROM python:2.7-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python2.7", "inventory_core.py", "./warehouse_settings.ini", "/data/inbound/shipments.csv", "/data/reconciled/output.pkl"]
