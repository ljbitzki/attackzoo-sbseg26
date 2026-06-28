# Attack "SMB Enumerating"

> Enumeration of SMB share directories and vulnerabilities.

## Metadata

| Field | Value |
|---|---|
| ID | `recon_smb_enum` |
| Category | 1) Reconnaissance and Discovery |
| Subcategory | 1.2 Port, service, OS, and vulnerability scanning |
| Image | `attack-smb-enumerating:latest` |
| Container | `attack-smb-enumerating` |
| Suggested max runtime | `10s` |
| Typical targets/services | `target IP service` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1135/](https://attack.mitre.org/techniques/T1135/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run recon_smb_enum --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-smb-enumerating attack-smb-enumerating:latest "<TARGET_IP>"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `target IP service`.
