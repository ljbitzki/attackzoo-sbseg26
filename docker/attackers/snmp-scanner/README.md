# Attack "SNMP Scanner"

> SNMP scan across all hosts in a network using a community-string wordlist.

## Metadata

| Field | Value |
|---|---|
| ID | `recon_snmp_scanner` |
| Category | 1) Reconnaissance and Discovery |
| Subcategory | 1.2 Port, service, OS, and vulnerability scanning |
| Image | `attack-snmp-scanner:latest` |
| Container | `attack-snmp-scanner` |
| Suggested max runtime | `10s` |
| Typical targets/services | `target IP service` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run recon_snmp_scanner --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-snmp-scanner attack-snmp-scanner:latest "<TARGET_IP>"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `target IP service`.
