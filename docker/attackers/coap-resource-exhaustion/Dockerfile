FROM python:3.11-alpine

WORKDIR /app

COPY attackers/coap-resource-exhaustion/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY attackers/coap-resource-exhaustion/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY attackers/coap-resource-exhaustion/coap-resource-exhaustion.py /app/coap-resource-exhaustion.py

ENV TARGET_HOST=localhost
ENV TARGET_PORT=5683

ENTRYPOINT ["/app/entrypoint.sh"]
