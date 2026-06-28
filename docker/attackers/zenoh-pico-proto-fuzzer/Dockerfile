FROM ubuntu:24.04
RUN apt update
RUN apt install build-essential -y
WORKDIR /usr/local/bin
COPY attackers/zenoh-pico-proto-fuzzer/attack_protocol_fuzzer.c /usr/local/bin/attack_protocol_fuzzer.c
COPY attackers/zenoh-pico-proto-fuzzer/build.sh /usr/local/bin/build.sh
COPY attackers/zenoh-pico-proto-fuzzer/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/build.sh
RUN /usr/local/bin/build.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]