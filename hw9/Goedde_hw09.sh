#! /bin/sh 

#Firewall created by Lucas Goedde

#flush/delete old rules 
iptables -F
iptables -t nat -F

#Place no restriction on outbound packets
iptables -I OUTPUT -j ACCEPT

#Block a list of specific ip addresses (128.46.75.0 to 128.46.75.255)
iptables -A INPUT -m iprange --src-range 128.46.75.0-128.46.75.255 -j DROP

#Block computer from being pinged by all other hosts
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP

#Port-forwarding from unused port to port 22 (first have to open port 3456)
iptables -A INPUT -p tcp --dport 3456 -j ACCEPT
iptables -t nat -A PREROUTING -p tcp --dport 3456 -j REDIRECT --to-ports 22

#Allow ssh to machine only from ecn.purdue.edu
iptables -A INPUT -p tcp --src ecn.purdue.edu --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j REJECT

#Allow only single ip address to access http service
iptables -A INPUT -p tcp --src 10.186.140.146 --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j REJECT

#Permit auth/ident (port 113) for services like SMTP/IRC
iptables -A INPUT -p tcp --dport 113 -j ACCEPT


