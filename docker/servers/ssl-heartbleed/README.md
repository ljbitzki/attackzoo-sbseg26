# Server "HTTPS Heartbleed Server"

> Provide a vulnerable HTTPS target for Heartbleed attack validation and observable TLS traffic generation.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `ssl-heartbleed` |
| Role | target-server |
| Image | `server-ssl-heartbleed:latest` |
| Container | `server-ssl-heartbleed` |
| Base | `vulhub/openssl:1.0.1c-with-nginx` |
| Service | nginx with Heartbleed-vulnerable OpenSSL for a controlled experiment |
| Protocols | `https`, `tls` |
| Internal ports | `443/tcp` |
| Published ports | `8443:443/tcp` |

## Execution

```bash
docker run -d --rm --name server-ssl-heartbleed -p 8443:443 server-ssl-heartbleed:latest
```

## Container IP

```bash
docker container inspect server-ssl-heartbleed --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-ssl-heartbleed
```

## Related Attacks

- `web_https_heartbleed`

## Related Benign Clients

- `client-random:https`
- `client-super:https`

## Testbed Observability

- TLS handshakes
- HTTPS traffic
- nginx logs when emitted by the container

In controlled experiments, use `python3 attackzoo.py experiment --server server-ssl-heartbleed` to associate target-container telemetry with execution artifacts.
