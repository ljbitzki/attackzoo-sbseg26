from __future__ import annotations

import csv
import secrets
import socket
import ssl
import struct
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple
from urllib.parse import urlparse

from modules.attackzoo.common import _ensure_dir, _phase_of

ProbeResult = Tuple[int, float, str]

DEFAULT_PROBE_PORTS: Dict[str, int] = {
    "http": 80,
    "https": 443,
    "ssh": 22,
    "smb": 445,
    "mqtt": 1883,
    "coap": 5683,
    "xrce": 8888,
    "zenoh": 7447,
    "telnet": 23,
}

PROBE_ALIASES: Dict[str, str] = {
    "web": "http",
    "ssl": "https",
    "tls": "https",
    "xrce-dds": "xrce",
    "xrcedds": "xrce",
    "micro-xrce-dds": "xrce",
    "uxrce-dds": "xrce",
    "zenoh-pico": "zenoh",
}

SUPPORTED_PROBES: Tuple[str, ...] = tuple(DEFAULT_PROBE_PORTS.keys())


def normalize_probe_service(service: str) -> str:
    svc = service.strip().lower().replace("_", "-")
    svc = PROBE_ALIASES.get(svc, svc)
    if svc not in DEFAULT_PROBE_PORTS:
        supported = ", ".join(SUPPORTED_PROBES)
        raise ValueError(f"unknown probe service={service!r}; supported: {supported}")
    return svc


def probe_default_port(service: str) -> int:
    return DEFAULT_PROBE_PORTS[normalize_probe_service(service)]


def _ssl_context() -> ssl.SSLContext:
    ctx = ssl._create_unverified_context()
    try:
        ctx.set_ciphers("ALL:@SECLEVEL=0")
    except ssl.SSLError:
        pass
    return ctx


def probe_http(url: str, timeout_s: float = 2.0) -> ProbeResult:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    t0 = time.perf_counter()
    ok = 0
    err = ""
    try:
        req = Request(url, headers={"User-Agent": "SBSeg26-probe/1.0"})
        kwargs: Dict[str, Any] = {}
        if urlparse(url).scheme.lower() == "https":
            kwargs["context"] = _ssl_context()
        with urlopen(req, timeout=timeout_s, **kwargs) as r:
            _ = r.read(64)
        ok = 1
    except (HTTPError, URLError, TimeoutError) as e:
        err = str(e)
    except Exception as e:
        err = repr(e)
    dt_ms = (time.perf_counter() - t0) * 1000.0
    return ok, dt_ms, err


def probe_https(url: str, timeout_s: float = 2.0) -> ProbeResult:
    return probe_http(url, timeout_s=timeout_s)


def _mqtt_encode_str(s: str) -> bytes:
    b = s.encode("utf-8")
    return len(b).to_bytes(2, "big") + b


def _mqtt_remaining_length(n: int) -> bytes:
    out = bytearray()
    while True:
        digit = n % 128
        n //= 128
        if n > 0:
            digit |= 0x80
        out.append(digit)
        if n == 0:
            break
    return bytes(out)


def probe_mqtt(host: str, port: int, timeout_s: float = 2.0, client_id: str = "SBSeg26-probe") -> ProbeResult:
    """CONNECT/CONNACK (MQTT 3.1.1)"""
    t0 = time.perf_counter()
    ok = 0
    err = ""
    s: Optional[socket.socket] = None
    try:
        s = socket.create_connection((host, port), timeout=timeout_s)
        s.settimeout(timeout_s)

        proto_name = _mqtt_encode_str("MQTT")
        proto_level = b"\x04"          # MQTT 3.1.1
        connect_flags = b"\x02"        # Clean Session
        keepalive = (30).to_bytes(2, "big")
        var_header = proto_name + proto_level + connect_flags + keepalive
        payload = _mqtt_encode_str(client_id)

        remaining = len(var_header) + len(payload)
        fixed = b"\x10" + _mqtt_remaining_length(remaining)  # CONNECT
        pkt = fixed + var_header + payload

        s.sendall(pkt)
        resp = s.recv(4)
        if resp == b"\x20\x02\x00\x00":
            ok = 1
        else:
            err = f"unexpected CONNACK bytes: {resp!r}"
    except Exception as e:
        err = repr(e)
    finally:
        try:
            if s:
                s.close()
        except Exception:
            pass
    dt_ms = (time.perf_counter() - t0) * 1000.0
    return ok, dt_ms, err


def probe_ssh(host: str, port: int, timeout_s: float = 2.0) -> ProbeResult:
    t0 = time.perf_counter()
    ok = 0
    err = ""
    s: Optional[socket.socket] = None
    try:
        s = socket.create_connection((host, port), timeout=timeout_s)
        s.settimeout(timeout_s)
        banner = s.recv(128)
        if banner.startswith(b"SSH-"):
            ok = 1
        else:
            err = f"unexpected SSH banner: {banner[:32]!r}"
    except Exception as e:
        err = repr(e)
    finally:
        try:
            if s:
                s.close()
        except Exception:
            pass
    return ok, (time.perf_counter() - t0) * 1000.0, err


def probe_telnet(host: str, port: int, timeout_s: float = 2.0) -> ProbeResult:
    t0 = time.perf_counter()
    ok = 0
    err = ""
    s: Optional[socket.socket] = None
    try:
        s = socket.create_connection((host, port), timeout=timeout_s)
        s.settimeout(min(timeout_s, 0.5))
        try:
            _ = s.recv(128)
        except Exception:
            pass
        ok = 1
    except Exception as e:
        err = repr(e)
    finally:
        try:
            if s:
                s.close()
        except Exception:
            pass
    return ok, (time.perf_counter() - t0) * 1000.0, err


def _smb2_negotiate_packet() -> bytes:
    header = (
        b"\xfeSMB"
        + struct.pack(
            "<HHIHHIIQIIQ16s",
            64,              # StructureSize
            0,               # CreditCharge
            0,               # Status/ChannelSequence
            0,               # NEGOTIATE
            1,               # CreditsRequested
            0,               # Flags
            0,               # NextCommand
            0,               # MessageId
            0,               # Reserved
            0,               # TreeId
            0,               # SessionId
            b"\x00" * 16,    # Signature
        )
    )
    body = (
        struct.pack(
            "<HHHHI16sIHH",
            36,                    # StructureSize
            2,                     # DialectCount
            1,                     # SecurityMode: signing enabled
            0,                     # Reserved
            0,                     # Capabilities
            secrets.token_bytes(16),
            0,                     # NegotiateContextOffset
            0,                     # NegotiateContextCount
            0,                     # Reserved2
        )
        + struct.pack("<HH", 0x0202, 0x0311)
    )
    payload = header + body
    return b"\x00" + len(payload).to_bytes(3, "big") + payload


def probe_smb(host: str, port: int, timeout_s: float = 2.0) -> ProbeResult:
    t0 = time.perf_counter()
    ok = 0
    err = ""
    s: Optional[socket.socket] = None
    try:
        s = socket.create_connection((host, port), timeout=timeout_s)
        s.settimeout(timeout_s)
        s.sendall(_smb2_negotiate_packet())
        resp = s.recv(256)
        if len(resp) >= 8 and resp[4:8] in (b"\xfeSMB", b"\xffSMB"):
            ok = 1
        else:
            err = f"unexpected SMB response: {resp[:32]!r}"
    except Exception as e:
        err = repr(e)
    finally:
        try:
            if s:
                s.close()
        except Exception:
            pass
    return ok, (time.perf_counter() - t0) * 1000.0, err


def _coap_uri_path_options(path: str) -> bytes:
    out = bytearray()
    last_opt = 0
    for raw_segment in path.strip("/").split("/"):
        if not raw_segment:
            continue
        value = raw_segment.encode("utf-8")
        option_number = 11  # Uri-Path
        delta = option_number - last_opt
        if delta > 12 or len(value) > 12:
            raise ValueError("CoAP probe path uses unsupported option encoding")
        out.append((delta << 4) | len(value))
        out.extend(value)
        last_opt = option_number
    return bytes(out)


def probe_coap(host: str, port: int, timeout_s: float = 2.0, path: str = "/.well-known/core") -> ProbeResult:
    t0 = time.perf_counter()
    ok = 0
    err = ""
    s: Optional[socket.socket] = None
    try:
        msg_id = secrets.randbits(16)
        token = secrets.token_bytes(2)
        pkt = bytes([0x40 | len(token), 0x01]) + msg_id.to_bytes(2, "big") + token
        pkt += _coap_uri_path_options(path)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout_s)
        s.connect((host, port))
        s.send(pkt)
        resp = s.recv(1152)
        if len(resp) < 4:
            err = f"short CoAP response: {resp!r}"
        elif (resp[0] >> 6) != 1:
            err = f"unexpected CoAP version byte: {resp[0]!r}"
        else:
            tkl = resp[0] & 0x0F
            resp_token = resp[4:4 + tkl]
            if resp_token != token:
                err = f"unexpected CoAP token: {resp_token!r}"
            elif resp[1] == 0:
                err = "empty CoAP message"
            else:
                ok = 1
    except Exception as e:
        err = repr(e)
    finally:
        try:
            if s:
                s.close()
        except Exception:
            pass
    return ok, (time.perf_counter() - t0) * 1000.0, err


def probe_xrce(host: str, port: int, timeout_s: float = 2.0) -> ProbeResult:
    t0 = time.perf_counter()
    ok = 0
    err = ""
    s: Optional[socket.socket] = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(min(timeout_s, 0.5))
        s.connect((host, port))
        s.send(b"uxrce_probe_" + secrets.token_bytes(8))
        try:
            _ = s.recv(256)
        except socket.timeout:
            pass
        except OSError as e:
            err = repr(e)
        else:
            pass
        ok = 1 if not err else 0
    except Exception as e:
        err = repr(e)
    finally:
        try:
            if s:
                s.close()
        except Exception:
            pass
    return ok, (time.perf_counter() - t0) * 1000.0, err


def probe_zenoh(host: str, port: int, timeout_s: float = 2.0) -> ProbeResult:
    t0 = time.perf_counter()
    ok = 0
    err = ""
    s: Optional[socket.socket] = None
    try:
        s = socket.create_connection((host, port), timeout=timeout_s)
        ok = 1
    except Exception as e:
        err = repr(e)
    finally:
        try:
            if s:
                s.close()
        except Exception:
            pass
    return ok, (time.perf_counter() - t0) * 1000.0, err


def probe_service(service: str, endpoint: Mapping[str, Any], timeout_s: float = 2.0) -> ProbeResult:
    svc = normalize_probe_service(service)
    url = str(endpoint.get("url") or "")
    host = str(endpoint.get("host") or "127.0.0.1")
    port = int(endpoint.get("port") or DEFAULT_PROBE_PORTS[svc])

    if svc == "http":
        return probe_http(url, timeout_s=timeout_s)
    if svc == "https":
        return probe_https(url, timeout_s=timeout_s)
    if svc == "ssh":
        return probe_ssh(host, port, timeout_s=timeout_s)
    if svc == "smb":
        return probe_smb(host, port, timeout_s=timeout_s)
    if svc == "mqtt":
        return probe_mqtt(host, port, timeout_s=timeout_s)
    if svc == "coap":
        return probe_coap(host, port, timeout_s=timeout_s)
    if svc == "xrce":
        return probe_xrce(host, port, timeout_s=timeout_s)
    if svc == "zenoh":
        return probe_zenoh(host, port, timeout_s=timeout_s)
    if svc == "telnet":
        return probe_telnet(host, port, timeout_s=timeout_s)
    return 0, 0.0, f"unknown service={svc}"


def probe_loop(
    *,
    out_csv: Path,
    service: str,
    endpoint: Mapping[str, Any],
    attack_id: str,
    level: str,
    warmup: float,
    attack: float,
    cooldown: float,
    interval: float,
    timeout_s: float,
    stop_evt: threading.Event,
) -> None:
    service = normalize_probe_service(service)
    t_start = time.time()
    _ensure_dir(out_csv.parent)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "service",
            "attack_id",
            "level",
            "phase",
            "t_epoch",
            "t_iso",
            "t_rel_s",
            "ok",
            "latency_ms",
            "error",
        ])
        while not stop_evt.is_set():
            now = time.time()
            t_rel = now - t_start
            ph = _phase_of(t_rel, warmup, attack, cooldown)
            if ph == "done":
                break

            ok, dt_ms, err = probe_service(service, endpoint, timeout_s=timeout_s)

            t_iso = datetime.fromtimestamp(now, tz=timezone.utc).isoformat()
            w.writerow([
                service,
                attack_id,
                level,
                ph,
                f"{now:.6f}",
                t_iso,
                f"{t_rel:.3f}",
                ok,
                f"{dt_ms:.3f}",
                err,
            ])
            f.flush()
            time.sleep(interval)
