FROM ubuntu:24.04
RUN apt update
RUN apt install arp-scan -y
COPY attackers/arp-scan/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]