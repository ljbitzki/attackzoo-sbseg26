# Attack "Zenoh-Pico Keepalive Flood"

> Flood of Zenoh/Zenoh-Pico keepalive messages to consume processing and session-handling capacity.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_zenoh_pico_keepalive_flood` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / Zenoh |
| Image | `attack-zenoh-pico-keepalive-flood:latest` |
| Container | `attack-zenoh-pico-keepalive-flood` |
| Suggested max runtime | `10s` |
| Typical targets/services | `zenoh-router` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `7447` | Target port |

## Intensity Parameters

| Parameter | Default |
|---|---|
| `duration_s` | `10` |
| `threads` | `4` |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_zenoh_pico_keepalive_flood --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-zenoh-pico-keepalive-flood attack-zenoh-pico-keepalive-flood:latest "<TARGET_IP>" "7447"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `zenoh-router`.
