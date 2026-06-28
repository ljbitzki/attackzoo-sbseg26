# Categorized Attack Review for `docker/attackers`

This document summarizes the local attack catalog under `docker/attackers`. The catalog is discovered from each attack directory's `attack.yaml`, together with its `README.md`, `Dockerfile`, `entrypoint.sh`, and any helper code executed by the container.

## Current Structure

- Attack containers live in `docker/attackers/<attack-name>/`.
- Benign clients live in `docker/clients/<client-name>/`.
- Target servers live in `docker/servers/<server-name>/`.
- The runtime catalog is loaded by `modules/loader.py` and `modules/registry.py` from `docker/attackers/*/attack.yaml`.

## Catalog Notes

The attack set spans reconnaissance, local-network exploitation, web application testing, brute force, tunneling/exfiltration simulation, denial of service, and IoT protocol behavior. Most attacks expose `target_ip`, `target_port`, or `target_net`; several also support `intensity_params` such as `duration_s`, `count`, `rate_pps`, `threads`, `concurrency`, `delay_ms`, and `payload_size`.

## Parameterization Guidance

Prefer adding new controls through `attack.yaml` instead of hardcoding values in entrypoints. When an attack accepts intensity parameters, map them to environment variables in `entrypoint.sh` and keep defaults conservative enough for a local lab.

## Adding Or Updating Attacks

Create or update `docker/attackers/<attack-name>/` with a `Dockerfile`, an executable `entrypoint.sh`, and an `attack.yaml`. Build images from `docker/` with:

```bash
./build-images.sh
```

Then verify discovery with:

```bash
python3 AttackZoo.py list --id <attack_id>
```
