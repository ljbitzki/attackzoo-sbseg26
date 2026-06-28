# Attack "XRCE-DDS Discovery Poisoning"

> Poisoning or manipulation of XRCE-DDS agent discovery messages to induce incorrect association, redirection, or discovery degradation.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_xrce_dds_discovery_poison` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / XRCE-DDS |
| Image | `attack-xrce-dds-discovery-poison:latest` |
| Container | `attack-xrce-dds-discovery-poison` |
| Suggested max runtime | `10s` |
| Typical targets/services | `xrce-dds-agent` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/tactics/TA0009/](https://attack.mitre.org/tactics/TA0009/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1557/](https://attack.mitre.org/techniques/T1557/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Advertised fake agent IP/FQDN |
| `--target_port` | `port` | no | `6666` | Advertised fake agent port |

## Intensity Parameters

| Parameter | Default |
|---|---|
| `duration_s` |  |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_xrce_dds_discovery_poison --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-xrce-dds-discovery-poison attack-xrce-dds-discovery-poison:latest "<TARGET_IP>" "6666"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `xrce-dds-agent`.
