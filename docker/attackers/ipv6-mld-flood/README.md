# Attack "IPv6 MLD Flood"

> ICMPv6 Multicast Listener Report MLD (131) flood on the local network.

## Metadata

| Field | Value |
|---|---|
| ID | `net_ipv6_mld_flood` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.2 IPv6 |
| Image | `attack-ipv6-mld-flood:latest` |
| Container | `attack-ipv6-mld-flood` |
| Suggested max runtime | `10s` |
| Typical targets/services | `local IPv6 network` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Parameters

This attack does not take parameters and operates at the local network level.

## Capture Warning

> This attack can generate a large amount of data if captured until its automatic completion. For demonstrations, use less than 5 seconds of execution.

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run net_ipv6_mld_flood --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-ipv6-mld-flood attack-ipv6-mld-flood:latest
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `local IPv6 network`.
