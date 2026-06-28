# Attack "MQTT Bruteforce"

> MQTT authentication brute force against the target broker using a controlled wordlist.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_mqtt_bruteforce` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / MQTT |
| Image | `attack-mqtt-bruteforce:latest` |
| Container | `attack-mqtt-bruteforce` |
| Suggested max runtime | `10s` |
| Typical targets/services | `mqtt-broker` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/)<br>[https://attack.mitre.org/techniques/T1110/](https://attack.mitre.org/techniques/T1110/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `1883` | Target port |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_mqtt_bruteforce --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-mqtt-bruteforce attack-mqtt-bruteforce:latest "<TARGET_IP>" "1883"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `mqtt-broker`.
