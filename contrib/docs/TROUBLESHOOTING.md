# Troubleshooting

This document collects non-essential operational troubleshooting notes for AttackZoo.
For the main installation and validation workflow, see the root `README.md`.

## Docker Is Not Running Or Not Available

Check that Docker is installed, running, and accessible by your user:

```bash
sudo systemctl status docker
newgrp docker
docker version
python3 attackzoo.py status
```

## Port Already In Use

If a server fails with a bind error, identify the local process:

```bash
sudo ss -tulpn | grep -E ':8080|:1883|:2222|:2323|:5683|:8443|:7447|:9001|:11080'
```

Stop the conflicting service or change the port mapping in the corresponding script/YAML.

## Missing Docker Image

If the CLI reports that an image cannot be found:

```bash
cd /path/to/attackzoo-sbseg26/docker/
./build-images.sh full
```

Or run the wrapper again:

```bash
cd /path/to/attackzoo-sbseg26/
./build.sh full
```

## Packet Capture Permission Problems

If PCAP files are not generated, confirm `tcpdump` and capabilities:

```bash
which tcpdump
getcap "$(command -v tcpdump)"
sudo setcap cap_net_raw,cap_net_admin=eip "$(command -v tcpdump)"
```

## Servers Stopped After Reboot

```bash
cd /path/to/attackzoo-sbseg26/
./servers.sh start
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep server
```

>[!IMPORTANT]
> If you installed the reduced version, pass `redux` as the second argument to `servers.sh`:
> `./servers.sh start redux`
