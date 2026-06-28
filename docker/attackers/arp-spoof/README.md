# Attack "ARP Spoof"

> Network gateway interception attack through ARP spoofing.

## Metadata

| Field | Value |
|---|---|
| ID | `net_arp_spoof` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.1 L2/L3 |
| Image | `attack-arp-spoof:latest` |
| Container | `attack-arp-spoof` |
| Suggested max runtime | `10s` |
| Typical targets/services | `local network` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/tactics/TA0009/](https://attack.mitre.org/tactics/TA0009/)<br>[https://attack.mitre.org/techniques/T1557/](https://attack.mitre.org/techniques/T1557/)<br>[https://attack.mitre.org/techniques/T1557/002/](https://attack.mitre.org/techniques/T1557/002/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--spoof_gw` | `ip` | yes | `192.168.0.1` | Spoofed Gateway |
| `--target_net` | `cidr` | yes | `192.168.0.0/24` | Target network |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run net_arp_spoof --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-arp-spoof attack-arp-spoof:latest "192.168.0.1" "192.168.0.0/24"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `local network`.
