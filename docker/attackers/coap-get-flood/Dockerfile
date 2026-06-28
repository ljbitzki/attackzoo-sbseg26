FROM python:3.11-alpine
RUN pip3 install --upgrade pip
WORKDIR /tmp
COPY attackers/coap-get-flood/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY attackers/coap-get-flood/entrypoint.sh /tmp/entrypoint.sh
COPY attackers/coap-get-flood/client.py /tmp/client.py
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]
