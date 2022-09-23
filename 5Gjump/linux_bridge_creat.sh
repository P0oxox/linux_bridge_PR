#!/bin/bash
sudo service network-manager start
sudo nmcli con add ifname br0 type bridge con-name br0


# ip link add br-eth1 type veth peer name h-eth1
# ip link add br-eth2 type veth peer name h-eth2
ip link add br-eth3 type veth peer name h-eth3

# nmcli con add type bridge-slave ifname br-eth1 master br0
# nmcli con add type bridge-slave ifname br-eth2 master br0
nmcli con add type bridge-slave ifname br-eth3 master br0


bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward" 
# ip netns add h1 
# ip netns exec h1 ifconfig h-eth1 192.168.15.2/24 up 
# ip netns exec h1 ip route add default via 192.168.15.5 
# ifconfig br0 up
# ip addr add 192.168.15.5/24 dev br0

sudo nmcli con modify br0 bridge.stp no
sudo nmcli con modify br0 ipv4.addresses '192.168.0.1/24'
sudo nmcli con modify br0 ipv4.method manual
sudo nmcli con up br0
sudo nmcli con up bridge-slave-br-eth3

# iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -o enp0s8 -j MASQUERADE
# iptables -F
# iptables -P FORWARD ACCEPT