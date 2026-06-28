# Server "Micro XRCE-DDS Agent"

> Serve as an XRCE-DDS agent for IoT attacks involving discovery, entities, fragments, sessions, timing, and UDP DoS.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `xrce-dds-agent` |
| Role | target-server |
| Image | `server-xrce-dds-agent:latest` |
| Container | `server-xrce-dds-agent` |
| Base | `built through agent-source-install.sh` |
| Service | eProsima Micro XRCE-DDS Agent over UDP transport |
| Protocols | `xrce-dds`, `udp` |
| Internal ports | `8888/udp` |
| Published ports | `8888:8888/udp` |

## Execution

```bash
docker run -d --rm -p 8888:8888/udp --name server-xrce-dds-agent server-xrce-dds-agent:latest udp4 -p 8888
```

## Container IP

```bash
docker container inspect server-xrce-dds-agent --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-xrce-dds-agent
```

## Related Attacks

- `iot_xrce_dds_discovery_poison`
- `iot_xrce_dds_entity_flood`
- `iot_xrce_dds_fragment_abuse`
- `iot_xrce_dds_malformed_inject`
- `iot_xrce_dds_session_hijack`
- `iot_xrce_dds_time_desync`
- `iot_xrce_dds_udp_dos`

## Related Benign Clients

- `client-super:xrce-dds`

## Testbed Observability

- XRCE-DDS/UDP datagrams
- agent stdout logs
- optional telemetry through docker stats

## Notes

- There is no direct local Dockerfile; the image is prepared by docker/servers/xrce-dds-agent/agent-source-install.sh.

In controlled experiments, use `python3 attackzoo.py experiment --server server-xrce-dds-agent` to associate target-container telemetry with execution artifacts.
