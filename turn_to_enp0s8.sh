#!/bin/bash

iptables -t nat --delete POSTROUTING 1
iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -o enp0s8 -j MASQUERADE
ip netns exec ns0 ping 8.8.8.8