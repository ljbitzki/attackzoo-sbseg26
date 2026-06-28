FROM hahwul/dalfox
USER root
COPY attackers/xss-scanner/XSS-payloadbox.txt /app/XSS-payloadbox.txt
COPY --chmod=0777 attackers/xss-scanner/entrypoint.sh /app/runstart.sh
RUN chmod +x /app/dalfox
ENTRYPOINT ["/app/runstart.sh"]
