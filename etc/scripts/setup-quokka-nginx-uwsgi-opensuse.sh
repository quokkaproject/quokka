#!/bin/bash
# Author: Nilton OS -- www.linuxpro.com.br
# Version: 0.5

echo 'setup-quokka-nginx-uwsgi-opensuse.sh'
echo 'Support OpenSUSE  12.X, 13.X'
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
zypper in -y gcc make mongodb git-core sudo nginx python-devel libjpeg8-devel
zypper in -y python-pip python-virtualenv pcre-devel python-imaging

## Start MongoDB
/etc/init.d/mongodb start
chkconfig --add mongodb

## Create VirtualEnv and User Quokka
if [[ $SUSE_VERSION == '12.2' ]]; then
    groupadd quokka
    useradd -m -g quokka --system -s /bin/sh -c 'Quokka' quokka
else
    useradd -m -U --system -s /bin/sh -c 'Quokka' quokka
fi

cd /home/quokka
virtualenv quokka-env
cd quokka-env
git clone https://github.com/quokkaproject/quokka
cd quokka

/home/quokka/quokka-env/bin/pip install -r requirements/requirements.txt
chown -R quokka:quokka /home/quokka


## Populating with sample data
/home/quokka/quokka-env/bin/python manage.py populate


## Install uWSGI
pip install --upgrade uwsgi

# Prepare folders for uwsgi
mkdir -p /etc/uwsgi && mkdir -p /var/log/uwsgi

usermod -a -G www nginx
mkdir -p /etc/nginx/vhosts.d && mkdir -p /etc/nginx/ssl



echo 'server {
        listen          YOUR_SERVER_IP:80;
        server_name     YOUR_SERVER_FQDN;

         ## Send File Upload via HTTP
		 client_body_in_file_only clean;
		 client_body_buffer_size 32K;
		 client_max_body_size 20M;
		 sendfile on;
         send_timeout 300s;

        location ~ ^/(static|mediafiles)/ {
            root    /home/quokka/quokka-env/quokka/quokka;
            ## Security
            ## location ~* ^.+.(py|pyc|sh|bat|ini|pot|git)$ {deny all; }
            expires 7d;
        }

        location / {
            uwsgi_pass      unix:/home/quokka/quokka-env/quokka/etc/quokka.socket;
            include         /etc/nginx/uwsgi_params;
            uwsgi_param     UWSGI_SCHEME $scheme;
            uwsgi_param     SERVER_SOFTWARE    nginx/$nginx_version;
        }
}' >/etc/nginx/vhosts.d/quokka.conf


sed -i "s/YOUR_SERVER_IP/$SERVER_IP/" /etc/nginx/vhosts.d/quokka.conf
sed -i "s/YOUR_SERVER_FQDN/$SERVER_FQDN/" /etc/nginx/vhosts.d/quokka.conf


# Create configuration file /etc/uwsgi/quokka.ini
echo '[uwsgi]
chmod-socket = 666
virtualenv = /home/quokka/quokka-env
mount  = /=wsgi:application
chdir  = /home/quokka/quokka-env/quokka
socket = /home/quokka/quokka-env/quokka/etc/logs/%n.socket
stats  = /home/quokka/quokka-env/quokka/etc/logs/%n.stats.socket
logto  = /home/quokka/quokka-env/quokka/etc/logs/%n.log
workers = 4
uid = quokka
gid = quokka
max-requests = 2000
limit-as = 512
reload-on-as = 256
reload-on-rss = 192
' >/etc/uwsgi/quokka.ini




## Daemons /start/stop

echo '#!/bin/sh
# Author: Nilton OS -- www.linuxpro.com.br
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
