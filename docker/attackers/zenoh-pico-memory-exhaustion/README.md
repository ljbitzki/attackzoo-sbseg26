# Attack "Zenoh-Pico Memory Exhaustion"

> Memory exhaustion of the Zenoh router/peer through mass creation of resources, sessions, declarations, or pending messages.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_zenoh_pico_memory_exhaustion` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / Zenoh |
| Image | `attack-zenoh-pico-memory-exhaustion:latest` |
| Container | `attack-zenoh-pico-memory-exhaustion` |
| Suggested max runtime | `10s` |
| Typical targets/services | `zenoh-router` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

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
python3 attackzoo.py run iot_zenoh_pico_memory_exhaustion --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-zenoh-pico-memory-exhaustion attack-zenoh-pico-memory-exhaustion:latest "<TARGET_IP>" "7447"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `zenoh-router`.
