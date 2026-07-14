# Attack Catalog Maintenance Notes

This document is a compact contributor reference for maintaining the local AttackZoo catalog. It intentionally avoids repeating the user-facing setup, execution, and reproducibility material from the root `README.md`.

## Documentation Map

- `README.md`: primary artifact documentation for setup, safety, validation, and reproducibility claims.
- `contrib/docs/CLI.md`: detailed `attackzoo.py` command reference.
- `contrib/docs/REPOSITORY_OVERVIEW.md`: repository layout and code-organization notes.
- `contrib/docs/MITRE_ATTACK_MAPPING.md`: canonical repository-level MITRE ATT&CK coverage reference generated from `docker/attackers/*/attack.yaml`.
- `contrib/docs/REDUX_LAB.md`: reduced reviewer lab profile, included attacks, servers, and quick campaign defaults.
- `contrib/docs/TROUBLESHOOTING.md`: operational troubleshooting notes.
- `docker/attackers/*/README.md`: attack-specific purpose, parameters, examples, and safety notes.
- `docker/servers/*/README.md` and `docker/clients/*/README.md`: service/client-specific operational notes.

## Repository Naming Conventions

Use the current English Docker paths consistently in documentation, scripts, and examples:

- `docker/attackers/`
- `docker/clients/`
- `docker/servers/`

Avoid legacy Portuguese directory names in new material. Runtime names such as `attack-*`, `client-*`, and `server-*` are part of the local Docker contract and should remain unchanged unless the corresponding scripts and metadata are updated together.

## Attack Catalog Structure

Each attack lives under:

```text
docker/attackers/<attack-name>/
```

A complete attack entry usually includes:

- `attack.yaml` with catalog metadata, image/container names, parameter schema, target mapping, runtime hints, and MITRE references.
- `Dockerfile` for the attack image.
- `entrypoint.sh` or equivalent executable code used by the container.
- `README.md` describing the attack purpose, parameters, examples, and safety notes.
- Optional helper files required by the attack implementation.

The runtime catalog is discovered from `docker/attackers/*/attack.yaml` by `modules/loader.py` and `modules/registry.py`. A well-formed attack definition should appear in the CLI without changing Python code.

## Summary Of The `attack.yaml` Basic Schema

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

## Parameterization Guidance

Prefer adding new runtime controls through `attack.yaml` instead of hardcoding values in entrypoints. When an attack accepts intensity parameters, map them to environment variables or explicit command arguments in `entrypoint.sh`.

Keep defaults conservative enough for local review. High-volume, flood, fuzzing, brute-force, or scanner behaviors should require explicit parameters for aggressive settings.

Common parameter keys include:

- `target_ip`
- `target_port`
- `target_net`
- `duration_s`
- `rate_pps`
- `threads`
- `concurrency`
- `delay_ms`
- `payload_size`

## Adding Or Updating An Attack

1. Create or update `docker/attackers/<attack-name>/`.
2. Add or revise `attack.yaml`, `Dockerfile`, `entrypoint.sh`, and `README.md`.
3. Keep `attack.yaml` aligned with the schema described in this document.
4. Add MITRE metadata when the behavior has a clear mapping.
5. Build the relevant Docker image.
6. Verify catalog discovery and perform a short local run against an authorized target.

Useful validation commands:

```bash
python3 attackzoo.py list --id <attack_id>
docker build -t <attack-image>:latest docker/attackers/<attack-name>
python3 attackzoo.py run <attack_id> --target <local-target> --duration 5
python3 attackzoo.py stop <attack_id>
```

For full or reduced image builds, use:

```bash
./build.sh full
./build.sh redux
```

## Documentation Style

Use American English for container READMEs, YAML descriptions, script comments, CLI help text, and internal documentation.

Keep generated or authoritative references in one place:

- Do not duplicate the full MITRE table outside `contrib/docs/MITRE_ATTACK_MAPPING.md`.
- Do not duplicate setup, safety, and reproducibility workflows outside `README.md` unless a shorter document has a specific reviewer purpose.
- Use links to the root references when a secondary document needs broader context.

## Maintenance Checklist

Before considering a catalog or documentation change complete:

- Run `python3 attackzoo.py list --id <attack_id>` for changed attacks.
- Run syntax checks for touched Python, shell, YAML, and Markdown files where applicable.
- Rebuild the relevant Docker image if Dockerfiles or runtime helper scripts changed.
- Run a short local attack execution for behavior changes.
- Update `contrib/docs/MITRE_ATTACK_MAPPING.md` if `attack.yaml` MITRE metadata changes.
- Keep `README.md` links accurate when adding or removing contributor documents.
