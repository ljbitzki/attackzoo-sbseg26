FROM ubuntu:24.04
COPY attackers/idor-path-traversal/ffuf /tmp/ffuf
COPY attackers/idor-path-traversal/LFI-LFISuite-pathtotest.txt /tmp/LFI-LFISuite-pathtotest.txt
COPY attackers/idor-path-traversal/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/ffuf
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]