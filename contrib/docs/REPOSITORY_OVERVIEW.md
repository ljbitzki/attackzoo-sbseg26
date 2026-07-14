# Repository Overview

This document keeps repository navigation and code-organization notes outside the root `README.md`.

For setup, safety guidance, artifact-review claims, and minimal validation, see the root `README.md`.
For the detailed CLI reference, see `contrib/docs/CLI.md`.
For attack catalog schema and maintenance notes, see `contrib/docs/CATALOG_MAINTENANCE.md`.

## Repository Layout

```text
.
|-- attackzoo.py                  # Main CLI
|-- setup.sh                      # System/Python dependency installation
|-- build.sh                      # Docker image build and server startup wrapper
|-- run_claim1.sh                 # Automated Claim 1 reviewer check
|-- run_claim2.sh                 # Automated Claim 2 reviewer check
|-- run_claim3.sh                 # Automated Claim 3 reviewer check
|-- run_claim_figures.sh          # Full Figshare-based paper-figure regeneration
|-- servers.sh                    # Control script for server-* containers
|-- clients.sh                    # Control script for client-* containers
|-- environment.sh                # Streamlit/environment helper
|-- requirements.txt              # Frozen Python dependencies
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
|   |-- CATALOG_MAINTENANCE.md    # Attack catalog schema and maintenance notes
|   |-- TROUBLESHOOTING.md        # Operational troubleshooting notes
|   `-- SCRIPTS.md                # Contrib script reference
`-- LICENSE                       # BSD 3-Clause License
```

## Code Documentation

The Python implementation uses docstrings and concise inline comments for local code documentation.
Operational usage is documented in `contrib/docs/CLI.md`, and catalog metadata conventions are documented in `contrib/docs/CATALOG_MAINTENANCE.md`.
