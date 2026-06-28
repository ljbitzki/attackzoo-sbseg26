# Random Client

> Generate continuous benign noise during experiments by randomly choosing among supported protocol clients.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `client-random` |
| Role | benign-client |
| Image | `client-random:latest` |
| Container pattern | `client-random-<N>` |
| Base | `ubuntu:24.04` |
| Entrypoint | `/tmp/clients.sh` |
| Protocols | `http`, `https`, `ssh`, `smb`, `mqtt`, `coap`, `telnet` |

## Parameters

| Parameter |
|---|
| `WEB_SERVER` |
| `SSH_SERVER` |
| `SMB_SERVER` |
| `MQTT_SERVER` |
| `COAP_SERVER` |
| `TELNET_SERVER` |
| `SSL_SERVER` |

## Execution

Recommended from the repository root:

```bash
./clients.sh start random
./clients.sh stop random
```

Direct container execution:

```bash
docker run -d --rm --name client-random-1 client-random:latest <WEB_IP> <SSH_IP> <SMB_IP> <MQTT_IP> <COAP_IP> <TELNET_IP> <SSL_IP>
```

## Typical Target Services

- `http-server`: HTTP / DVWA Server
- `ssh-server`: SSH Server
- `smb-server`: SMB / Samba Server
- `mqtt-broker`: MQTT Broker
- `coap-server`: CoAP Server
- `telnet-server`: Telnet Server
- `ssl-heartbleed`: HTTPS Heartbleed Server

## Testbed Observability

- stdout with the selected service
- mixed benign traffic in PCAP
- random time spacing between requests

## Notes

- Infinite loop; use docker rm -f on the container to stop it.
- Does not cover XRCE-DDS or Zenoh; use `client-super` for those protocols.

Use these clients to generate benign traffic before, during, or after the attack window in controlled experiments. Container logs report performed attempts and help correlate benign traffic with captured PCAP files.
