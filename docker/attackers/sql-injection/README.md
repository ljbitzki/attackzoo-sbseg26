# Attack "SQL Injection"

> SQL injection exploitation tests.

## Metadata

| Field | Value |
|---|---|
| ID | `web_sql_injection` |
| Category | 3) Web Application Attacks |
| Subcategory | 3.1 General Web |
| Image | `attack-sql-injection:latest` |
| Container | `attack-sql-injection` |
| Suggested max runtime | `10s` |
| Typical targets/services | `http-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `8080` | Target port |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run web_sql_injection --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-sql-injection attack-sql-injection:latest "<TARGET_IP>" "8080"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `http-server`.
