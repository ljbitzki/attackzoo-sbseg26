# Attack "Zenoh-Pico Protocol Fuzzer"

> Sending malformed or mutated Zenoh/Zenoh-Pico messages to trigger errors, exceptions, or crashes on the target.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_zenoh_pico_proto_fuzzer` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / Zenoh |
| Image | `attack-zenoh-pico-proto-fuzzer:latest` |
| Container | `attack-zenoh-pico-proto-fuzzer` |
| Suggested max runtime | `10s` |
| Typical targets/services | `zenoh-router` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/004/](https://attack.mitre.org/techniques/T1499/004/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `7447` | Target port |

## Intensity Parameters

| Parameter | Default |
|---|---|
| `duration_s` |  |
| `count` | `1000` |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_zenoh_pico_proto_fuzzer --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-zenoh-pico-proto-fuzzer attack-zenoh-pico-proto-fuzzer:latest "<TARGET_IP>" "7447"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `zenoh-router`.
