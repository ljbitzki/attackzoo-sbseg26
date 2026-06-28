# Generic Contributor Notes

Use this document as a compact reference for maintaining repository assets outside the root README.

## Directory Names

Use the current Docker paths consistently:

- `docker/attackers/`
- `docker/clients/`
- `docker/servers/`

Avoid the old Portuguese Docker directory names in new documentation, scripts, and examples.

## Documentation Language

Container READMEs, YAML descriptions, script comments, CLI help text, and internal documentation should use American English. Keep Docker image and container identifiers unchanged when they are part of the runtime contract, for example `attack-*`, `client-*`, and `server-*`.

## Validation

After changing scripts or catalog files, run syntax checks for Python, shell, and YAML files where possible. Full Docker builds are useful but optional when the change is limited to documentation text.
