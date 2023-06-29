#!/bin/sh

# release install

sudo apt update
#firmadyne
sudo apt-get install -y busybox-static fakeroot git dmsetup kpartx netcat-openbsd nmap python-psycopg2 python3-psycopg2 snmp uml-utilities util-linux vlan
#firmwalker
npm i -g eslint
