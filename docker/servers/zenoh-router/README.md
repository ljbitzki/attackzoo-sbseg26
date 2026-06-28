# Server "Zenoh Router"

> Serve as a Zenoh router for Zenoh-Pico attacks against fragmentation, keepalive, memory, fuzzing, sequence, and timestamp behavior.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `zenoh-router` |
| Role | target-server |
| Image | `server-zenoh-router:latest` |
| Container | `server-zenoh-router` |
| Base | `eclipse/zenoh:1.7.2` |
| Service | Eclipse Zenoh router |
| Protocols | `zenoh`, `tcp` |
| Internal ports | `7447/tcp` |
| Published ports | `7447:7447/tcp` |

## Execution

```bash
docker run -d --rm --name server-zenoh-router -p 7447:7447 server-zenoh-router:latest
```

## Container IP

```bash
docker container inspect server-zenoh-router --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-zenoh-router
```

## Related Attacks

- `iot_zenoh_pico_fragments_reassembly`
- `iot_zenoh_pico_keepalive_flood`
- `iot_zenoh_pico_memory_exhaustion`
- `iot_zenoh_pico_proto_fuzzer`
- `iot_zenoh_pico_sequence_exhaustion`
- `iot_zenoh_pico_timestamp_mess`

## Related Benign Clients

- `client-super:zenoh`

## Testbed Observability

- Zenoh TCP/7447 connections
- container stdout logs
- optional telemetry through docker stats

In controlled experiments, use `python3 attackzoo.py experiment --server server-zenoh-router` to associate target-container telemetry with execution artifacts.
