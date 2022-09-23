#!/bin/bash

ifconfig enp0s8 0.0.0.0
echo 'enp0s8 turn-off for 3 secnds.....'
sleep 3
netplan apply
sleep 1
ifmetric enp0s8 0
ifmetric enp0s3 1
iptables -t nat --delete POSTROUTING 1
iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -o enp0s8 -j MASQUERADE
echo 'enp0s8 recovery'
