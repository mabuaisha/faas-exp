#!/bin/bash

set -e

# Install required packages including vsftpd, ftp,firewall
sudo yum install -y vsftpd ftp firewalld

# setup firewalld & vsftpd services
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo systemctl status firewalld
sudo systemctl start vsftpd
sudo systemctl enable vsftpd

# Configure firewall rules
sudo firewall-cmd --zone=public --permanent --add-port=21/tcp
sudo firewall-cmd --zone=public --permanent --add-service=ftp
sudo firewall-cmd --reload

# Configure FTP Server and user
yes | sudo cp -rf /home/centos/vsftpd.conf /etc/vsftpd/
sudo useradd -m -c “FTP User” -s /bin/bash ${ftp_username}
echo ${ftp_password} | sudo passwd ${ftp_username} --stdin
echo "${ftp_username}" | sudo tee -a /etc/vsftpd/user_list
sudo systemctl restart vsftpd