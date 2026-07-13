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

This attack does not require a target and operates at the local network level. Intensity parameters bound unattended campaign runs.

## Intensity Parameters

| Parameter | Default | Effect |
|---|---:|---|
| `active_s` | `5` | Maximum time spent generating CDP flood traffic inside the attack window. |
| `duration_s` |  | Upper bound injected by `attackzoo.py run --duration`; the entrypoint uses the lower value between `active_s` and `duration_s` when both are set. |
| `count` | `1` | Number of concurrent `yersinia` worker processes. |
| `delay_ms` | `500` | Delay between worker starts. |

## Capture Warning

> The launcher is intentionally capped for campaign safety. Increase count or active_s only after validating host load and capture volume.

## Campaign Safety Notes

The previous launcher started 2000 `yersinia cdp` processes at once. In the partially completed campaign, one interrupted L1 run produced approximately 76 GB of raw PCAP data before the load guardrail stopped the experiment. The current defaults start one worker for at most 5 seconds, preserving representative CDP flood traffic without creating an unbounded process burst.

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run net_cdp_table_flood --duration 20
python3 attackzoo.py run net_cdp_table_flood --duration 20 --active-s 3 --count 1 --delay-ms 500
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-cdp-table-flood \
  -e ACTIVE_S=5 -e COUNT=1 -e DELAY_MS=500 \
  attack-cdp-table-flood:latest
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `local network`.
