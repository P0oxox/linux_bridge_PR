#!/bin/bash
# sudo service network-manager start
# ip link add br-eth3 type veth peer name h-eth3
# nmcli con add type bridge-slave ifname br-eth1 master br0
# ip link add br-eth3 type veth peer name h-eth3
# nmcli con add type bridge-slave ifname br-eth3 master br0


ip netns add h1
ip link set h-eth3 netns h1  #有一個h1插在eth3的port
ip -n h1 addr add 192.168.0.6/24 dev h-eth3 # h1 add ip

ip netns exec h1 ip link set h-eth3 up 
ip netns exec h1 ip route add 192.168.0.0/24 via 192.168.0.1

sudo nmcli con up br0
sudo nmcli con up bridge-slave-br-eth3
ifconfig br-eth3 up


sysctl -w net.ipv4.ip_forward=1
sysctl -p
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o enp0s8 -j MASQUERADE
ip netns exec h1 ip route add default via 192.168.0.1
# ip netns exec h1 ifconfig

#iptables -t nat -L -n -v