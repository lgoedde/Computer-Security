from Goedde_hw08 import *
spoofIP = '192.168.1.1'
targetIP = '192.168.0.10'
Tcp = TcpAttack(spoofIP,targetIP)
Tcp.scanTarget(1,1024)
if (Tcp.attackTarget(904)):
    print("Port was open to attack")