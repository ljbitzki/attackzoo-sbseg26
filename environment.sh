#!/usr/bin/env bash

if [ "${#}" -lt 1 ] || [ "${#}" -gt 2 ]; then
    echo "An action argument is required (start, stop, or restart)"
    echo "$0 restart [all|redux] or $0 stop [all|redux]"
    exit 1
fi

ACTION="${1}"
PROFILE="${2:-all}"

case "${PROFILE}" in
    all|full|redux)
        ;;
    *)
        echo "Unknown server profile: ${PROFILE}"
        echo "$0 restart [all|redux] or $0 stop [all|redux]"
        exit 1
        ;;
esac

function RESTART {
    SLPID=$( sudo ps aux | grep 'streamlit' | grep -v grep | awk '{print $2}' )
    if [[ -z "${SLPID}" ]]; then
        ./servers.sh restart "${PROFILE}"
        source .venv/bin/activate
        streamlit run modules/attackzoo_st.py --theme.base="dark" --server.headless true &
    else
        sudo kill "${SLPID}"
        ./servers.sh restart "${PROFILE}"
        source .venv/bin/activate
        streamlit run modules/attackzoo_st.py --theme.base="dark" --server.headless true &
    fi
}

function STOP {
	./servers.sh stop "${PROFILE}"
	if [[ -n $( which deactivate ) ]]; then
		deactivate
	fi
	SLPID=$( sudo ps aux | grep 'streamlit' | grep -v grep | awk '{print $2}' )
	if [[ -n "${SLPID}" ]]; then
		kill "${SLPID}"
	fi
}

case "${ACTION}" in
    restart)
        RESTART
        ;;
    stop)
	    STOP
	    ;;
    *)
        echo "An action argument is required (start, stop, or restart)"
        ;;
esac
