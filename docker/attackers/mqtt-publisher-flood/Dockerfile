FROM ubuntu:24.04
RUN apt update
RUN apt install mosquitto-clients -y
COPY attackers/mqtt-publisher-flood/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]
