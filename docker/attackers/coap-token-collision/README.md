# Attack "CoAP Token Collision"

> Burst of CoAP messages that forces token reuse or collisions to degrade target state tracking and transaction correlation.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_coap_token_collision` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / CoAP |
| Image | `attack-coap-token-collision:latest` |
| Container | `attack-coap-token-collision` |
| Suggested max runtime | `10s` |
| Typical targets/services | `coap-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `5683` | Target port |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_coap_token_collision --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-coap-token-collision attack-coap-token-collision:latest "<TARGET_IP>" "5683"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `coap-server`.
