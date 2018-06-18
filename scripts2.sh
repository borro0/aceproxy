#!/bin/sh

./acestream/start-engine --client-console & python ./acestream/aceproxy/acehttp.py &

sleep 10

curl --output /dev/null http://127.0.0.1:8000/pid/31ed3696c78bf651c25a8759803c6345912a2a9e/stream.mp4
