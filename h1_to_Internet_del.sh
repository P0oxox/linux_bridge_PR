#!/bin/bash
ip netns del ns0
ip link set br0 down
brctl delbr br0
iptables -t nat --delete POSTROUTING 1
iptables -t nat --delete POSTROUTING 2
iptables -t nat --delete POSTROUTING 3
iptables -t nat -v -L -n --line-number

#dconf reset -f /
