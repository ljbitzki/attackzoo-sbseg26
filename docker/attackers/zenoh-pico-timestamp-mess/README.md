# Attack "Zenoh-Pico Timestamp Manipulation Flood"

> Flood of Zenoh/Zenoh-Pico packets with manipulated timestamps to affect target ordering, expiration, or time logic.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_zenoh_pico_timestamp_mess` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / Zenoh |
| Image | `attack-zenoh-pico-timestamp-mess:latest` |
| Container | `attack-zenoh-pico-timestamp-mess` |
| Suggested max runtime | `10s` |
| Typical targets/services | `zenoh-router` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

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
python3 attackzoo.py run iot_zenoh_pico_timestamp_mess --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-zenoh-pico-timestamp-mess attack-zenoh-pico-timestamp-mess:latest "<TARGET_IP>" "7447"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `zenoh-router`.
