FROM ubuntu:24.04
RUN apt update
RUN apt install nmap -y
COPY attackers/port-scanner-tcp/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
