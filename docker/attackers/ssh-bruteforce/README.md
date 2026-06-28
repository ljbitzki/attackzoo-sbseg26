# Attack "SSH Bruteforce"

> SSH authentication brute force.

## Metadata

| Field | Value |
|---|---|
| ID | `bf_ssh` |
| Category | 4) Brute Force Against Remote Access Applications |
| Subcategory | 4.1 Brute Force |
| Image | `attack-ssh-bruteforce:latest` |
| Container | `attack-ssh-bruteforce` |
| Suggested max runtime | `10s` |
| Typical targets/services | `ssh-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `2222` | Target port |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run bf_ssh --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-ssh-bruteforce attack-ssh-bruteforce:latest "<TARGET_IP>" "2222"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `ssh-server`.
