#!/bin/sh

./acestream/start-engine --client-console & python ./acestream/aceproxy/acehttp.py &

sleep 10

curl --output /dev/null http://127.0.0.1:8000/pid/a399b7e2920975a72afe9854f269a1ecad77af2d/stream.mp4
