#!/bin/bash

ifdown wlan0
rm /etc/network/interfaces && ln -s /etc/network/interfaces.alcs /etc/network/interfaces
ifup wlan0

rm /etc/rc.local && ln -s /etc/rc.local.alcs /etc/rc.local

update-rc.d nginx disable
update-rc.d hostapd disable
update-rc.d dnsmasq disable
