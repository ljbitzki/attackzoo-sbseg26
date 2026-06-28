# Server "Telnet Server"

> Serve as a target for Telnet brute force and simple benign login traffic.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `telnet-server` |
| Role | target-server |
| Image | `server-telnet-server:latest` |
| Container | `server-telnet-server` |
| Base | `ubuntu:24.04` |
| Service | telnetd via xinetd |
| Protocols | `telnet` |
| Internal ports | `23/tcp` |
| Published ports | `2323:23/tcp` |

## Execution

```bash
docker run -d --rm --name server-telnet-server -p 2323:23 server-telnet-server:latest
```

## Container IP

```bash
docker container inspect server-telnet-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-telnet-server
```

## Related Attacks

- `bf_telnet`

## Related Benign Clients

- `client-random:telnet`
- `client-super:telnet`

## Testbed Observability

- Telnet TCP/23 connections
- xinetd/telnetd logs when available
- login attempts

In controlled experiments, use `python3 attackzoo.py experiment --server server-telnet-server` to associate target-container telemetry with execution artifacts.
