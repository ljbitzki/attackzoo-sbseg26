# Attack "XRCE-DDS UDP DoS"

> UDP packet flood against the XRCE-DDS agent to degrade network or service availability.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_xrce_dds_udp_dos` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / XRCE-DDS |
| Image | `attack-xrce-dds-udp-dos:latest` |
| Container | `attack-xrce-dds-udp-dos` |
| Suggested max runtime | `10s` |
| Typical targets/services | `xrce-dds-agent` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `8888` | Target port |

## Intensity Parameters

| Parameter | Default |
|---|---|
| `duration_s` | `10` |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_xrce_dds_udp_dos --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-xrce-dds-udp-dos attack-xrce-dds-udp-dos:latest "<TARGET_IP>" "8888"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `xrce-dds-agent`.
