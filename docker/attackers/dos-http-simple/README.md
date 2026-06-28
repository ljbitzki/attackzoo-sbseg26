# Attack "DoS HTTP Simple"

> Simple HTTP application DoS.

## Metadata

| Field | Value |
|---|---|
| ID | `dos_http_simple` |
| Category | 6) Denial of Service and Impact |
| Subcategory | 6.2 Application-layer DoS |
| Image | `attack-dos-http-simple:latest` |
| Container | `attack-dos-http-simple` |
| Suggested max runtime | `10s` |
| Typical targets/services | `http-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `8080` | Target port |

## Intensity Parameters

| Parameter | Default |
|---|---|
| `duration_s` |  |
| `count` | `200` |
| `concurrency` | `50` |
| `delay_ms` | `100` |
| `payload_size` | `16` |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run dos_http_simple --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-dos-http-simple attack-dos-http-simple:latest "<TARGET_IP>" "8080"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `http-server`.
