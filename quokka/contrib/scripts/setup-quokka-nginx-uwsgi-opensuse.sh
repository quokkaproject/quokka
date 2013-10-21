#!/bin/bash
# Author: Nilton OS -- www.linuxpro.com.br
# Version: 0.4

echo 'setup-quokka-nginx-uwsgi-opensuse.sh'
echo 'Support OpenSUSE  11.X, 12.X, 13.X'
echo 'Installs Nginx + uWSGI + Quokka'

# Check if user has root privileges
if [[ $EUID -ne 0 ]]; then
echo "You must run the script as root or using sudo"
   exit 1
fi
 
SUSE_VERSION=$(cat /etc/issue | awk '{ print $4 }' | head -n1)
 
echo -e "Set Server Name Ex: quokkaproject.domain.com : \c "
read  SERVER_FQDN

echo -e "Set Server IP (commonly 127.0.0.1 works): \c "
read  SERVER_IP
 
 
echo "" >>/etc/hosts
echo "$SERVER_IP  $SERVER_FQDN" >>/etc/hosts
 
 
zypper ar http://download.opensuse.org/repositories/devel:/languages:/python/openSUSE_${SUSE_VERSION}/ devel_python
zypper --no-gpg-checks refresh
zypper in -y gcc make mongodb git-core sudo nginx python-devel python-pip python-virtualenv

## Start MongoDB
/etc/init.d/mongodb start
chkconfig --add mongodb

## Create VirtualEnv and User Quokka
groupadd quokka
useradd -m -G quokka --system -s /bin/sh -c 'Quokka' -d /home/quokka quokka
cd /home/quokka
virtualenv quokka-env
cd quokka-env
git clone https://github.com/pythonhub/quokka
cd quokka

/home/quokka/quokka-env/bin/pip install -r requirements.txt
chown -R quokka:quokka /home/quokka


## Populating with sample data
/home/quokka/quokka-env/bin/python manage.py populate


## Install uWSGI
pip install --upgrade uwsgi
  
# Prepare folders for uwsgi
mkdir /etc/uwsgi && mkdir /var/log/uwsgi
 
usermod -a -G www nginx
mkdir -p /etc/nginx/vhosts.d && mkdir -p /etc/nginx/ssl

 
 
echo 'server {
        listen          YOUR_SERVER_IP:80;
        server_name     YOUR_SERVER_FQDN;

        location ~ ^/(media|static)/ {
            root    /home/quokka/quokka-env/quokka/quokka;
            expires 7d;
        }

        location / {
            uwsgi_pass      unix:///tmp/quokka.socket;
            include         /etc/nginx/uwsgi_params;
            uwsgi_param     UWSGI_SCHEME $scheme;
            uwsgi_param     SERVER_SOFTWARE    nginx/$nginx_version;
            client_max_body_size 40m;
        }
}' >/etc/nginx/vhosts.d/quokka.conf
 
 
sed -i "s/YOUR_SERVER_IP/$SERVER_IP/" /etc/nginx/vhosts.d/quokka.conf
sed -i "s/YOUR_SERVER_FQDN/$SERVER_FQDN/" /etc/nginx/vhosts.d/quokka.conf


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
 
 
 
 
## Daemons /start/stop
 
echo '#!/bin/sh
# Autor: Nilton OS -- www.linuxpro.com.br
#
#
### BEGIN INIT INFO
# Provides:          uwsgi
# Required-Start:    $syslog $remote_fs
# Should-Start:      $time ypbind smtp
# Required-Stop:     $syslog $remote_fs
# Should-Stop:       ypbind smtp
# Default-Start:     3 5
# Default-Stop:      0 1 2 6
# Short-Description: Application Container Server for Networked/Clustered Web Applications
# Description:       Application Container Server for Networked/Clustered Web Applications
### END INIT INFO
 
# Check for missing binaries (stale symlinks should not happen)
UWSGI_BIN=`which uwsgi`
test -x $UWSGI_BIN || { echo "$UWSGI_BIN not installed"; 
        if [ "$1" = "stop" ]; then exit 0;
        else exit 5; fi; }
 
UWSGI_EMPEROR_MODE=true
UWSGI_VASSALS="/etc/uwsgi/"
UWSGI_OPTIONS="--logto /var/log/uwsgi/uwsgi.log"
 
 
UWSGI_OPTIONS="$UWSGI_OPTIONS --autoload"
 
if [ "$UWSGI_EMPEROR_MODE" = "true" ] ; then
    UWSGI_OPTIONS="$UWSGI_OPTIONS --emperor $UWSGI_VASSALS"
fi                
. /etc/rc.status 
rc_reset
 
case "$1" in
    start)
        echo -n "Starting uWSGI "
        /sbin/startproc $UWSGI_BIN $UWSGI_OPTIONS
        rc_status -v
        ;;
    stop)
        echo -n "Shutting down uWSGI "
        /sbin/killproc $UWSGI_BIN
        rc_status -v
        ;;
    restart)
        $0 stop
        $0 start
        rc_status
        ;;
    reload)
        echo -n "Reload service uWSGI "
        /sbin/killproc -HUP $UWSGI_BIN
        rc_status -v
        ;;
    status)
        echo -n "Checking for service uWSGI "
        /sbin/checkproc $UWSGI_BIN
        rc_status -v
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart|reload}"
        exit 1
        ;;
esac
rc_exit '> /etc/init.d/uwsgi
 
chmod +x /etc/init.d/uwsgi
ln -s /etc/init.d/uwsgi /usr/sbin/rcuwsgi
 
/etc/init.d/uwsgi start
/etc/init.d/nginx restart
 
 
chkconfig --add uwsgi
chkconfig --add nginx
  
## you can reload uwsgi with
#/etc/init.d/uwsgi restart
## to reload Quokka only (without restarting uwsgi)
# touch /etc/uwsgi/quokka.ini
