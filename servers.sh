#!/usr/bin/env bash

if [ "${#}" -lt 1 ] || [ "${#}" -gt 2 ]; then
    echo "An action argument is required (start, stop, or restart)"
    echo "$0 stop [all|redux] or $0 start [all|redux] or $0 restart [all|redux]"
    exit 1
fi

ACTION="${1}"
PROFILE="${2:-all}"

case "${PROFILE}" in
    all|full|redux)
        ;;
    *)
        echo "Unknown server profile: ${PROFILE}"
        echo "$0 stop [all|redux] or $0 start [all|redux] or $0 restart [all|redux]"
        exit 1
        ;;
esac

ALL_REQUIRED_IMAGES=(
    server-http-server
    server-ssh-server
    server-smb-server
    server-mqtt-broker
    server-coap-server
    server-xrce-dds-agent
    server-zenoh-router
    server-telnet-server
    server-ssl-heartbleed
)

REDUX_REQUIRED_IMAGES=(
    server-http-server
    server-ssh-server
    server-mqtt-broker
)

if [ "${PROFILE}" = "redux" ]; then
    REQUIRED_IMAGES=("${REDUX_REQUIRED_IMAGES[@]}")
    BUILD_PROFILE="redux"
else
    REQUIRED_IMAGES=("${ALL_REQUIRED_IMAGES[@]}")
    BUILD_PROFILE="full"
fi

for IMAGE in "${REQUIRED_IMAGES[@]}"; do
    if [ "$( docker images -q "${IMAGE}:latest" | wc -l )" -eq 0 ]; then
        echo "Missing server image: ${IMAGE}:latest. Run ./build.sh ${BUILD_PROFILE} to rebuild the images."
        exit 1
    fi
done

function PROFILE_INCLUDES {
    if [ "${PROFILE}" != "redux" ]; then
        return 0
    fi
    case "${1}" in
        server-http-server|server-ssh-server|server-mqtt-broker)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

function STOP {
    if [ "${PROFILE}" = "redux" ]; then
        local servers=()
        mapfile -t servers < <( docker ps -a --format '{{.Names}}' | grep -E '^server-(http-server|ssh-server|mqtt-broker)$' || true )
        if [ "${#servers[@]}" -gt 0 ]; then
            docker rm -f "${servers[@]}"
        fi
        return
    fi
    while read -r SERVER; do
        docker rm -f "${SERVER}"
    done < <( docker ps -a | grep 'server-' | awk '{print $1}' )
}

function START {
    if PROFILE_INCLUDES server-http-server && [ $( docker ps -a | grep -c 'server-http-server') -eq 0 ]; then
        docker run -d --rm --name server-http-server -p 8080:80 server-http-server:latest
    fi
    if PROFILE_INCLUDES server-ssh-server && [ $( docker ps -a | grep -c 'server-ssh-server') -eq 0 ]; then
        docker run -d --rm --name server-ssh-server -p 2222:22 server-ssh-server:latest
    fi
    if PROFILE_INCLUDES server-smb-server && [ $( docker ps -a | grep -c 'server-smb-server') -eq 0 ]; then
        docker run -it -d --rm --name server-smb-server -p 139:139 -p 445:445 -p 137:137/udp -p 138:138/udp server-smb-server:latest  -g "log level = 3" -s "public;/share" -u "example2;badpass"
    fi
    if PROFILE_INCLUDES server-mqtt-broker && [ $( docker ps -a | grep -c 'server-mqtt-broker') -eq 0 ]; then
        docker run -d --rm --name server-mqtt-broker -p 1883:1883 -p 9001:9001 server-mqtt-broker:latest
    fi
    if PROFILE_INCLUDES server-coap-server && [ $( docker ps -a | grep -c 'server-coap-server') -eq 0 ]; then
        docker run -d --rm --name server-coap-server -p 5683:5683 -p 5683:5683/udp server-coap-server:latest
    fi
    if PROFILE_INCLUDES server-xrce-dds-agent && [ $( docker ps -a | grep -c 'server-xrce-dds-agent') -eq 0 ]; then
        docker run -d --rm -p 8888:8888/udp --name server-xrce-dds-agent server-xrce-dds-agent:latest "udp4" "-p" "8888"
    fi
    if PROFILE_INCLUDES server-zenoh-router && [ $( docker ps -a | grep -c 'server-zenoh-router') -eq 0 ]; then
        docker run -d --rm --name server-zenoh-router -p 7447:7447 server-zenoh-router:latest
    fi
    if PROFILE_INCLUDES server-telnet-server && [ $( docker ps -a | grep -c 'server-telnet-server') -eq 0 ]; then
        docker run -d --rm --name server-telnet-server -p 2323:23 server-telnet-server:latest
    fi
    if PROFILE_INCLUDES server-ssl-heartbleed && [ $( docker ps -a | grep -c 'server-ssl-heartbleed') -eq 0 ]; then
        docker run -d --rm --name server-ssl-heartbleed -p 8443:443 server-ssl-heartbleed:latest
    fi
}

case ${ACTION} in
    stop)
        STOP
        ;;
    start)
        START
        ;;
    restart)
        STOP
        START
        ;;
    *)
        echo "An action argument is required (start, stop, or restart)"
        ;;
esac
exit 0
