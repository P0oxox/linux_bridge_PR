#!/bin/bash
ifconfig enp0s8 0
nmcli con mod enp0s8 ipv4.addresses 172.30.5.88/24
nmcli con mod enp0s8 ipv4.gateway 172.30.5.1
