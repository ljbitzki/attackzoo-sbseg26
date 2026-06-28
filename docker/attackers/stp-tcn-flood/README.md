# Attack "STP TCN Flood"

> BPDU (Bridge Protocol Data Unit) packet flood with STP topology change information and random MAC addresses.

## Metadata

| Field | Value |
|---|---|
| ID | `net_stp_tcn_flood` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.1 L2/L3 |
| Image | `attack-stp-tcn-flood:latest` |
| Container | `attack-stp-tcn-flood` |
| Suggested max runtime | `10s` |
| Typical targets/services | `local network` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Parameters

This attack does not take parameters and operates at the local network level.

## Capture Warning

> This attack can generate a large amount of data if captured until its automatic completion. For demonstrations, use less than 5 seconds of execution.

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run net_stp_tcn_flood --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-stp-tcn-flood attack-stp-tcn-flood:latest
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `local network`.
