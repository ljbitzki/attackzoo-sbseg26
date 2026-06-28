# Archived README Notes

This file is kept as an archived companion to the root README. The active root `README.md` is intentionally left unchanged during the current translation pass.

## Current Repository Paths

The repository now uses English directory names for Docker assets:

- `docker/attackers/` for attack containers.
- `docker/clients/` for benign client containers.
- `docker/servers/` for target server containers.

The dynamic attack catalog is loaded from `docker/attackers/*/attack.yaml` by `modules/loader.py` and `modules/registry.py`.

## Common Commands

```bash
./setup.sh
./build.sh
python3 attackzoo.py status
python3 attackzoo.py list
python3 attackzoo.py run dos_syn_flood --target 172.17.0.2 --duration 10
python3 attackzoo.py stop dos_syn_flood
python3 attackzoo.py experiment --attack-id dos_syn_flood --out example --runs 3
```

Generated captures, features, datasets, logs, and experiment outputs are stored under `captures/`, `features/`, `datasets/`, `logs/`, and `experiments/` respectively.
