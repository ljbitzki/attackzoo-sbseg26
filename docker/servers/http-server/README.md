# Server "HTTP / DVWA Server"

> Provide a vulnerable web application for web attacks, scanners, enumeration, and controlled HTTP DoS.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `http-server` |
| Role | target-server |
| Image | `server-http-server:latest` |
| Container | `server-http-server` |
| Base | `vulnerables/web-dvwa` |
| Service | HTTP with Damn Vulnerable Web Application (DVWA) |
| Protocols | `http` |
| Internal ports | `80/tcp` |
| Published ports | `8080:80/tcp` |

## Execution

```bash
docker run -d --rm --name server-http-server -p 8080:80 server-http-server:latest
```

## Container IP

```bash
docker container inspect server-http-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker exec -it server-http-server cat /var/log/messages
```

## Related Attacks

- `web_sql_injection`
- `web_dir_enumeration`
- `web_idor_path_traversal`
- `web_idor_url_parameter`
- `php_lfi_enumeration`
- `web_post_bruteforce`
- `web_simple_scanner`
- `web_wide_scanner`
- `web_xss_scanner`
- `dos_http_simple`
- `dos_http_slowloris`

## Related Benign Clients

- `client-random:web`
- `client-super:http`
- `client-super:https`

## Testbed Observability

- HTTP traffic in PCAP
- HTTP response codes through probes
- internal logs in /var/log/messages

In controlled experiments, use `python3 attackzoo.py experiment --server server-http-server` to associate target-container telemetry with execution artifacts.
