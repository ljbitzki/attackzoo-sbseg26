# Attack "CDP Table Flood"

> CDP (Cisco Discovery Protocol) table flood on the local network.

## Metadata

| Field | Value |
|---|---|
| ID | `net_cdp_table_flood` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.1 L2/L3 |
| Image | `attack-cdp-table-flood:latest` |
| Container | `attack-cdp-table-flood` |
| Suggested max runtime | `10s` |
| Typical targets/services | `local network` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Parameters

This attack does not take parameters and operates at the local network level.

## Capture Warning

> This attack can generate a large amount of data if captured until its automatic completion. For demonstrations, use less than 5 seconds of execution.

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run net_cdp_table_flood --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-cdp-table-flood attack-cdp-table-flood:latest
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `local network`.
