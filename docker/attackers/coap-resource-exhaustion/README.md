# Attack "CoAP Resource Discovery Exhaustion"

> Burst of CoAP resource discovery/mapping messages, typically against /.well-known/core, intended to exhaust target resources.

## Metadata

| Field | Value |
|---|---|
| ID | `iot_coap_resource_exhaustion` |
| Category | 7) IoT |
| Subcategory | 7.1 IoT Protocols / CoAP |
| Image | `attack-coap-resource-exhaustion:latest` |
| Container | `attack-coap-resource-exhaustion` |
| Suggested max runtime | `10s` |
| Typical targets/services | `coap-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/003/](https://attack.mitre.org/techniques/T1595/003/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `5683` | Target port |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run iot_coap_resource_exhaustion --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-coap-resource-exhaustion attack-coap-resource-exhaustion:latest "<TARGET_IP>" "5683"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `coap-server`.
