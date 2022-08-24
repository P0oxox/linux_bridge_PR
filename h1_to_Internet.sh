#!/bin/bash
brctl addbr br0 ip link set br0 up # add bridge br0
ip netns add ns0 # add ns0

ip link add veth0-ns type veth peer name veth0-br # add pair veth0-ns and veth0-br
ip link set veth0-ns netns ns0 # veth0-ns 接到 ns0
brctl addif br0 veth0-br       # veth0-br 接到 br0

ifconfig veth0-br up 

bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward" 
ip netns exec ns0 ifconfig veth0-ns 192.168.15.2/24 up 

ifconfig br0 up

ip netns exec ns0 ip route add default via 192.168.15.5 
ip addr add 192.168.15.5/24 dev br0

ifconfig enp0s8 up
iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -o enp0s8 -j MASQUERADE
#iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -o enp0s3 -j MASQUERADE
iptables -F
iptables -P FORWARD ACCEPT

# ip netns exec ns0 ping 8.8.8.8
