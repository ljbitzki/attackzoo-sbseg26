# AttackZoo Reduced Lab

The reduced lab is a fast demonstration profile for reviewers who want to exercise the complete AttackZoo workflow without building the full attack and client catalog.

It builds only seven attacker images, one representative attack from each catalog category, plus the three target servers needed by those attacks. Benign client images are not built in this profile.

## Included Scope

| Category | Attack ID | Attack Image | Required Server |
| --- | --- | --- | --- |
| 1) Reconnaissance and Discovery | `recon_arp_scan` | `attack-arp-scan` | none specific |
| 2) Network Interception and Exploitation | `net_arp_spoof` | `attack-arp-spoof` | none specific |
| 3) Web Application Attacks | `web_simple_scanner` | `attack-web-simple-scanner` | `server-http-server` |
| 4) Brute Force Against Remote Access Applications | `bf_ssh` | `attack-ssh-bruteforce` | `server-ssh-server` |
| 5) Exfiltration and Tunneling | `exf_icmp_tunnel` | `attack-icmp-tunnel` | `server-ssh-server` |
| 6) Denial of Service and Impact | `dos_http_simple` | `attack-dos-http-simple` | `server-http-server` |
| 7) IoT | `iot_mqtt_publisher` | `attack-mqtt-publisher` | `server-mqtt-broker` |

The reduced server profile contains:

- `server-http-server`
- `server-ssh-server`
- `server-mqtt-broker`

## Setup

From the repository root:

```bash
chmod +x setup.sh
./setup.sh redux
```

This installs the normal system and Python dependencies, installs Docker when needed, builds only the reduced Docker image set, and starts the reduced target servers.

If dependencies are already installed and only the Docker images need to be rebuilt, run:

```bash
./build.sh redux
```

## Server Control

The reduced profile can be managed independently from the full server set:

```bash
./servers.sh start redux
./servers.sh restart redux
./servers.sh stop redux
```

## Run The Reduced Campaign

Activate the virtual environment and run:

```bash
source .venv/bin/activate
python3 contrib/scripts/run_redux_campaign.py
```

Default campaign settings:

| Setting | Value |
| --- | --- |
| Runs | `1` |
| Levels | `L1` |
| Warmup | `3` seconds |
| Attack | `5` seconds |
| Cooldown | `2` seconds |
| Server profile | `redux` |
| Feature extraction | enabled |
| Dataset generation | enabled |
| Reports | enabled |
| Resource collection | enabled |
| Server statistics | enabled |

Outputs are written under:

```text
experiments/redux_campaign_<timestamp>/
```

The wrapper accepts the same optional arguments as `contrib/scripts/run_full_campaign.py`, so reviewers can override defaults when needed. For example:

```bash
python3 contrib/scripts/run_redux_campaign.py --out reviewer_quick_check --levels L0
```

## Notes

- The reduced lab is intended for quick functional review and demonstration.
- The full artifact remains available through `./setup.sh`, `./build.sh`, and   `contrib/scripts/run_full_campaign.py`.
- Benign background clients are intentionally excluded from the reduced build.
