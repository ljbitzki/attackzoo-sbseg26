# Server "MQTT Broker"

> Act as an MQTT broker for publishing, brute force, LWT abuse, and QoS amplification in IoT experiments.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `mqtt-broker` |
| Role | target-server |
| Image | `server-mqtt-broker:latest` |
| Container | `server-mqtt-broker` |
| Base | `eclipse-mosquitto:2` |
| Service | Eclipse Mosquitto MQTT broker |
| Protocols | `mqtt`, `websocket` |
| Internal ports | `1883/tcp`, `9001/tcp` |
| Published ports | `1883:1883/tcp`, `9001:9001/tcp` |

## Execution

```bash
docker run -d --rm --name server-mqtt-broker -p 1883:1883 -p 9001:9001 server-mqtt-broker:latest
```

## Container IP

```bash
docker container inspect server-mqtt-broker --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-mqtt-broker
```

## Related Attacks

- `iot_mqtt_bruteforce`
- `iot_mqtt_publisher`
- `iot_mqtt_lwt_abuse`
- `iot_mqtt_qos_amplification`

## Related Benign Clients

- `client-random:mqtt`
- `client-super:mqtt`

## Testbed Observability

- MQTT CONNECT/PUBLISH/SUBSCRIBE
- Mosquitto logs
- optional telemetry through docker stats

In controlled experiments, use `python3 attackzoo.py experiment --server server-mqtt-broker` to associate target-container telemetry with execution artifacts.
