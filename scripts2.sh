#!/bin/sh

# usage -> 4 arguments -> 

# 1: upload rate with mbit, 
# 2: buffer size with kb, 
# 3: delay with ms, 
# 4: loss with %

# example: sudo ./scripts2.sh 0.5mbit 5kb 1ms 1%
# buffersize should be proportional to rate, so 1mbit -> 10 kb | 10mbit -> 100kb

tc qdisc del dev enp0s3 root
tc qdisc add dev enp0s3 root handle 1:0 netem delay $3 loss $4
tc qdisc add dev enp0s3 parent 1:1 handle 10: tbf rate $1 buffer $2 latency 400ms

hostname=$(hostname)

../start-engine --client-console & python acehttp.py & bwm-ng -o csv > $hostname.csv &

sleep 15

curl --output /dev/null http://127.0.0.1:8000/pid/2e7c5f458b66b3e76719bc6e8a2a851f57de078a/stream.mp4
