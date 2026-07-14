<p align="center">
  <img src="./contrib/assets/attackzoo.png" width="666"/>
</p>
<p align="center">
  <a href="https://www.linux.org/"><img src="https://img.shields.io/badge/Linux-8d2b01?logo=Linux&logoColor=white" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-7ed321?logo=python&logoColor=white" /></a>
  <a href="https://docker.com/"><img src="https://img.shields.io/badge/Docker-257bd6?logo=docker&logoColor=white" /></a>
  <a href="https://www.sbseg2026.uff.br/chamadas/sf/"><img src="https://img.shields.io/badge/SBSeg2026-SF-blue" /></a>
  <img src="https://img.shields.io/badge/SeloD-41824a" /></a>
  <img src="https://img.shields.io/badge/SeloF-5b9de3" /></a>
  <img src="https://img.shields.io/badge/SeloS-d34e55" /></a>
  <img src="https://img.shields.io/badge/SeloR-e8aa3f" /></a>
  <a href="https://opensource.org/license/bsd-3-clause"><img src="https://img.shields.io/badge/BSD-License-003001.svg" /></a>
</p>

# AttackZoo: A Reproducible Testbed for Attack Execution and Network Traffic Datasets Generation

This repository contains **AttackZoo**, a Docker-based testbed for building and running controlled network, application, and IoT attack scenarios. The artifact automates target servers, benign clients, attack containers, traffic capture, feature extraction, dataset generation, and experiment reporting through both a command-line (CLI) interface and an optional Streamlit Web UI.

The associated paper, `"AttackZoo: A Reproducible Testbed for Attack Execution and Network Traffic Datasets Generation"` presents an environment for producing reproducible traffic evidence from parameterized Docker attacks. The artifact is intended to let reviewers inspect the testbed, run attacks in an isolated lab, capture PCAP files, extract traffic features, generate datasets, telemetry metrics, reports, charts and experimental campaigns metadata.

**Paper abstract**: _The recurring generation of network traffic datasets for cybersecurity research is constrained by fragmented experimental workflows, limited reproducibility, and restricted coverage of attack vectors. This paper presents AttackZoo, a reproducible testbed that integrates a containerized repository of 60 attacks categorized according to the MITRE ATT&CK framework and a CLI-centered orchestration layer, complemented by an optional Streamlit UI, that automates the full cycle of execution, data collection, and consolidation. The pipeline incorporates traffic capture, log inspection, and feature extraction using multiple tools, producing structured and traceable datasets. By providing broad coverage of attacks, techniques, and tactics among existing testbeds, AttackZoo reduces the operational overhead of experiments and enables the systematic generation of comparable datasets, with all artifacts openly available._

## README Structure

This document is organized as follows:

1. [Project summary and artifact scope](#attackzoo-a-reproducible-testbed-for-the-execution-of-attacks-and-the-generation-of-network-traffic-datasets)
2. [This README Structure](#readme-structure)
3. [Artifact Badges Considered](#artifact-badges-considered)
4. [Basic environment information, components, and requirements](#basic-information)
5. [Dependencies and external resources used during installation](#dependencies)
6. [Safety and isolation guidance](#safety-considerations)
7. [Installation on a clean machine](#installation-process)
8. [Minimal validation test](#minimal-test)
9. [Reproducible experiment claims](#reproducible-experiment-claims)
10. [Basic code and repository documentation](#basic-documentation)
11. [Troubleshooting](#troubleshooting)
12. [License](#license)

## Artifact Badges Considered

The artifact is intended to support the following review badges:

- Available Artifacts (Artefatos Disponíveis): **`SeloD`** <img src="./contrib/assets/SeloD.png" width="23"/>
- Functional Artifacts (Artefatos Funcionais): **`SeloF`** <img src="./contrib/assets/SeloF.png" width="23"/>
- Sustainable Artifacts (Artefatos Sustentáveis): **`SeloS`** <img src="./contrib/assets/SeloS.png" width="23"/>
- Reproducible Experiments (Experimentos Reprodutíveis): **`SeloR`** <img src="./contrib/assets/SeloR.png" width="23"/>

## Basic Information

### Main Components

| Component | Location | Purpose |
| --- | --- | --- |
| Main CLI | `attackzoo.py` | Command-line entry point for the AttackZoo Testbed. |
| CLI parser and commands | `modules/attackzoo/` | Implementation of `status`, `list`, `run`, `stop`, `ps`, `logs`, `captures`, `features`, `dataset`, `experiment`, and `report`. |
| Dynamic attack catalog | `docker/attackers/*/attack.yaml` | Plug-and-play attack definitions loaded automatically by the tool. |
| Target servers | `docker/servers/` | Docker images for HTTP, SSH, SMB, MQTT, CoAP, XRCE-DDS, Zenoh, Telnet, and SSL/Heartbleed services. |
| Benign clients | `docker/clients/` | Containers that generate benign background traffic. |
| Web UI | `modules/attackzoo_st.py` | Streamlit interface for interactive use. |
| Helper scripts | `setup.sh`, `build.sh`, `servers.sh`, `clients.sh`, `environment.sh` | Dependency installation, Docker image builds, server/client control, environment control and Streamlit optional Web UI. |
| Outputs | `captures/`, `features/`, `datasets/`, `experiments/`, `logs/` | Artifacts generated during runs and experiments. |

### Current Catalog

The current repository contains 60 attacks declared through individual `attack.yaml`, organized into the following categories:

| Category | Count |
| --- | :---: |
| `1) Reconnaissance and Discovery` | 9 |
| `2) Network Interception and Exploitation` | 8 |
| `3) Web Application Attacks` | 10 |
| `4) Brute Force Against Remote Access Applications` | 2 |
| `5) Exfiltration and Tunneling` | 2 |
| `6) Denial of Service and Impact` | 8 |
| `7) IoT` | 21 |

>[!NOTE]
>The current MITRE ATT&CK metadata covers 9 tactics, 21 top-level techniques, and 35 technique/sub-technique entries when sub-techniques are counted separately. See the [full mapping documentation](contrib/docs/MITRE_ATTACK_MAPPING.md).

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

>[!NOTE]
>More details about [Safety and port isolation guidance](#safety-considerations).

### Recommended Execution Environment

Environment used for local validation:

| Resource | Tested configuration |
| --- | --- |
| CPU | AMD Ryzen 5 5600X 6-Core Processor |
| Memory | 32 GB DDR4 |
| Storage | NVMe |
| Operating system | Ubuntu 24.04.4 LTS |
| Python | Python 3.12.3 with `venv` |
| Docker | Docker Engine 29.6.1 |

>[!WARNING]
>**Minimum recommended environment for review:**

| Resource | Recommended minimum |
| --- | --- |
| Operating system | Ubuntu 24.04 LTS or a compatible Linux distribution with `apt` packge manager  |
| Packages | Docker and Python 3 |
| CPU | 4 vCPUs |
| Memory | 4 GB RAM for reduced tests; 8 GB for full experiment |
| Storage | 30 GB free for installation and images; 50 GB or more for PCAP captures and repeated experiments |
| Network | Isolated environment, preferably a dedicated host or lab environment without direct Internet exposure |

## Dependencies

### System Dependencies

`setup.sh` installs and/or configures the main dependencies on Ubuntu/Debian-like systems:

- `ca-certificates`
- `curl`
- `git`
- `python3-venv`
- `tcpdump`
- `tshark`
- Docker Engine (`docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`)

Tested package versions on Ubuntu 24.04.4 LTS:

| Package | Tested version |
| --- | --- |
| `ca-certificates` | `20260601~24.04.1` |
| `curl` | `8.5.0-2ubuntu10.11` |
| `git` | `1:2.43.0-1ubuntu7.3` |
| `python3-venv` | `3.12.3-0ubuntu2.1` |
| `tcpdump` | `4.99.4-3ubuntu4.24.04.1` |
| `tshark` | `4.2.2-1.1build3` |
| `docker-ce` | `5:29.6.1-1~ubuntu.24.04~noble` |
| `docker-ce-cli` | `5:29.6.1-1~ubuntu.24.04~noble` |
| `containerd.io` | `2.2.6-1~ubuntu.24.04~noble` |
| `docker-buildx-plugin` | `0.35.0-1~ubuntu.24.04~noble` |

>[!CAUTION]
>Please note that **this repository depends** on `Docker Engine` being installed as described in the [official documentation](https://docs.docker.com/engine/install/ubuntu/) and also on the [post-installation instructions for Linux](https://docs.docker.com/engine/install/linux-postinstall). Be advised that installation via `apt install` **might not be compatible**.

The script also adds the current user to the `docker` group, configures capture permissions for `tcpdump`, creates `.venv/`, installs Python dependencies, and installs NTLFlowLyzer Project directly from its GitHub repository.

### Python Dependencies

`requirements.txt` is frozen with exact versions from the validated `.venv`.
Primary runtime dependencies include:

```text
streamlit==1.58.0
pandas==3.0.4
numpy==2.5.0
matplotlib==3.11.0
scapy==2.7.0
PyYAML==6.0.3
```

The validated `.venv` also contains `NTLFlowLyzer==0.1.0`; `setup.sh` installs it separately from the upstream GitHub repository listed below.

### External Resources Used During Installation

- The official Docker repository for Ubuntu.
- Operating-system package indexes.
- PyPI for Python packages.
- `https://github.com/ahlashkari/NTLFlowLyzer.git`.
- Base images and packages referenced by Dockerfiles under `docker/`.

No SSH keys, private credentials, API tokens, or cloud infrastructure are required to run the artifact.

>[!NOTE]
> The time required to complete the process may vary depending on the host's resources and the available internet speed.

## Safety Considerations

This artifact runs scanners, brute-force tools, fuzzers, floods, and other attack behaviors. **Use it only in an environment that you own, isolate, and are authorized to test.**

Safe review recommendations:

- Run the artifact on an isolated dedicated machine or disposable lab environment.
- Avoid installing the testbed on a workstation or shared host.
- Do not point attacks at external addresses, third-party networks, or services without explicit authorization.
- Prefer internal testbed targets, such as the `server-*` containers.
- Avoid exposing the host directly to the Internet during review.
- Check for port conflicts before starting servers.
- Use short durations for DoS/flood attacks during initial tests.
- Stop attack containers after validation with `python3 attackzoo.py stop <attack_id>` or `docker rm -f <container>`.

Ports that may be exposed on the host:
**TCP**: 139, 445, 1883, 2222, 2323, 5683, 7447, 8080, 8443, 9001, 11080.
**UDP**: 137, 138, 5683, 8888.

>[!NOTE]
> Weak passwords and intentionally vulnerable configurations in the containers are disposable lab values. Do not reuse them anywhere else.

## Installation process

### Demonstration video of the installation process

[![installation-process-video](https://img.youtube.com/vi/fx2Z5ZD_Rbo/0.jpg)](https://www.youtube.com/watch?v=fx2Z5ZD_Rbo)

>[!TIP]
>This video demonstrates and follows all the steps listed below.

The steps below assume a **clean Ubuntu 24.04 LTS machine** or an equivalent environment.

### 1. Clone the repository and enters it

```bash
git clone git@github.com:GT-IoTEdu/attackzoo-sbseg26.git
cd attackzoo-sbseg26
```

### 2. Install system and Python dependencies with an _`one-script-setup`_

```bash
chmod +x setup.sh
./setup.sh dependencies
```

After installation, apply the new Docker group permission:

```bash
newgrp docker
```

>[!NOTE]
> This command will reload the shell session. It's mandatory to reload the current shell before continue.

_Logging out and back in also applies the group change._

### 3. Build the Docker Images Catalog and Start Servers

Here we have 2 options:
- A `Full Version`: (60 attackers, 9 servers, 2 client types and all dependencies); or
- A `Reduced Version`: (7 attackers, 3 servers and dependencies).

#### \*\* Full Version Installation \*\*

>[!CAUTION]
> This builds all server, attacker, and client images, starts target servers, and other elements. The first build depends on machine and network speed: on a machine similar to the one previously described as the test environment used by the authors, **reserve 15 to 30 minutes** because many Docker images and packages will be downloaded and compiled.

```bash
./setup.sh full
```

#### \*\* Reduced Version Installation \*\* 

>[!TIP]
>For a faster reviewer demonstration, the repository provides this reduced profile with seven attacks, one from each catalog category, and only the HTTP, SSH, and MQTT target servers: yet they still manage to demonstrate all of the tool's capabilities. Even so, the installation typically takes **at least 2 to 5 minutes**. 

```bash
./setup.sh redux
```

The reduced testbed profile does not build benign client images. See [contrib/docs/REDUX_LAB.md](contrib/docs/REDUX_LAB.md) for more information about the included attack list, server profile, and campaign defaults.

### 4. Activate The Python Environment

```bash
cd /path/to/attackzoo-sbseg26
if [[ -z "${VIRTUAL_ENV}" ]]; then
  source .venv/bin/activate
fi
```

### 5. Simples Installation Check

```bash
python3 attackzoo.py status
```

Expected output: `docker_available=true`

>[!NOTE]
>If Docker is not accessible, check whether the service is running and whether Docker group permissions have been applied. Some help could be found in [Troubleshooting section](#troubleshooting).

## Minimal Test

This section runs a short validation to confirm that the CLI loads the catalog, that target servers are active, and a simple attack can be launched against a testbed server.

### 1. Prepare The Session

```bash
cd /path/to/attackzoo-sbseg26
if [[ -z "${VIRTUAL_ENV}" ]]; then
  source .venv/bin/activate
fi
```

### 2. Confirm Docker And The Catalog

```bash
python3 attackzoo.py status
python3 attackzoo.py list --category "Denial"
```

Expected results:

- `docker_available=true`.
- A list of attacks from `6) Denial of Service and Impact`, including `dos_http_simple`.

### 3. Confirm That The HTTP Server Is Active

```bash
./servers.sh start
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep server-http-server
curl -I http://127.0.0.1:8080/
```

>[!IMPORTANT]
> If you installed the reduced version, you need to add `redux` as first parameter for servers.sh script.
> `./servers.sh redux start`


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
- `experiments/smoke_http/reports/` with tables and charts when enough data is available.

Accepted availability probes for `--probes` are `http`, `https`, `ssh`, `smb`, `mqtt`, `coap`, `xrce`, `zenoh`, and `telnet`. Use `all` to enable all probes or `none` to disable them. For service-specific endpoints, repeat `--probe-endpoint`, for example `--probe-endpoint ssh=172.17.0.3:22`.

## Reproducible Experiment Claims

The claims below reflect the functionality implemented in this repository. If the final paper uses different numbering or titles, keep the commands and adjust only the claim labels.

### Claim 1: The Artifact Provides An Extensible Catalog Of Containerized Attacks

Goal: show that the tool automatically discovers attacks declared in `docker/attackers/*/attack.yaml`, groups them by category, and exposes execution parameters through the CLI.

Commands:

```bash
cd /path/to/attackzoo-sbseg26
if [[ -z "${VIRTUAL_ENV}" ]]; then
  source .venv/bin/activate
fi
python3 attackzoo.py list
python3 attackzoo.py list --json > /tmp/attackzoo-catalog.json
python3 -m json.tool /tmp/attackzoo-catalog.json > /tmp/attackzoo-catalog-formatted.json
```
To check the full output:

```bash
cat /tmp/attackzoo-catalog-formatted.json | jq
```

To check the count by categories:

```bash
python3 - <<'PY'
from modules.registry import CATEGORIES
print(sum(len(v) for v in CATEGORIES.values()), "attacks")
for category, attacks in CATEGORIES.items():
    print(f"{category}: {len(attacks)}")
PY
```

**Expected time**: less than 1 minute.
**Expected resources**: negligible CPU and memory. Docker does not need to be running for catalog listing, but Python dependencies must be installed.
**Expected result**: 60 attacks loaded across 7 categories. The JSON output contains `id`, `name`, `image`, `container`, `params`, `mitre`, and `max_runtime_s` for each attack.

### Claim 2: The Environment Runs Attacks Against Containerized Target Servers

Goal: demonstrate functional attack execution against services inside the testbed.

Preparation:

```bash
cd /path/to/attackzoo-sbseg26
if [[ -z "${VIRTUAL_ENV}" ]]; then
  source .venv/bin/activate
fi
./servers.sh start
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E '^server-'
```

>[!IMPORTANT]
> If you installed the reduced version, you need to add `redux` as first parameter for servers.sh script.
> `./servers.sh redux start`

Simple HTTP DoS against th HTTP Server (for example):

```bash
HTTP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)
python3 attackzoo.py run dos_http_simple --target "$HTTP_IP" --port 80
```

TCP Port Knocking Reconnaissance against the HTTP Server (for example):

```bash
python3 attackzoo.py run recon_port_scanner_tcp --target "$HTTP_IP"
```

Check running attacks and stop manually:

```bash
python3 attackzoo.py ps
python3 attackzoo.py stop dos_http_simple
python3 attackzoo.py stop recon_port_scanner_tcp
```

Expected time: 1 to 5 minutes after images have already been built.

Expected resources: 1 to 2 vCPUs and up to 2 GB of additional RAM for short tests. Flood attacks may increase CPU and network usage; keep durations short.

Expected result: the CLI prints `[OK] Container started` and `[OK] Container stoped`, containers appear in `ps` while active, and servers remain manageable through `servers.sh`.

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

>[!NOTE]
> This experimente takes 15 seconds to complete. Please wait until terminal prints something like:
>`[OK] dos_http_simple L0 run01`
>`experiments/http_features/reports`

**Expected time**: 1 to 10 minutes for short experiments. NTLFlowLyzer may take longer on large PCAP files.
**Expected resources**: disk use proportional to captured traffic. Short tests usually need less than 1 GB; full repetitions may require tens of GB.
**Expected result**:
- Probes, tables, charts, telemetry and more under `experiments/http_features/dos_http_simple/...`
- Stored PCAP captures under `captures/`.
- Features CSVs under `features/`.
- Dataset CSVs under `datasets/`.
- Per-run metadata in `meta.json`.

To list resulting captures:

```bash
python3 attackzoo.py captures
python3 attackzoo.py captures --latest --json
```

### Claim 4: The Artifact Reproduces Warmup-Attack-Cooldown Batches And T3-T8 Reports

Goal: reproduce a more complex experimental scenario with warmup, attack, and cooldown phases, multi throughput levels, availability probes, hooks, filter and consolidated reports:

```bash

HTTP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)

python3 attackzoo.py experiment \
  --attack-id dos_http_simple \
  --out full_http \
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

>[!NOTE]
> This experimente takes 12~15 minutes to complete. It will execute 3 runs of 2 throughput levels with 30s+60s+30s seconds per run:
>`3 x 2 x (30 + 60 + 30) = 720 seconds (12 minutes)`.
>Please wait until terminal prints something like:
>`[OK] dos_http_simple L0 run01`
>`[OK] dos_http_simple L0 run02`
>`[OK] dos_http_simple L0 run03`
>`[OK] dos_http_simple L1 run01`
>`[OK] dos_http_simple L1 run02`
>`[OK] dos_http_simple L1 run03`
>`experiments/full_http/reports`

If you already have data from a previous experiment, you can regenerate reports from collected/stored data:

```bash
python3 attackzoo.py report \
  --input experiments/full_http/ \
  --warmup 30 \
  --attack 60 \
  --cooldown 30
```

**Expected time**: approximately `(warmup + attack + cooldown) * runs * levels`, plus post-processing. The example above takes about 12 minutes before report generation.
**Expected resources**: 4 vCPUs, 8 GB RAM, and a few GB of free space for PCAPs/CSVs. Increase disk and memory for more levels, more repetitions, or higher-intensity attacks.
**Expected result**:

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

Full example `copy-and-paste`: 

```bash
# Create attack dir
mkdir -p docker/attackers/example-ping
# Create Dockerfile
cat > docker/attackers/example-ping/Dockerfile <<'EOF'
FROM alpine:3.20

RUN apk add --no-cache iputils

ENTRYPOINT ["ping", "-c", "4"]
EOF
# Create attack.yaml attack declaration
cat > docker/attackers/example-ping/attack.yaml <<'EOF'
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
EOF
# Build the new container
docker build -t attack-example-ping:latest docker/attackers/example-ping
# List attack from catalog
python3 attackzoo.py list --id example_ping
```

**Expected time**: less than 5 minutes for a simple attack, plus Docker image build time.
**Expected result**: the new "attack" appears in the CLI without changing any core Python file in the Project.

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
|   |-- attackzoo_st.py           # Streamlit UI
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
|-- contrib/docs/
|   |-- CLI.md                    # Detailed attackzoo.py command reference
|   |-- REDUX_LAB.md              # Reduced reviewer lab profile
|   |-- MITRE_ATTACK_MAPPING.md   # MITRE ATT&CK coverage reference
|   `-- CATALOG_MAINTENANCE.md    # Notes for maintaining the attack catalog
`-- LICENSE                       # BSD 3-Clause License
```

### Code Documentation

This project was developed with code documentation as built-in function comments, using mainly **`Python docstring`**.

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

### Summary of the `attack.yaml` Basic Schema

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

### Docker isn't running or not available

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

### Missing Docker Image

If the CLI reports that an image cannot be found:

```bash
cd cd /path/to/attackzoo-sbseg/docker/
./build-images.sh full
```

Or run the wrapper again:

```bash
cd /path/to/attackzoo-sbseg/
./build.sh full
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
cd /path/to/attackzoo-sbseg/
./servers.sh start
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep server
```

>[!IMPORTANT]
> If you installed the reduced version, you need to add `redux` as first parameter for servers.sh script.
> `./servers.sh redux start`

## License

This project is licensed under the BSD 3-Clause License. See `LICENSE` in the repository root for the full terms.
