FROM ubuntu:24.04
RUN apt update
RUN apt install build-essential -y
WORKDIR /usr/local/bin
COPY attackers/zenoh-pico-keepalive-flood/attack_dos_keepalive_flood.c /usr/local/bin/attack_dos_keepalive_flood.c
COPY attackers/zenoh-pico-keepalive-flood/build.sh /usr/local/bin/build.sh
COPY attackers/zenoh-pico-keepalive-flood/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/build.sh
RUN /usr/local/bin/build.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]