FROM ubuntu:24.04
ARG FFUF_VERSION=2.1.0
ARG FFUF_SHA256=fc2c82736c14dcbea4daf3d3cf3878c1c4773008ba45c2bc0fceba7d17b40bb5
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates curl && \
    curl -fsSL "https://github.com/ffuf/ffuf/releases/download/v${FFUF_VERSION}/ffuf_${FFUF_VERSION}_linux_amd64.tar.gz" -o /tmp/ffuf.tar.gz && \
    echo "${FFUF_SHA256}  /tmp/ffuf.tar.gz" | sha256sum -c - && \
    tar -xzf /tmp/ffuf.tar.gz -C /tmp ffuf && \
    chmod +x /tmp/ffuf && \
    rm -rf /var/lib/apt/lists/* /tmp/ffuf.tar.gz
COPY attackers/web-post-bruteforce/Pwdb_top-1000.txt /tmp/Pwdb_top-1000.txt
COPY attackers/web-post-bruteforce/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh
ENTRYPOINT ["/tmp/entrypoint.sh"]
