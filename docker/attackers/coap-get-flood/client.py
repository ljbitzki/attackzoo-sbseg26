import asyncio
import os
import sys
import time
from aiocoap import *


def env_int(name, default):
    value = os.getenv(name, str(default))
    try:
        return int(value)
    except ValueError:
        print(f"Invalid integer value for {name}: {value}", file=sys.stderr)
        sys.exit(2)


def env_float(name, default):
    value = os.getenv(name, str(default))
    try:
        return float(value)
    except ValueError:
        print(f"Invalid numeric value for {name}: {value}", file=sys.stderr)
        sys.exit(2)


async def send_get(protocol, base_uri, request_id, timeout_s):
    request = Message(code=GET, uri=f"{base_uri}/{request_id}")
    try:
        await asyncio.wait_for(protocol.request(request).response, timeout=timeout_s)
        return True
    except Exception as exc:
        print(f"Error request {request_id}: {exc}")
        return False


async def run_flood(target, port):
    count = env_int("COUNT", 1000)
    delay_ms = env_int("DELAY_MS", 0)
    duration_s = env_int("DURATION_S", 0)
    request_timeout_s = env_float("REQUEST_TIMEOUT_S", 2.0)
    started_at = time.monotonic()
    sent = 0
    failed = 0
    base_uri = f"coap://{target}:{port}"

    protocol = await Context.create_client_context()

    for request_id in range(count):
        if duration_s > 0 and time.monotonic() - started_at >= duration_s:
            break

        ok = await send_get(protocol, base_uri, request_id, request_timeout_s)
        sent += 1
        if not ok:
            failed += 1

        if delay_ms > 0:
            await asyncio.sleep(delay_ms / 1000)

    print(f"Requests sent: {sent}")
    print(f"Errors: {failed}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <target_ip_or_fqdn> <target_port>", file=sys.stderr)
        sys.exit(2)

    asyncio.run(run_flood(sys.argv[1], sys.argv[2]))
