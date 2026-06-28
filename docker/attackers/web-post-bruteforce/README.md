# Attack "Web POST Bruteforce"

> Web application POST authentication brute force using a wordlist.

## Metadata

| Field | Value |
|---|---|
| ID | `web_post_bruteforce` |
| Category | 3) Web Application Attacks |
| Subcategory | 3.1 General Web |
| Image | `attack-web-post-bruteforce:latest` |
| Container | `attack-web-post-bruteforce` |
| Suggested max runtime | `10s` |
| Typical targets/services | `http-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/)<br>[https://attack.mitre.org/techniques/T1110/](https://attack.mitre.org/techniques/T1110/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |
| `--target_port` | `port` | no | `8080` | Target port |

## Capture Warning

> This attack can generate a large amount of data if captured until its automatic completion. For demonstrations, use less than 5 seconds of execution.

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run web_post_bruteforce --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-web-post-bruteforce attack-web-post-bruteforce:latest "<TARGET_IP>" "8080"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `http-server`.
