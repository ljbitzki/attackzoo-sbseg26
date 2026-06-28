# Attack "DNS Tunneling"

> DNS tunneling exfiltration behavior through random domain name resolution.

## Metadata

| Field | Value |
|---|---|
| ID | `exf_dns_tunneling` |
| Category | 5) Exfiltration and Tunneling |
| Subcategory | 5.1 Exfiltration and Tunneling |
| Image | `attack-dns-tunneling:latest` |
| Container | `attack-dns-tunneling` |
| Suggested max runtime | `10s` |
| Typical targets/services | `external/local DNS resolver` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0010/](https://attack.mitre.org/tactics/TA0010/)<br>[https://attack.mitre.org/tactics/TA0011/](https://attack.mitre.org/tactics/TA0011/)<br>[https://attack.mitre.org/techniques/T1048/](https://attack.mitre.org/techniques/T1048/)<br>[https://attack.mitre.org/techniques/T1048/003/](https://attack.mitre.org/techniques/T1048/003/)<br>[https://attack.mitre.org/techniques/T1071/](https://attack.mitre.org/techniques/T1071/)<br>[https://attack.mitre.org/techniques/T1071/004/](https://attack.mitre.org/techniques/T1071/004/) |

## Parameters

This attack does not take a target. It uses DNS servers 1.1.1.1, 1.0.0.1, 8.8.8.8, 8.8.4.4, 9.9.9.9, 149.112.112.112, and 76.76.19.19.

## Intensity Parameters

| Parameter | Default |
|---|---|
| `duration_s` |  |
| `count` | `200` |
| `delay_ms` | `200` |
| `payload_size` |  |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run exf_dns_tunneling --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-dns-tunneling attack-dns-tunneling:latest
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `external/local DNS resolver`.
