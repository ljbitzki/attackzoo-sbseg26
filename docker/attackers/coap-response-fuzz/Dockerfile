FROM python:3.11-alpine

WORKDIR /app

COPY attackers/coap-response-fuzz/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY attackers/coap-response-fuzz/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY attackers/coap-response-fuzz/coap-response-fuzz.py /app/coap-response-fuzz.py

ENV TARGET_HOST=localhost
ENV TARGET_PORT=5683

ENTRYPOINT ["/app/entrypoint.sh"]
