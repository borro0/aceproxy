#!/bin/sh

hostname=$(hostname)

../start-engine --client-console & python acehttp.py & bwm-ng -o csv > $hostname.csv &

sleep 15

curl --output /dev/null http://127.0.0.1:8000/pid/0bdf6de85fa5f2473d6a47210c598161d362d201/stream.mp4
