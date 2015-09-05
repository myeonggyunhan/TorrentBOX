#!/bin/bash
sudo usermod -a -G leap nginx
chmod 710 /home/leap

sudo systemctl start nginx
sudo systemctl start uwsgi

sudo systemctl enable nginx
sudo systemctl enable uwsgi

# Set firewall and SELinux rule for nginx
sudo firewall-cmd --permanent --zone=public --add-service=http 
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload

# Allow static file read
sudo setsebool -P httpd_read_user_content 1

# Allow unix socket
yum install -y policycoreutils-{python,devel}
grep nginx /var/log/audit/audit.log | audit2allow -M nginx
semodule -i nginx.pp
usermod -a -G leap nginx
chmod g+rx /home/leap/


# Set firewall and SELinux rule for rabbitmq
sudo firewall-cmd --permanent --add-port=5672/tcp
sudo firewall-cmd --reload
sudo setsebool -P nis_enabled 1
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
