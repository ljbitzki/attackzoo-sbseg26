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
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Parameters

This attack does not require a target and operates at the local network level. Intensity parameters bound unattended campaign runs.

## Intensity Parameters

| Parameter | Default | Effect |
|---|---:|---|
| `active_s` | `5` | Maximum time spent generating STP TCN flood traffic inside the attack window. |
| `duration_s` |  | Upper bound injected by `attackzoo.py run --duration`; the entrypoint uses the lower value between `active_s` and `duration_s` when both are set. |
| `count` | `1` | Number of concurrent `yersinia` worker processes. |
| `delay_ms` | `500` | Delay between worker starts. |

## Capture Warning

> The launcher is intentionally capped for campaign safety. Increase count or active_s only after validating host load and capture volume.

## Campaign Safety Notes

The previous launcher started 2000 `yersinia stp -attack 3` processes at once. In the partially completed campaign, one interrupted L1 run produced approximately 43 GB of raw PCAP data and the observed 1-minute load average exceeded 60. The current defaults start one worker for at most 5 seconds, avoiding the process burst that previously tripped the load kill-switch.

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run net_stp_tcn_flood --duration 20
python3 attackzoo.py run net_stp_tcn_flood --duration 20 --active-s 3 --count 1 --delay-ms 500
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-stp-tcn-flood \
  -e ACTIVE_S=5 -e COUNT=1 -e DELAY_MS=500 \
  attack-stp-tcn-flood:latest
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `local network`.
