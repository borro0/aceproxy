#!/bin/sh

#install openssh
sudo apt-get update
sudo apt install git
sudo apt install vim
sudo apt-get install openssh-server
sudo service ssh restart
sudo apt install python-pip
sudo apt install python-gevent
sudo apt install python-psutil
# sudo apt install python-apscheduler
sudo apt install curl
sudo pip install apscheduler
sudo apt install ntp

#install acestream
echo "installing acestream...."
wget http://dl.acestream.org/linux/acestream_3.1.16_ubuntu_16.04_x86_64.tar.gz
tar zxvf acestream_3.1.16_ubuntu_16.04_x86_64.tar.gz
sudo apt-get install python-setuptools python-m2crypto python-apsw
mv acestream_3.1.16_ubuntu_16.04_x86_64 acestream
cd acestream

echo "installing vlc and apache...."
sudo apt install vlc apache2
sudo service apache2 restart
wget http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_30fps_normal.mp4

git clone https://github.com/borro0/aceproxy.git
