#!/usr/bin/env bash

if [ "${#}" -ne 1 ]; then
    echo "An action argument is required (start, stop, or restart)"
    echo "$0 restart"
    exit 1
fi

function RESTART {
    SLPID=$( sudo ps aux | grep 'streamlit' | grep -v grep | awk '{print $2}' )
    if [[ -z "${SLPID}" ]]; then
        ./servers.sh restart
        source .venv/bin/activate
        streamlit run modules/attackzoo_st.py --theme.base="dark" --server.headless true &
    else
        sudo kill "${SLPID}"
        ./servers.sh restart
        source .venv/bin/activate
        streamlit run modules/attackzoo_st.py --theme.base="dark" --server.headless true &
    fi
}

function STOP {
	./servers.sh stop
	if [[ -n $( which deactivate ) ]]; then
		deactivate
	fi
	SLPID=$( sudo ps aux | grep 'streamlit' | grep -v grep | awk '{print $2}' )
	if [[ -n "${SLPID}" ]]; then
		kill "${SLPID}"
	fi
}

case "${1}" in
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
