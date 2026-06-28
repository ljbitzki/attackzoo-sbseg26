# Server "SSH Server"

> Serve as a target for SSH brute force and ICMP/SSH tunneling in controlled experiments.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `ssh-server` |
| Role | target-server |
| Image | `server-ssh-server:latest` |
| Container | `server-ssh-server` |
| Base | `ubuntu:24.04` |
| Service | OpenSSH with password authentication enabled for a controlled environment |
| Protocols | `ssh` |
| Internal ports | `22/tcp` |
| Published ports | `2222:22/tcp` |

## Execution

```bash
docker run -d --rm --name server-ssh-server -p 2222:22 server-ssh-server:latest
```

## Container IP

```bash
docker container inspect server-ssh-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker exec -it server-ssh-server cat /var/log/messages
```

## Related Attacks

- `bf_ssh`
- `exf_icmp_tunnel`

## Related Benign Clients

- `client-random:ssh`
- `client-super:ssh`

## Testbed Observability

- SSH authentication attempts
- SSH daemon/rsyslog logs
- TCP/22 traffic in PCAP

In controlled experiments, use `python3 attackzoo.py experiment --server server-ssh-server` to associate target-container telemetry with execution artifacts.
