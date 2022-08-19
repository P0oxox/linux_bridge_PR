#!/bin/bash
ifmetric enp0s8 1
ifmetric enp0s3 0
iptables -t nat --delete POSTROUTING 1
iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -o enp0s3 -j MASQUERADE
ip netns exec ns0 ping 8.8.8.8
