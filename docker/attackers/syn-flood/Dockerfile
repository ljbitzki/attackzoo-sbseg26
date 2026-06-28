FROM python:3.11-alpine
RUN apk add --no-cache git
RUN cd /tmp
RUN pip3 install --upgrade pip
RUN pip3 install scapy
COPY attackers/syn-flood/entrypoint.sh /tmp/entrypoint.sh
COPY attackers/syn-flood/sf.py /tmp/sf.py
WORKDIR /tmp
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]