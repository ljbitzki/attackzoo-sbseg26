# Attack "ICMP Tunnel"

> TCP port 22 (SSH) tunnel over ICMP (pings).

## Metadata

| Field | Value |
|---|---|
| ID | `exf_icmp_tunnel` |
| Category | 5) Exfiltration and Tunneling |
| Subcategory | 5.1 Exfiltration and Tunneling |
| Image | `attack-icmp-tunnel:latest` |
| Container | `attack-icmp-tunnel` |
| Suggested max runtime | `10s` |
| Typical targets/services | `ssh-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/tactics/TA0011/](https://attack.mitre.org/tactics/TA0011/)<br>[https://attack.mitre.org/techniques/T1572/](https://attack.mitre.org/techniques/T1572/)<br>[https://attack.mitre.org/techniques/T1095/](https://attack.mitre.org/techniques/T1095/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `2222` | Target port |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run exf_icmp_tunnel --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-icmp-tunnel attack-icmp-tunnel:latest "<TARGET_IP>" "2222"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `ssh-server`.
