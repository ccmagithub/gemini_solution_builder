#!/bin/bash

HOSTNAME=`hostname`
echo $HOSTNAME > /etc/salt/minion_id
echo "127.0.0.1 $HOSTNAME localhost" > /etc/hosts
echo "127.0.0.1 $HOSTNAME" >> /etc/hosts
sed -i 's/master: salt_master_ip/master: $PORTAL_IP/g' /etc/salt/minion
rm -rf /etc/salt/pki/minion/*
/etc/init.d/salt-minion stop
pkill salt-minion
salt-minion -d
