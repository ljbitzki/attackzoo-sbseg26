# AttackZoo Documentation

This document describes the current repository layout and the command-line workflow. The root `README.md` is handled separately and is intentionally not edited in this pass.

## Docker Layout

- `docker/attackers/`: attack container definitions. Each attack should provide `attack.yaml`, `Dockerfile`, and the entrypoint/helper files needed by the container.
- `docker/clients/`: benign client containers, including `random` and `super`.
- `docker/servers/`: target server containers used by the lab.

The attack catalog is discovered from `docker/attackers/*/attack.yaml`; no Python code change is required when a well-formed attack definition is added.

## Main Commands

```bash
python3 attackzoo.py status
python3 attackzoo.py list
python3 attackzoo.py run <attack_id> --target <ip-or-host> --duration <seconds>
python3 attackzoo.py stop <attack_id>
python3 attackzoo.py captures
python3 attackzoo.py features --pcap captures/example.pcap
python3 attackzoo.py dataset --pcap captures/example.pcap
python3 attackzoo.py experiment --attack-id <attack_id> --out <name>
```

## Experiments

The `experiment` command runs warmup, attack, and cooldown phases across one or more intensity levels. Outputs are written under `experiments/<out>/<attack_id>/<level>/run<N>/` and may include PCAP captures, probe CSVs, resource telemetry, generated features, datasets, and report tables/figures.

## Adding A New Attack

Create a new directory under `docker/attackers/<attack-name>/` and include:

- `attack.yaml` with the catalog metadata, parameter schema, image name, and container name.
- `Dockerfile` for the image.
- `entrypoint.sh` or equivalent executable code.
- `README.md` describing purpose, parameters, run examples, and safety notes.

Build and validate with:

```bash
cd docker
./build-images.sh
cd ..
python3 attackzoo.py list --id <attack_id>
```

