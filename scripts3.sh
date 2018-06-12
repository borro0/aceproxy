#!/bin/sh

echo "starting stream....."
vlc -vvv bbb_sunflower_1080p_30fps_normal.mp4 --sout '#standard{access=http, mux=ts, dst=0.0.0.0:9999/stream}'
./start-engine --stream-source-node --name test --source http://localhost:9999/stream --bitrate 320000 --publish-dir '/var/www/html/ace' --allow-public-trackers 1 --title test --quality HD --category entertaining
