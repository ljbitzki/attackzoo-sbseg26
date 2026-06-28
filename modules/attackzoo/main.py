from __future__ import annotations

from typing import List, Optional

from modules.attackzoo.parser import build_parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args, extra = parser.parse_known_args(argv)
    args.extra = extra
    return int(args.func(args))
