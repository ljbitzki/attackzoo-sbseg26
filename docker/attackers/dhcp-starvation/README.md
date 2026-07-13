# Attack "DHCP Starvation"

> DHCP lease exhaustion on the local network.

## Metadata

| Field | Value |
|---|---|
| ID | `net_dhcp_starvation` |
| Category | 2) Network Interception and Exploitation |
| Subcategory | 2.1 L2/L3 |
| Image | `attack-dhcp-starvation:latest` |
| Container | `attack-dhcp-starvation` |
| Suggested max runtime | `10s` |
| Typical targets/services | `local network` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Parameters

This attack does not require a target and operates at the local network level. Intensity parameters bound unattended campaign runs.

## Intensity Parameters

| Parameter | Default | Effect |
|---|---:|---|
| `active_s` | `5` | Maximum time spent generating DHCP starvation traffic inside the attack window. |
| `duration_s` |  | Upper bound injected by `attackzoo.py run --duration`; the entrypoint uses the lower value between `active_s` and `duration_s` when both are set. |
| `count` | `1` | Number of concurrent `yersinia` worker processes. |
| `delay_ms` | `1000` | Delay between worker starts. |

## Capture Warning

> The launcher is intentionally capped for campaign safety. Increase count or active_s only after validating host load, DHCP state churn, and capture volume.

## Campaign Safety Notes

The previous launcher started 1000 `yersinia dhcp` processes at once. In the partially completed campaign, one interrupted L1 run produced approximately 70 GB of raw PCAP data and the observed 1-minute load average exceeded 50. The current defaults use one worker, a 5-second active generation cap, and a 1-second worker-start delay to make unattended execution less likely to trigger the load kill-switch.

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run net_dhcp_starvation --duration 20
python3 attackzoo.py run net_dhcp_starvation --duration 20 --active-s 3 --count 1 --delay-ms 1000
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-dhcp-starvation \
  -e ACTIVE_S=5 -e COUNT=1 -e DELAY_MS=1000 \
  attack-dhcp-starvation:latest
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `local network`.
