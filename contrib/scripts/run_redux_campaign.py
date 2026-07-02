#!/usr/bin/env python3
"""Run the reduced AttackZoo demonstration campaign.

This wrapper reuses run_full_campaign.py with a fixed seven-attack subset:
one representative attack from each catalog category, short timings, and only
the target servers required by that subset.
"""

from __future__ import annotations

import datetime as dt
import sys
from typing import Optional, Sequence

from run_full_campaign import main as run_full_campaign_main


REDUX_ATTACKS = (
    "recon_arp_scan",
    "net_arp_spoof",
    "web_simple_scanner",
    "bf_ssh",
    "exf_icmp_tunnel",
    "dos_http_simple",
    "iot_mqtt_publisher",
)


def campaign_name() -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"redux_campaign_{stamp}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    user_args = list(argv if argv is not None else sys.argv[1:])
    defaults = [
        "--out",
        campaign_name(),
        "--runs",
        "1",
        "--levels",
        "L1",
        "--warmup",
        "3",
        "--attack",
        "5",
        "--cooldown",
        "2",
        "--check-interval-s",
        "1",
        "--server-profile",
        "redux",
        "--only",
        ",".join(REDUX_ATTACKS),
    ]
    return run_full_campaign_main(defaults + user_args)


if __name__ == "__main__":
    raise SystemExit(main())
