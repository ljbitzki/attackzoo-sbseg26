# Super Client / Multiprotocol

> Generate controlled benign traffic with count, interval, and duration defined by parameters.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `client-super` |
| Role | benign-client |
| Image | `client-super:latest` |
| Container pattern | `client-super-<N>` |
| Base | `ubuntu:24.04` |
| Entrypoint | `python3 /tmp/super-client.py` |
| Protocols | `http`, `https`, `smb`, `ssh`, `rdp`, `telnet`, `smtp`, `imap`, `pop3`, `ftp`, `dns`, `snmp`, `sip`, `coap`, `mqtt`, `zenoh`, `xrce-dds` |

## Parameters

| Parameter |
|---|
| `service` |
| `ip` |
| `port|0` |
| `count` |
| `interval_s` |
| `total_time_s` |

## Execution

Recommended from the repository root:

```bash
CLIENT_SUPER_SERVICE=web ./clients.sh start super
CLIENT_SUPER_SERVICE=mqtt CLIENT_SUPER_TOTAL=30 ./clients.sh restart super
./clients.sh stop super
```

Direct container execution:

```bash
docker run --rm --name client-super-1 client-super:latest web 172.17.0.2 80 10 1 15
```

## Typical Target Services

- `http-server`: HTTP / DVWA Server
- `ssh-server`: SSH Server
- `smb-server`: SMB / Samba Server
- `mqtt-broker`: MQTT Broker
- `coap-server`: CoAP Server
- `telnet-server`: Telnet Server
- `ssl-heartbleed`: HTTPS Heartbleed Server
- `xrce-dds-agent`: Micro XRCE-DDS Agent
- `zenoh-router`: Zenoh Router

## Testbed Observability

- stdout with attempts, success/failure, and elapsed time
- per-protocol traffic in PCAP
- fine-grained benign load control

## Accepted Services

`http`, `https`, `smb`, `ssh`, `rdp`, `telnet`, `smtp`, `imap`, `pop3`, `ftp`, `dns`, `snmp`, `sip`, `coap`, `mqtt`, `zenoh`, `zenoh-pico`, `xrce-dds`, `uxrce-dds`.

When the provided port is `0`, the client uses the known default port for the service.

Use these clients to generate benign traffic before, during, or after the attack window in controlled experiments. Container logs report performed attempts and help correlate benign traffic with captured PCAP files.
