#!/bin/bash
ip netns del ns0
ip link set br0 down
brctl delbr br0

iptables -t nat --delete POSTROUTING 1
