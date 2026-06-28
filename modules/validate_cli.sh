#!/usr/bin/env bash

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$REPO_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
CLI="$PYTHON_BIN $REPO_DIR/attackzoo.py"

# Colors ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
fail() { echo -e "${RED}[FAIL]${NC} $*"; FAILURES=$((FAILURES+1)); }

FAILURES=0

# Setup mode ───────────────────────────────────────────────────────────────
if [[ "${1:-}" == "setup" ]]; then
    echo "=== Setup: Ubuntu Linux ==="

    echo "Checking Python 3..."
    python3 --version

    echo "Installing python3-pip and python3-venv..."
    sudo apt-get update -q
    sudo apt-get install -y -q python3-pip python3-venv

    echo "Creating virtualenv at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"

    echo "Installing dependencies..."
    "$VENV_DIR/bin/pip" install --upgrade pip -q
    "$VENV_DIR/bin/pip" install -r "$REPO_DIR/requirements.txt" -q

    echo ""
    ok "Setup complete!"
    echo "Run now: ./validate_cli.sh"
    echo "With Docker:    ./validate_cli.sh --docker"
    echo "With target:      ./validate_cli.sh --docker --target <IP>"
    exit 0
fi

# Argument parsing ──────────────────────────────────────────────────────
WITH_DOCKER=false
TARGET_IP=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --docker) WITH_DOCKER=true; shift ;;
        --target) TARGET_IP="${2:-}"; shift 2 ;;
        *) shift ;;
    esac
done

echo "=== CLI validation - SBSeg2026 attacks ==="
echo "Directory: $REPO_DIR"
[[ -n "$TARGET_IP" ]] && echo "Target:       $TARGET_IP"
echo ""

# Check virtualenv
if [[ ! -f "$PYTHON_BIN" ]]; then
    echo -e "${RED}[ERROR]${NC} Virtualenv not found at $VENV_DIR"
    echo "Run first: ./validate_cli.sh setup"
    exit 1
fi

echo "Python: $($PYTHON_BIN --version)"
echo ""

# Tests without Docker ────────────────────────────────────────────────────────
echo "-- Tests without Docker ──────────────────────────────────────────────────"

echo -n "[1] list (full catalog)... "
if $CLI list > /tmp/cli_list_out.txt 2>&1; then
    ok
else
    fail; cat /tmp/cli_list_out.txt
fi

echo -n "[2] Attack count (expected: >=40)... "
COUNT=$($CLI list --json 2>/dev/null | python3 -c "import sys,json; data=json.load(sys.stdin); print(sum(len(v) for v in data.values()))" 2>/dev/null || echo 0)
if [[ "$COUNT" -ge 40 ]]; then
    ok "$COUNT attacks loaded"
else
    fail "Only $COUNT attacks (expected >=40)"
fi

echo -n "[3] list --json (valid JSON output)... "
if $CLI list --json 2>/dev/null | python3 -m json.tool > /dev/null 2>&1; then
    ok
else
    fail "Invalid JSON"
fi

echo -n "[4] list --category DoS... "
OUTPUT=$($CLI list --category "DoS" 2>&1)
if echo "$OUTPUT" | grep -qi "dos\|flood\|syn\|udp\|icmp" 2>/dev/null; then
    ok
else
    fail "No DoS attack found in the output"
fi

echo -n "[5] list --category IoT... "
OUTPUT=$($CLI list --category "IoT" 2>&1)
if echo "$OUTPUT" | grep -qi "iot\|mqtt\|coap" 2>/dev/null; then
    ok
else
    fail "No IoT attack found in the output"
fi

echo -n "[6] list --id dos_syn_flood... "
OUTPUT=$($CLI list --id dos_syn_flood 2>&1)
if echo "$OUTPUT" | grep -qi "syn" 2>/dev/null; then
    ok
else
    fail "ID dos_syn_flood not found"
fi

echo -n "[7] run --help (shows --target)... "
OUTPUT=$($CLI run --help 2>&1)
if echo "$OUTPUT" | grep -q "\-\-target" 2>/dev/null; then
    ok
else
    fail "--target does not appear in help"
fi

echo ""

# Docker tests ────────────────────────────────────────────────────────
if $WITH_DOCKER; then

    echo "-- Docker tests (infrastructure) ───────────────────────────────────────"

    echo -n "[8] status (docker_available=true)... "
    OUTPUT=$($CLI status 2>&1)
    if echo "$OUTPUT" | grep -qi "docker_available.*true\|true" 2>/dev/null; then
        ok
    else
        fail "Docker unavailable or unexpected status"
        echo "    Output: $OUTPUT"
        echo "    Tente: sudo service docker start"
    fi

    echo -n "[9] ps --all (lista containers)... "
    if $CLI ps --all > /tmp/cli_ps_out.txt 2>&1; then
        ok
    else
        fail; cat /tmp/cli_ps_out.txt
    fi

    echo ""

    # Type: CONTINUOUS ──────────────────────────────────────────────────────────
    echo "-- Docker tests - CONTINUOUS: dos_syn_flood ──────────────────────────────"
    echo "   Continuous attacks stay alive indefinitely."
    echo "   Validate with: docker ps -> container appears in the list."
    echo ""

    docker rm -f attack-syn-flood > /dev/null 2>&1 || true

    echo -n "[10] run dos_syn_flood --target 127.0.0.1 --duration 5... "
    OUTPUT=$($CLI run dos_syn_flood --target 127.0.0.1 --duration 5 2>&1)
    if echo "$OUTPUT" | grep -qi "\[OK\]" 2>/dev/null; then
        ok
    else
        if echo "$OUTPUT" | grep -qi "unable to find image\|not found\|pull" 2>/dev/null; then
            warn "Image not built - run: cd docker && ./build-images.sh"
        else
            fail "Unexpected output: $OUTPUT"
        fi
    fi

    echo -n "[11] logs dos_syn_flood (hping3 active)... "
    LOGS=$($CLI logs dos_syn_flood 2>&1)
    if echo "$LOGS" | grep -qi "sent\|packet\|hping\|flood" 2>/dev/null; then
        ok "hping3 found in logs"
    else
        warn "No flood output (OK if the image is not built)"
    fi

    docker rm -f attack-syn-flood > /dev/null 2>&1 || true
    echo ""

    # Type: ONE-SHOT ──────────────────────────────────────────────────────────
    echo "-- Docker tests - ONE-SHOT: recon_port_scanner_tcp ─────────────────────"
    echo "   One-shot attacks run the tool and exit on their own."
    echo "   Do not use --duration. Wait for output with docker wait, then check logs."
    echo ""

    docker rm -f attack-port-scanner-tcp > /dev/null 2>&1 || true

    echo -n "[12] run recon_port_scanner_tcp --target 127.0.0.1 (without --duration)... "
    OUTPUT=$($CLI run recon_port_scanner_tcp --target 127.0.0.1 2>&1)
    if echo "$OUTPUT" | grep -qi "\[OK\]\|started" 2>/dev/null; then
        ok "Container started"
    else
        if echo "$OUTPUT" | grep -qi "unable to find image\|not found\|pull" 2>/dev/null; then
            warn "Image not built - run: cd docker && ./build-images.sh"
        else
            fail "Unexpected output: $OUTPUT"
        fi
    fi

    echo -n "[13] docker wait (wait for container exit, 60s timeout)... "
    if timeout 60 docker wait attack-port-scanner-tcp > /dev/null 2>&1; then
        ok "Container exited normally"
    else
        warn "Timeout - nmap may be taking longer (run manually to confirm)"
    fi

    echo -n "[14] logs recon_port_scanner_tcp (check nmap output)... "
    LOGS=$(docker logs attack-port-scanner-tcp 2>&1)
    if echo "$LOGS" | grep -qi "nmap\|Nmap done\|PORT\|open\|closed\|filtered" 2>/dev/null; then
        ok "nmap output found in logs"
    else
        fail "No nmap output - check manually: docker logs attack-port-scanner-tcp"
        echo "    Collected logs: $(echo "$LOGS" | head -3)"
    fi

    docker rm -f attack-port-scanner-tcp > /dev/null 2>&1 || true
    echo ""

    # Type: BRUTE FORCE (requires --target) ────────────────────────────────────
    if [[ -n "$TARGET_IP" ]]; then
        echo "-- Docker tests - BRUTE FORCE: iot_mqtt_bruteforce (target: $TARGET_IP) --"
        echo "   Brute-force attacks run until the wordlist is exhausted or they are stopped."
        echo "   Validate with: docker ps (live container) + docker logs (attempts)."
        echo ""

        docker rm -f attack-mqtt-bruteforce > /dev/null 2>&1 || true

        echo -n "[15] run iot_mqtt_bruteforce --target $TARGET_IP --duration 10... "
        OUTPUT=$($CLI run iot_mqtt_bruteforce --target "$TARGET_IP" --duration 10 2>&1)
        if echo "$OUTPUT" | grep -qi "\[OK\]" 2>/dev/null; then
            ok "Container started"
        else
            if echo "$OUTPUT" | grep -qi "unable to find image\|not found\|pull" 2>/dev/null; then
                warn "Image not built - run: cd docker && ./build-images.sh"
            else
                fail "Unexpected output: $OUTPUT"
            fi
        fi

        echo -n "[16] logs iot_mqtt_bruteforce (login attempts)... "
        sleep 3
        LOGS=$(docker logs attack-mqtt-bruteforce 2>&1)
        if echo "$LOGS" | grep -qi "try\|attempt\|fail\|success\|login\|connect\|mqtt\|password" 2>/dev/null; then
            ok "Brute-force activity found in logs"
        else
            warn "No output yet (normal if the broker takes time to respond)"
            echo "    Logs: $(echo "$LOGS" | head -3)"
        fi

        docker rm -f attack-mqtt-bruteforce > /dev/null 2>&1 || true
        echo ""
    else
        echo "-- Docker tests - BRUTE FORCE (skipped) ───────────────────────────────"
        echo "   Requires a running target server. Add --target IP to enable."
        echo "   Example: ./validate_cli.sh --docker --target 172.17.0.3"
        echo ""
    fi

else
    echo "-- Docker tests (skipped) ─────────────────────────────────────────"
    echo "    Run './validate_cli.sh --docker' to include them."
    echo ""
fi

# Summary ───────────────────────────────────────────────────────────────────
echo "═════════════════════════════════════════════════════════════════════════"
if [[ "$FAILURES" -eq 0 ]]; then
    ok "All tests passed!"
else
    fail "$FAILURES test(s) failed."
    exit 1
fi
