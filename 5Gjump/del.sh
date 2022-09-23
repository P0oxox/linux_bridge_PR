#!/bin/bash
# 好像刪不乾淨
# ip link set br0 down
# brctl delbr br0
ip netns del h1
nmcli connection delete br0
sudo nmcli connection delete bridge-slave-br-eth1
sudo nmcli connection delete bridge-slave-br-eth2
sudo nmcli connection delete bridge-slave-br-eth3
# brctl show