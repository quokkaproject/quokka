#!/bin/bash
# Autor: Nilton OS -- www.linuxpro.com.br
echo 'setup-quokka-nginx-uwsgi-ubuntu.sh'
echo 'Support Ubuntu/Debian'
echo 'Installs Nginx + uWSGI + Quokka'
echo 'Requires ubuntu 12.04+ and installs nginx + uwsgi'
 
if [[ $EUID -ne 0 ]]; then
   echo "You must run the script as root or using sudo"
   exit 1
fi
 
echo -e "Set Server Name Ex: quokkaproject.domain.com : \c "
read  SERVER_FQDN
 
echo -e "Set Server IP (commonly 127.0.0.1 works): \c "
read  SERVER_IP
 
 
echo "" >>/etc/hosts
echo "$SERVER_IP  $SERVER_FQDN" >>/etc/hosts
 
 
# Upgrade and install needed software
apt-get update
apt-get -y upgrade
apt-get autoremove
apt-get autoclean
apt-get -y install nginx-full mongodb-server git-core python-virtualenv
apt-get -y install build-essential python-dev libxml2-dev python-pip unzip



## Create VirtualEnv and User Quokka
adduser --disabled-login --gecos 'Quokka' quokka
cd /home/quokka
sudo -u quokka -H virtualenv quokka-env
cd quokka-env
source bin/activate
sudo -u quokka -H git clone https://github.com/pythonhub/quokka
cd quokka

chown -R quokka:quokka /home/quokka
/home/quokka/quokka-env/bin/pip install -r requirements.txt
chown -R quokka:quokka /home/quokka

## Populating with sample data
/home/quokka/quokka-env/bin/python manage.py populate

deactivate
## Install uWSGI
PIPPATH=`which pip`
$PIPPATH install --upgrade uwsgi
  
# Prepare folders for uwsgi
mkdir /etc/uwsgi
mkdir /var/log/uwsgi
 
  
 
echo 'server {
        listen          YOUR_SERVER_IP:80;
        server_name     YOUR_SERVER_FQDN;
        location / {
            uwsgi_pass      unix:///tmp/quokka.socket;
            include         /etc/nginx/uwsgi_params;
            uwsgi_param     UWSGI_SCHEME $scheme;
            uwsgi_param     SERVER_SOFTWARE    nginx/$nginx_version;

            ### remove the comments if you use uploads (max 10 MB)
            #client_max_body_size 10m;
            ###
        }
}' >/etc/nginx/sites-available/quokka.conf
 

ln -s /etc/nginx/sites-available/quokka.conf /etc/nginx/sites-enabled/quokka.conf
rm /etc/nginx/sites-enabled/default
mkdir /etc/nginx/ssl

sed -i "s/YOUR_SERVER_IP/$SERVER_IP/" /etc/nginx/sites-available/quokka.conf
sed -i "s/YOUR_SERVER_FQDN/$SERVER_FQDN/" /etc/nginx/sites-available/quokka.conf


# Create configuration file /etc/uwsgi/quokka.ini
echo '[uwsgi]
chmod-socket = 666
chdir = /home/quokka/quokka-env/quokka
virtualenv = /home/quokka/quokka-env
module = wsgi
socket = /tmp/%n.socket
socket = /tmp/%n.sock
logto = /var/log/uwsgi/%n.log
workers = 3
uid = quokka
gid = quokka' >/etc/uwsgi/quokka.ini
 
 
 #Create a configuration file for uwsgi in emperor-mode
#for Upstart in /etc/init/uwsgi-emperor.conf
echo '# Emperor uWSGI script

description "uWSGI Emperor"
start on runlevel [2345]
stop on runlevel [06]
##
#remove the comments in the next section to enable static file compression for the welcome app
#in that case, turn on gzip_static on; on /etc/nginx/nginx.conf
##
#pre-start script
#    chown -R quokka:quokka /home/quokka/*
#end script
respawn
exec uwsgi --master --die-on-term --emperor /etc/uwsgi --logto /var/log/uwsgi/uwsgi.log
' > /etc/init/uwsgi-emperor.conf


start uwsgi-emperor
/etc/init.d/nginx restart

## you can reload uwsgi with
# restart uwsgi-emperor
## and stop it with
# stop uwsgi-emperor
## to reload quokka only (without restarting uwsgi)
# touch /etc/uwsgi/quokka.ini
