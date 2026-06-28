FROM ubuntu:24.04
RUN apt update
RUN apt install build-essential cmake git pkg-config libpcap-dev -y
WORKDIR /opt
COPY attackers/xrce-dds-discovery-poison/attack_discovery_poison.c /opt/attack_discovery_poison.c
COPY attackers/xrce-dds-discovery-poison/install.sh /opt/install.sh
RUN chmod +x /opt/install.sh
RUN /opt/install.sh
WORKDIR /opt/Micro-XRCE-DDS-Client
COPY attackers/xrce-dds-discovery-poison/compile.sh /opt/Micro-XRCE-DDS-Client/compile.sh
RUN chmod +x /opt/Micro-XRCE-DDS-Client/compile.sh
RUN /opt/Micro-XRCE-DDS-Client/compile.sh
COPY attackers/xrce-dds-discovery-poison/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]