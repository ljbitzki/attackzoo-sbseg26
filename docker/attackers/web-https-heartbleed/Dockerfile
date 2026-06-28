FROM python:3.9-alpine
RUN apk add --no-cache bash
COPY attackers/web-https-heartbleed/ssltest.py /tmp/ssltest.py
COPY attackers/web-https-heartbleed/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]
