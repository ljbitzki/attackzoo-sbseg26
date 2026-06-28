FROM python:3.11-alpine

WORKDIR /app

COPY attackers/mqtt-qos-amplification/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY attackers/mqtt-qos-amplification/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY attackers/mqtt-qos-amplification/mqtt-qos-amplification.py /app/mqtt-qos-amplification.py

ENV TARGET_HOST=localhost

ENTRYPOINT ["/app/entrypoint.sh"]
