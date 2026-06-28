# Attack "CoAP Response Fuzzing"

> Burst of randomized or mutated CoAP messages intended to trigger errors, exceptions, or crashes on the target.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_coap_response_fuzz` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / CoAP |
| Image | `attack-coap-response-fuzz:latest` |
| Container | `attack-coap-response-fuzz` |
| Suggested max runtime | `10s` |
| Typical targets/services | `coap-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/004/](https://attack.mitre.org/techniques/T1499/004/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `5683` | Target port |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_coap_response_fuzz --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-coap-response-fuzz attack-coap-response-fuzz:latest "<TARGET_IP>" "5683"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `coap-server`.
