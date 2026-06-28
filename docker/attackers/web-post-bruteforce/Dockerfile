FROM ubuntu:24.04
COPY attackers/web-post-bruteforce/ffuf /tmp/ffuf
COPY attackers/web-post-bruteforce/Pwdb_top-1000.txt /tmp/Pwdb_top-1000.txt
COPY attackers/web-post-bruteforce/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/ffuf
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]