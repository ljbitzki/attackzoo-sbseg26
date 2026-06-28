# Containerized Attack Testbed: A Reproducible Approach for Generating Traffic Evidence

This repository contains **AttackZoo**, a Docker-based testbed for building and running controlled network, application, and IoT attack scenarios. The artifact automates target servers, benign clients, attack containers, traffic capture, feature extraction, dataset generation, and experiment reporting through both a command-line interface and a Streamlit UI.

The associated paper, "Containerized Attack Testbed: A Reproducible Approach for Generating Traffic Evidence," presents an environment for producing reproducible traffic evidence from parameterized Docker attacks. The artifact is intended to let reviewers inspect the testbed, run attacks in an isolated lab, capture PCAP files, and regenerate metrics and reports used to support the paper's claims.

## README Structure

This document is organized as follows:

1. Project summary and artifact scope.
2. Basic environment information, components, and requirements.
3. Dependencies and external resources used during installation.
4. Safety and isolation guidance.
5. Installation on a clean machine.
6. Minimal validation test.
7. Reproducible experiment claims.
8. Basic code and repository documentation.
9. Troubleshooting.
10. License.

## Artifact Badges Considered

The artifact is intended to support the following review badges:

- Artifacts Available.
- Artifacts Functional.
- Artifacts Sustainable.
- Experiments Reproducible.

## Basic Information

### Main Components

| Component | Location | Purpose |
| --- | --- | --- |
| Main CLI | `attackzoo.py` | Command-line entry point for listing, running, stopping, and inspecting attacks, captures, features, datasets, and experiments. |
| CLI parser and commands | `modules/attackzoo/` | Implementation of `status`, `list`, `run`, `stop`, `ps`, `logs`, `captures`, `features`, `dataset`, `experiment`, and `report`. |
| Dynamic attack catalog | `docker/attackers/*/attack.yaml` | Plug-and-play attack definitions loaded automatically by the tool. |
| Target servers | `docker/servers/` | Docker images for HTTP, SSH, SMB, MQTT, CoAP, XRCE-DDS, Zenoh, Telnet, and SSL/Heartbleed services. |
| Benign clients | `docker/clients/` | Containers that generate benign background traffic. |
| Web UI | `modules/tool.py` | Streamlit interface for interactive use. |
| Helper scripts | `setup.sh`, `build.sh`, `servers.sh`, `clients.sh`, `environment.sh` | Dependency installation, Docker image builds, server/client control, and Streamlit environment control. |
| Outputs | `captures/`, `features/`, `datasets/`, `experiments/`, `logs/` | Artifacts generated during runs and experiments. |

### Current Catalog

The current repository contains 60 attacks declared through `attack.yaml`, organized into the following categories:

| Category | Count |
| --- | ---: |
| `1) Reconnaissance and Discovery` | 9 |
| `2) Network Interception and Exploitation` | 8 |
| `3) Web Application Attacks` | 10 |
| `4) Brute Force Against Remote Access Applications` | 2 |
| `5) Exfiltration and Tunneling` | 2 |
| `6) Denial of Service and Impact` | 8 |
| `7) IoT` | 21 |

### Target Servers

| Server | Container | Host-exposed port(s) |
| --- | --- | --- |
| HTTP/DVWA | `server-http-server` | `8080/tcp -> 80/tcp` |
| SSH | `server-ssh-server` | `2222/tcp -> 22/tcp` |
| SMB/Samba | `server-smb-server` | `139/tcp`, `445/tcp`, `137/udp`, `138/udp` |
| MQTT/Mosquitto | `server-mqtt-broker` | `1883/tcp`, `9001/tcp` |
| CoAP | `server-coap-server` | `5683/tcp`, `5683/udp` |
| XRCE-DDS Agent | `server-xrce-dds-agent` | `8888/udp` |
| Zenoh Router | `server-zenoh-router` | `7447/tcp` |
| Telnet | `server-telnet-server` | `2323/tcp -> 23/tcp` |
| SSL/Heartbleed | `server-ssl-heartbleed` | `8443/tcp -> 443/tcp` |

The build script may also start Dozzle on `11080/tcp` to make Docker logs easier to inspect from a browser.

### Recommended Execution Environment

Environment used by the authors for local tests:

| Resource | Tested configuration |
| --- | --- |
| CPU | AMD Ryzen 5 5500X |
| Memory | 8 GB DDR4 |
| Storage | SSD |
| Operating system | Kubuntu 24.04 LTS |
| Python | Python 3.12 with `venv` |
| Docker | Docker Engine 29.2.1 |
| Optional virtualization | VirtualBox 7.1 |

Minimum recommended environment for review:

| Resource | Recommended minimum |
| --- | --- |
| Operating system | Ubuntu 24.04 LTS or a compatible Linux distribution with `apt`, Docker, and Python 3 |
| CPU | 4 vCPUs |
| Memory | 8 GB RAM for reduced tests; 16 GB for full experiment batches |
| Disk | 30 GB free for installation and images; 50 GB or more for PCAP captures and repeated experiments |
| Network | Isolated environment, preferably a VM or dedicated host without direct Internet exposure |

## Dependencies

### System Dependencies

`setup.sh` installs or configures the main dependencies on Ubuntu/Debian systems:

- `ca-certificates`
- `curl`
- `cmake`
- `git`
- `python3-venv`
- `tcpdump`
- `tshark`
- `wireshark`
- `redis`
- Docker Engine (`docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`, `docker-compose-plugin`)

The script also adds the current user to the `docker` group, configures capture permissions for `tcpdump`/`dumpcap`, creates `.venv/`, installs Python dependencies, and installs NTLFlowLyzer from GitHub.

### Python Dependencies

Direct dependencies from `requirements.txt`:

```text
streamlit>=1.36
pandas>=2.0
numpy>=1.20
matplotlib>=3.5
scapy>=2.5
pyyaml>=6.0
```

### External Resources Used During Installation

- The official Docker repository for Ubuntu.
- Operating-system package indexes.
- PyPI for Python packages.
- `https://github.com/ahlashkari/NTLFlowLyzer.git`.
- Base images and packages referenced by Dockerfiles under `docker/`.

No SSH keys, private credentials, API tokens, or cloud infrastructure are required to run the artifact.

## Safety Considerations

This artifact runs scanners, brute-force tools, fuzzers, floods, and other attack behaviors. Use it only in an environment that you own, isolate, and are authorized to test.

Safe review recommendations:

- Run the artifact in a VM or dedicated machine.
- Do not point attacks at external addresses, third-party networks, or services without explicit authorization.
- Prefer internal testbed targets, such as the `server-*` containers.
- Avoid exposing the host directly to the Internet during review.
- Check for port conflicts before starting servers.
- Use short durations for DoS/flood attacks during initial tests.
- Stop attack containers after validation with `python3 attackzoo.py stop <attack_id>` or `docker rm -f <container>`.

Ports that may be exposed on the host:

```text
TCP: 139, 445, 1883, 2222, 2323, 5683, 7447, 8080, 8443, 9001, 11080
UDP: 137, 138, 5683, 8888
```

Weak passwords and intentionally vulnerable configurations in the containers are disposable lab values. Do not reuse them anywhere else.

## Installation

The steps below assume a clean Ubuntu 24.04 LTS machine or an equivalent environment. Run all commands from the repository root.

### 1. Clone The Repository

```bash
git clone <REPOSITORY_URL>
cd sbseg26
```

If the artifact directory was already provided, enter its root:

```bash
cd /path/to/sbseg26
```

### 2. Install System And Python Dependencies

```bash
chmod +x setup.sh
./setup.sh
```

After installation, apply the new Docker group permission:

```bash
newgrp docker
```

Logging out and back in also applies the group change.

### 3. Build Images And Start Servers

```bash
chmod +x build.sh
./build.sh
```

This builds server, attacker, and client images, starts target servers, and prints container IP addresses. The first build depends on machine and network speed; on an SSD-backed machine with stable Internet access, reserve 20 to 60 minutes because many Docker images and packages are downloaded or compiled.

### 4. Activate The Python Environment

```bash
source .venv/bin/activate
```

### 5. Check The Installation

```bash
python3 attackzoo.py status
python3 attackzoo.py list
```

Expected `status` output:

```text
docker_available=true
```

If Docker is not accessible, check whether the service is running and whether Docker group permissions have been applied.

### 6. Control Servers And Clients

```bash
./servers.sh start
./servers.sh restart
./servers.sh stop

./clients.sh start all
./clients.sh restart random
./clients.sh stop super
```

`clients.sh` accepts `all`, `random`, or `super` as the target. The `client-random` container requires the standard HTTP, SSH, SMB, MQTT, CoAP, Telnet, and SSL/Heartbleed servers to be running. The `client-super` container can be directed with environment variables:

```bash
CLIENT_SUPER_SERVICE=mqtt
./clients.sh start super

CLIENT_SUPER_SERVICE=zenoh
CLIENT_SUPER_TOTAL=30
./clients.sh restart super

CLIENT_SUPER_TARGET_IP=172.17.0.2
CLIENT_SUPER_TARGET_PORT=443
./clients.sh start super
```

The scripts also accept the previous Portuguese aliases (`iniciar`, `reiniciar`, and `parar`) for compatibility.

To open the Streamlit interface directly:

```bash
source .venv/bin/activate
streamlit run modules/tool.py --theme.base="dark" --server.headless true
```

To restart the environment and Streamlit UI together:

```bash
./environment.sh restart
```

### 7. List The Full Catalog

```bash
python3 attackzoo.py list
python3 attackzoo.py list --json
python3 attackzoo.py list --category "IoT"
python3 attackzoo.py list --id dos_syn_flood
```

## Minimal Test

This section runs a short validation to confirm that the CLI loads the catalog, that target servers are active, and that a simple attack can be launched againstserverocal testbed.

### 1. Prepare The Session

```bash
cd /path/to/sbseg26
souserverenv/bin/activate
```

### 2. Confirm Docker And The Catalog

```bash
python3 attackzoo.py status
python3 attackzoo.py list --category "Denial"
```

Expected results:

- `docker_available=true`.
- A list of attacks from `6) Denial of Service and Impact`, including `dos_http_simple` andserversyn_flood`.

### 3. Confirm That The HTTP Server Is Active

```bash
./servers.sh start
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep server-http-server
curl -I http://127.0.0.1:8080/
```

Expected result:

- The `server-http-server` container is `Up`.
- The HTTP server responds through host port `8080`.

### 4. Run A Short HTTP Attack

Use the internal IP of the HTTP container and its internal port `80`:

```bash
HTTP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)
python3 attackzoo.py run dos_http_simple --target "$HTTP_IP" --port 80
```

Expected result:

```text
[OK] Container started: <container_id>
```

`dos_http_simple` is a one-shot attack: it sends a short burst of HTTP requests and exits on its own. To inspect active or previous attack containers:

```bash
python3 attackzoo.py ps
python3 attackzoo.py ps --all
```

### 5. Run A Short Baseline Experiment

This command validates the `experiment` workflow without launching a real attack by using only level `L0`:

```bash
python3 attackzoo.py experiment \
  --attack-id dos_http_simple \
  --out smoke_http \
  --runs 1 \
  --levels L0 \
  --warmup 3 \
  --attack 3 \
  --cooldown 3 \
  --probes http \
  --http-url http://127.0.0.1:8080/ \
  --iface lo \
  --bpf "tcp port 8080"
```

Expected outputs:

- `experiments/smoke_http/dos_http_simple/L0/run01/`.
- `probe_http.csv` with HTTP probe data.
- A `.pcap` file if `tcpdump` is installed and authorized.
- `experiments/smoke_http/reports/` with tables and figures when enough data is available.

Accepted availability probes for `--probes` are `http`, `https`, `ssh`, `smb`, `mqtt`, `coap`, `xrce`, `zenoh`, and `telnet`. Use `all` to enable all probes or `none` to disable them. For service-specific endpoints, repeat `--probe-endpoint`, for example `--probe-endpoint ssh=172.17.0.3:22`.

## Reproducible Experiment Claims

The claims below reflect the functionality implemented in this repository. If the final paper uses different numbering or titles, keep the commands and adjust only the claim labels.

### Claim 1: The Artifact Provides An Extensible Catalog Of Containerized Attacks

Goal: show that the tool automatically discovers attacks declared in `docker/attackers/*/attack.yaml`, groups them by category, and exposes execution parameters through the CLI.

Commands:

```bash
source .venv/bin/activate
python3 attackzoo.py list
python3 attackzoo.py list --json > /tmp/attackzoo-catalog.json
python3 -m json.tool /tmp/attackzoo-catalog.json > /tmp/attackzoo-catalog-formatted.json
```

To check the count:

```bash
python3 - <<'PY'
from modules.registry import CATEGORIES
print(sum(len(v) for v in CATEGORIES.values()), "attacks")
for category, attacks in CATEGORIES.items():
    print(f"{category}: {len(attacks)}")
PY
```

Expected time: less than 1 minute.

Expected resources: negligible CPU and memory. Docker does not need to be running for catalog serverg, but Python dependencies must be installed.

Expected result: 60 attacks loaded across 7 categories. The JSON outpserveruld contain `id`, `name`, `image`, `container`, `params`, `mitre`, and `max_runtime_s` for each attack.

### Claim 2: The Environment Runs Attacks Against Containerized Target Servers

Goal: demonstrate functional attack execution against services inside the testbed.

Preparation:

```bash
source .venv/bin/activate
./servers.sh start
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep server
```

HTTP example:

```bash
HTTP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)
python3 attackzoo.py run dos_http_simple --target "$HTTP_IP" --port 80
```

TCP reconnaissance example:

```bash
python3 attackzoo.py run recon_port_scanner_tcp --target "$HTTP_IP"
```

Continuous attack example, stopped manually:

```bash
python3 attackzoo.py run dos_syn_flood --target "$HTTP_IP" --port 80
python3 attackzoo.py ps
python3 attackzoo.py stop dos_syn_flood
```

Expected time: 1 to 5 minutes after images have already been built.

Expected resources: 1 to 2 vCPUs and up to 2 GB of additional RAM for short tests. Flood attacks may increase CPU and network usage; keep durations short.

Expected result: the CLI prints `[OK] Container started`, containers appear in `ps` while active, and servers remain manageable through `servers.sh`.

### Claim 3: The Artifact Generates Traffic Evidence, Features, And Datasets

Goal: demonstrate the PCAP capture, feature extraction, and dataset-generation pipeline from a controlled execution.

Short experiment with capture and extraction:

```bash
python3 attackzoo.py experiment \
  --attack-id dos_http_simple \
  --out http_features \
  --runs 1 \
  --levels L0 \
  --warmup 5 \
  --attack 5 \
  --cooldown 5 \
  --probes http \
  --http-url http://127.0.0.1:8080/ \
  --iface lo \
  --bpf "tcp port 8080" \
  --extract-features \
  --build-dataset \
  --tools-tshark \
  --tools-scapy
```

List captures:

```bash
python3 attackzoo.py captures
python3 attackzoo.py captures --latest --json
```

Extract features manually from an existing PCAP:

```bash
python3 attackzoo.py features --pcap <FILE.pcap> --tools tshark,scapy --outdir features/
python3 attackzoo.py dataset --pcap <FILE.pcap> --features-dir features --outdir datasets
```

Expected time: 1 to 10 minutes for short experiments. NTLFlowLyzer may take longer on large PCAP files.

Expected resources: disk use proportional to captured traffic. Short tests usually need less than 1 GB; full repetitions may require tens of GB.

Expected result:

servers under `experiments/http_features/.../*.pcap` or `captures/`.
- Features under `features/`.
- Dataset CSVs under `datasets/`.
- Per-run metadata in `meta.json`.

### Claim 4: The Artifact Reproduces Warmup-Attack-Cooldown Batches And T3-T8 Reports

Goal: reproduce the tool's experimental organization with warmup, attack, and cooldown phases, availability probes, and consolidated reports.serverple with an HTTP attack and hooks:

```bash

HTTP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)

python3 attackzoo.py experiment \
  --attack-id dos_http_simple \
  --out paper_http \
  --service http \
  --runs 3 \
  --levels L0,L1 \
  --warmup 30 \
  --attack 60 \
  --cooldown 30 \
  --probes http \
  --http-url http://127.0.0.1:8080/ \
  --host "$HTTP_IP" \
  --port 80 \
  --iface docker0 \
  --bpf "tcp port 80 or tcp port 8080" \
  --collect-resources \
  --server server-http-server \
  --attack-start-hook "python3 attackzoo.py run dos_http_simple --target {host} --port {port}" \
  --attack-stop-hook "python3 attackzoo.py stop dos_http_simple"
```

Regenerate reports from collected data:

```bash
python3 attackzoo.py report \
  --input experiments/paper_http/ \
  --warmup 30 \
  --attack 60 \
  --cooldown 30
```

Expected time: approximately `(warmup + attack + cooldown) * runs * levels`, plus post-processing. The example above takes about 12 minutes before report generation.

Expected resources: 4 vCPUs, 8 GB RAM, and a few GB of free space for PCAPs/CSVs. Increase disk and memory for more levels, more repetitions, or higher-intensity attacks.

Expected result:

```text
experiments/paper_http/
  dos_http_simple/
    L0/run01/
    L0/run02/
    L0/run03/
    L1/run01/
    L1/run02/
    L1/run03/
  reports/
    figs/
    tables/
```

Expected files include `probe_<service>.csv` (for example, `probe_http.csv`), `resource.csv`, `server_stats.csv`, `meta.json`, PCAP files, and tables/figures summarizing availability, resources, stability, and reexecution.

### Claim 5: New Attacks Can Be Added Without Changing Python Code

Goal: demonstrate catalog sustainability and extensibility through YAML files.

Steps:

1. Create a directory under `docker/attackers/<new-attack>/`.
2. Add `Dockerfile`, `entrypoint.sh`, `README.md`, and `attack.yaml`.
3. Declare fields such as `id`, `name`, `category`, `image`, `container_name`, `target_mapping`, `params`, and `max_runtime_s` in `attack.yaml`.
4. Build the Docker image.
5. Run `python3 attackzoo.py list --id <attack_id>`.

Minimal `attack.yaml` example:

```yaml
id: example_ping
name: Example Ping
category: 1) Reconnaissance and Discovery
description: Example attack used to validate dynamic discovery.
image: attack-example-ping:latest
container_name: attack-example-ping
max_runtime_s: 10
target_mapping:
  target: target_ip
params:
  - key: target_ip
    label: Target IP address or FQDN
    kind: ip
    placeholder: __HOST_IP__
```

Expeserverime: less than 5 minutes for a simple attack, plus Docker image build time.

Expected result: the new attack appears in the CLI without editing `modules/registry.py`, `modules/loader.py`, or any other Python file.

## Basic Documentation

### Repository Layout

```text
.
|-- attackzoo.py                  # Main CLI
|-- setup.sh                      # System/Python dependency installation
|-- build.sh                      # Docker image build and server startup wrapper
|-- servers.sh                    # Control script for server-* containers
|-- clients.sh                    # Control script for client-* containers
|-- environment.sh                # Streamlit/environment helper
|-- requirements.txt              # Python dependencies
|-- modules/
|   |-- tool.py                   # Streamlit UI
|   |-- loader.py                 # Dynamic attack.yaml discovery
|   |-- registry.py               # AttackSpec/ParamSpec dataclasses and loaded catalog
|   |-- runners.py                # Docker wrappers
|   |-- features.py               # PCAP feature extraction
|   |-- datasets.py               # CSV dataset generation
|   `-- attackzoo/
|       |-- parser.py             # argparse parser
|       |-- commands.py           # Main subcommands
|       |-- experiment.py         # Experiment orchestration
|       |-- capture.py            # tcpdump capture
|       |-- probes.py             # HTTP/MQTT/etc. probes
|       |-- telemetry.py          # Host resources and docker stats
|       `-- reports/              # Availability, stability, and resource reports
|-- docker/
|   |-- build-images.sh           # Builds servers, attackers, and clients
|   |-- attackers/                # One subdirectory per attack
|   |-- servers/                  # Target server Dockerfiles and YAMLs
|   `-- clients/                  # Benign client Dockerfiles and YAMLs
|-- hooks/
|   |-- attack_start.sh           # Attack-window start hook helper
|   `-- attack_stop.sh            # Attack-window stop hook helper
|-- logs/                         # Runtime logs
|-- contrib/docs/                 # Additional artifact-review documentation
`-- LICENSE                       # BSD 3-Clause License
```

### Main CLI

```bash
python3 attackzoo.py --help
python3 attackzoo.py status
python3 attackzoo.py list [--category TEXT] [--id ID] [--json]
python3 attackzoo.py run <attack_id> [--target IP_OR_HOST] [--port PORT] [--duration N] [--rate N]
python3 attackzoo.py stop <attack_id>
python3 attackzoo.py ps [--all] [--json]
python3 attackzoo.py logs <attack_id> [--tail N]
python3 attackzoo.py captures [--latest] [--json]
python3 attackzoo.py features --pcap FILE [--tools LIST] [--outdir DIR]
python3 attackzoo.py dataset --pcap FILE [--features-dir DIR] [--outdir DIR]
python3 attackzoo.py experiment --attack-id ID --out DIR [options]
python3 attackzoo.py report --input DIR --warmup N --attack N --cooldown N [--outdir DIR]
```

### Summary Of The `attack.yaml` Schema

| Field | Required | Description |
| --- | --- | --- |
| `id` | yes | Unique attack identifier used by the CLI. |
| `name` | yes | Human-readable name displayed in the UI/CLI. |
| `category` | yes | Category used to group the attack. |
| `description` | no | Attack behavior description. |
| `image` | yes | Docker image used by `docker run`. |
| `container_name` | yes | Attacker container name. |
| `max_runtime_s` | no | Suggested default duration for the UI. |
| `target_mapping` | no | Maps CLI aliases such as `target` and `port` to real parameters. |
| `mitre` | no | Related MITRE technique/tactic URLs. |
| `params` | no | Ordered list of parameters passed to `entrypoint.sh`. |

Fields for each item in `params`:

| Field | Required | Description |
| --- | --- | --- |
| `key` | yes | Internal parameter name. |
| `label` | yes | User-facing label. |
| `kind` | yes | Type: `ip`, `port`, `cidr`, `int`, `float`, or `text`. |
| `placeholder` | no | UI/documentation example. |
| `default` | no | Default value; makes the parameter optional in the CLI. |
| `validate` | no | Custom validation regex. |

## Troubleshooting

### `docker_available=false`

Check that Docker is installed, running, and accessible by your user:

```bash
sudo systemctl status docker
newgrp docker
docker version
python3 attackzoo.py status
```

### Port Already In Use

If a server fails with a bind error, identify the local process:

```bash
sudo ss -tulpn | grep -E ':8080|:1883|:2222|:2323|:5683|:8443|:7447|:9001|:11080'
```

Stop the conflicting service or change the port mapping in the corresponding script/YAML.

### Misserverocker Image

If the CLI reports that an image cannot be found:

```bash
cd docker
./build-images.sh
cd ..
```

Or run the wrapper again:

```bash
./build.sh
```

### Packet Capture Permission Problems

If PCAP files are not generated, confirm `tcpdump` and capabilities:

```bash
which tcpdump
getcap "$(command -v tcpdump)"
sudo setcap cap_net_raw,cap_net_admin=eip "$(command -v tcpdump)"
```

### Servers Stopped After Reboot

```bash
./servers.sh start
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep server
```

## License

This project is licensed under the BSD 3-Clause License. See `LICENSE` in the repository root for the full terms.
