#!/bin/sh
TARGET="${1}"
PORT="${2}"
/app/dalfox url --url http://${TARGET}:${PORT}/login.php\?cat\=123\&artist\=123\&asdf\=ff --custom-payload /app/XSS-payloadbox.txt
