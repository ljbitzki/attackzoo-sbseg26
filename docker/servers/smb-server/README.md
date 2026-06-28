# Server "SMB / Samba Server"

> Provide an SMB/Samba share for enumeration and benign share-listing traffic.

## Metadata

| Field | Value |
|---|---|
| Logical ID | `smb-server` |
| Role | target-server |
| Image | `server-smb-server:latest` |
| Container | `server-smb-server` |
| Base | `alpine` |
| Service | Samba with a public share configured at container startup |
| Protocols | `smb`, `netbios` |
| Internal ports | `137/udp`, `138/udp`, `139/tcp`, `445/tcp` |
| Published ports | `137:137/udp`, `138:138/udp`, `139:139/tcp`, `445:445/tcp` |

## Execution

```bash
docker run -it -d --rm --name server-smb-server -p 139:139 -p 445:445 -p 137:137/udp -p 138:138/udp server-smb-server:latest -g "log level = 3" -s "public;/share" -u "example2;badpass"
```

## Container IP

```bash
docker container inspect server-smb-server --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Logs

```bash
docker logs server-smb-server
```

## Related Attacks

- `recon_smb_enum`

## Related Benign Clients

- `client-random:smb`
- `client-super:smb`

## Testbed Observability

- SMB/NetBIOS queries
- Samba logs on stdout
- share-listing attempts

In controlled experiments, use `python3 attackzoo.py experiment --server server-smb-server` to associate target-container telemetry with execution artifacts.
