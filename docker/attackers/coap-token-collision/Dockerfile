FROM python:3.11-alpine

WORKDIR /app

COPY attackers/coap-token-collision/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY attackers/coap-token-collision/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY attackers/coap-token-collision/coap-token-collision.py /app/coap-token-collision.py

ENV TARGET_HOST=localhost
ENV TARGET_PORT=5683

ENTRYPOINT ["/app/entrypoint.sh"]
