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

This attack does not require a target and operates at the local network level. Intensity parameters bound unattended campaign runs.

## Intensity Parameters

| Parameter | Default | Effect |
|---|---:|---|
| `active_s` | `5` | Maximum time spent running the MLD flood binary inside the attack window. |
| `nice_level` | `10` | Positive `nice(1)` adjustment used to reduce scheduler pressure from the flood process. |
| `duration_s` |  | Upper bound injected by `attackzoo.py run --duration`; the entrypoint uses the lower value between `active_s` and `duration_s` when both are set. |

## Capture Warning

> The launcher is intentionally capped for campaign safety. The current binary does not expose packet-rate control, so active_s bounds generation time.

## Campaign Safety Notes

The available campaign artifacts show completed L1/L2 MLD runs producing roughly 0.7-0.9 GB of raw PCAP data per run, while L3 did not complete. Unlike the `yersinia` launchers, this attack does not create thousands of processes; the risk is sustained unbounded packet generation from the binary. The current defaults cap active generation at 5 seconds and run the process with `nice -n 10`.

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run net_ipv6_mld_flood --duration 20
python3 attackzoo.py run net_ipv6_mld_flood --duration 20 --active-s 3 --nice-level 10
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-ipv6-mld-flood \
  -e ACTIVE_S=5 -e NICE_LEVEL=10 \
  attack-ipv6-mld-flood:latest
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `local IPv6 network`.
