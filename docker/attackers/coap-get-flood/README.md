# Attack "CoAP GET Flood"

> Burst of CoAP GET requests against the target CoAP/IoT service to overload the application layer.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_coap_get_flood` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / CoAP |
| Image | `attack-coap-get-flood:latest` |
| Container | `attack-coap-get-flood` |
| Suggested max runtime | `10s` |
| Typical targets/services | `coap-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `5683` | Target port |

## Intensity Parameters

| Parameter | Default |
|---|---|
| `duration_s` |  |
| `count` | `1000` |
| `delay_ms` |  |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_coap_get_flood --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-coap-get-flood attack-coap-get-flood:latest "<TARGET_IP>" "5683"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `coap-server`.
