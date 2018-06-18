#!/bin/sh

#install openssh
sudo apt-get update
sudo apt install git -y
sudo apt install vim -y
sudo apt-get install openssh-server -y
sudo service ssh restart -y
sudo apt install python-pip -y
sudo apt install python-gevent -y
sudo apt install python-psutil -y
# sudo apt install python-apscheduler
sudo apt install curl -y
sudo pip install apscheduler -y
sudo apt install ntp -y

#install acestream
echo "installing acestream...."
wget http://dl.acestream.org/linux/acestream_3.1.16_ubuntu_16.04_x86_64.tar.gz
tar zxvf acestream_3.1.16_ubuntu_16.04_x86_64.tar.gz
sudo apt-get install python-setuptools python-m2crypto python-apsw -y
mv acestream_3.1.16_ubuntu_16.04_x86_64 acestream
cd acestream

echo "installing vlc and apache...."
sudo apt install vlc apache2 -y
sudo service apache2 restart -y
wget http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_30fps_normal.mp4

git clone https://github.com/borro0/aceproxy.git
