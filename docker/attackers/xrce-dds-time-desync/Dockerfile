FROM ubuntu:24.04
RUN apt update
RUN apt install build-essential cmake git pkg-config libpcap-dev -y
WORKDIR /opt
COPY attackers/xrce-dds-time-desync/attack_time_desync.c /opt/attack_time_desync.c
COPY attackers/xrce-dds-time-desync/install.sh /opt/install.sh
RUN chmod +x /opt/install.sh
RUN /opt/install.sh
WORKDIR /opt/Micro-XRCE-DDS-Client
COPY attackers/xrce-dds-time-desync/compile.sh /opt/Micro-XRCE-DDS-Client/compile.sh
RUN chmod +x /opt/Micro-XRCE-DDS-Client/compile.sh
RUN /opt/Micro-XRCE-DDS-Client/compile.sh
COPY attackers/xrce-dds-time-desync/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]