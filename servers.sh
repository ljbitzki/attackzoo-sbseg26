#!/usr/bin/env bash

if [ "${#}" -ne 1 ]; then
    echo "An action argument is required (start, stop, or restart)"
    echo "$0 stop or $0 start or $0 restart"
    exit 1
fi

REQUIRED_IMAGES=(
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

for IMAGE in "${REQUIRED_IMAGES[@]}"; do
    if [ "$( docker images -q "${IMAGE}:latest" | wc -l )" -eq 0 ]; then
        echo "Missing server image: ${IMAGE}:latest. Run cd docker && ./build-images.sh to rebuild the images."
        exit 1
    fi
done

function STOP {
    while read -r SERVER; do
        docker rm -f "${SERVER}"
    done < <( docker ps -a | grep 'server-' | awk '{print $1}' )
}

function START {
    if [ $( docker ps -a | grep -c 'server-http-server') -eq 0 ]; then
        docker run -d --rm --name server-http-server -p 8080:80 server-http-server:latest
    fi
    if [ $( docker ps -a | grep -c 'server-ssh-server') -eq 0 ]; then
        docker run -d --rm --name server-ssh-server -p 2222:22 server-ssh-server:latest
    fi
    if [ $( docker ps -a | grep -c 'server-smb-server') -eq 0 ]; then
        docker run -it -d --rm --name server-smb-server -p 139:139 -p 445:445 -p 137:137/udp -p 138:138/udp server-smb-server:latest  -g "log level = 3" -s "public;/share" -u "example2;badpass"
    fi
    if [ $( docker ps -a | grep -c 'server-mqtt-broker') -eq 0 ]; then
        docker run -d --rm --name server-mqtt-broker -p 1883:1883 -p 9001:9001 server-mqtt-broker:latest
    fi
    if [ $( docker ps -a | grep -c 'server-coap-server') -eq 0 ]; then
        docker run -d --rm --name server-coap-server -p 5683:5683 -p 5683:5683/udp server-coap-server:latest
    fi
    if [ $( docker ps -a | grep -c 'server-xrce-dds-agent') -eq 0 ]; then
        docker run -d --rm -p 8888:8888/udp --name server-xrce-dds-agent server-xrce-dds-agent:latest "udp4" "-p" "8888"
    fi
    if [ $( docker ps -a | grep -c 'server-zenoh-router') -eq 0 ]; then
        docker run -d --rm --name server-zenoh-router -p 7447:7447 server-zenoh-router:latest
    fi
    if [ $( docker ps -a | grep -c 'server-telnet-server') -eq 0 ]; then
        docker run -d --rm --name server-telnet-server -p 2323:23 server-telnet-server:latest
    fi
    if [ $( docker ps -a | grep -c 'server-ssl-heartbleed') -eq 0 ]; then
        docker run -d --rm --name server-ssl-heartbleed -p 8443:443 server-ssl-heartbleed:latest
    fi
}

case ${1} in
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
