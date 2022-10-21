# TP3 : On va router des trucs

Au menu de ce TP, on va revoir un peu ARP et IP histoire de **se mettre en jambes dans un environnement avec des VMs**.

Puis on mettra en place **un routage simple, pour permettre à deux LANs de communiquer**.

![Reboot the router](./pics/reboot.jpeg)

## Sommaire

- [TP3 : On va router des trucs](#tp3--on-va-router-des-trucs)
  - [Sommaire](#sommaire)
  - [0. Prérequis](#0-prérequis)
  - [I. ARP](#i-arp)
    - [1. Echange ARP](#1-echange-arp)
    - [2. Analyse de trames](#2-analyse-de-trames)
  - [II. Routage](#ii-routage)
    - [1. Mise en place du routage](#1-mise-en-place-du-routage)
    - [2. Analyse de trames](#2-analyse-de-trames-1)
    - [3. Accès internet](#3-accès-internet)
  - [III. DHCP](#iii-dhcp)
    - [1. Mise en place du serveur DHCP](#1-mise-en-place-du-serveur-dhcp)
    - [2. Analyse de trames](#2-analyse-de-trames-2)

## 0. Prérequis

➜ Pour ce TP, on va se servir de VMs Rocky Linux. 1Go RAM c'est large large. Vous pouvez redescendre la mémoire vidéo aussi.  

➜ Vous aurez besoin de deux réseaux host-only dans VirtualBox :

- un premier réseau `10.3.1.0/24`
- le second `10.3.2.0/24`
- **vous devrez désactiver le DHCP de votre hyperviseur (VirtualBox) et définir les IPs de vos VMs de façon statique**

➜ Les firewalls de vos VMs doivent **toujours** être actifs (et donc correctement configurés).

➜ **Si vous voyez le p'tit pote 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu.**

## I. ARP

Première partie simple, on va avoir besoin de 2 VMs.

| Machine  | `10.3.1.0/24` |
|----------|---------------|
| `john`   | `10.3.1.11`   |
| `marcel` | `10.3.1.12`   |

```schema
   john               marcel
  ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     │
  └─────┘    └───┘    └─────┘
```

> Référez-vous au [mémo Réseau Rocky](../../cours/memo/rocky_network.md) pour connaître les commandes nécessaire à la réalisation de cette partie.

### 1. Echange ARP

🌞**Générer des requêtes ARP**

- effectuer un `ping` d'une machine à l'autre
```
[user1@localhost ~]$ ping 10.3.1.12
PING 10.3.1.12 (10.3.1.12) 56(84) bytes of data.
64 bytes from 10.3.1.12: icmp_seq=1 ttl=64 time=0.723 ms
64 bytes from 10.3.1.12: icmp_seq=2 ttl=64 time=0.767 ms
64 bytes from 10.3.1.12: icmp_seq=3 ttl=64 time=0.859 ms
64 bytes from 10.3.1.12: icmp_seq=4 ttl=64 time=0.957 ms
^C
--- 10.3.1.12 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 0.723/0.826/0.957/0.089 ms

```

```
[user1@localhost ~]$ ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=64 time=0.568 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=64 time=0.806 ms
64 bytes from 10.3.1.11: icmp_seq=3 ttl=64 time=0.758 ms
64 bytes from 10.3.1.11: icmp_seq=4 ttl=64 time=0.919 ms
^C
--- 10.3.1.11 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3067ms
rtt min/avg/max/mdev = 0.568/0.762/0.919/0.126 ms

```
- observer les tables ARP des deux machines
```
[user1@localhost ~]$ ip neigh show
10.3.1.12 dev enp0s3 lladdr 08:00:27:67:7d:fc STALE
10.3.1.0 dev enp0s3 lladdr 0a:00:27:00:00:01 DELAY
```

```
[user1@localhost ~]$ ip neigh show
10.3.1.0 dev enp0s3 lladdr 0a:00:27:00:00:01 DELAY
10.3.1.11 dev enp0s3 lladdr 08:00:27:80:60:1f STALE
```
- repérer l'adresse MAC de `john` dans la table ARP de `marcel` et vice-versa
- prouvez que l'info est correcte (que l'adresse MAC que vous voyez dans la table est bien celle de la machine correspondante)
  - une commande pour voir la MAC de `marcel` dans la table ARP de `john`
  ```
  [user1@localhost ~]$ ip neigh show | grep 10.3.1.12
  10.3.1.12 dev enp0s3 lladdr 08:00:27:67:7d:fc STALE
  ```
  - et une commande pour afficher la MAC de `marcel`, depuis `marcel`
  ```
  [user1@localhost ~]$ ip a | grep 08:00
  link/ether 08:00:27:67:7d:fc brd ff:ff:ff:ff:ff:ff
  ```

### 2. Analyse de trames

🌞**Analyse de trames**

- utilisez la commande `tcpdump` pour réaliser une capture de trame
- videz vos tables ARP, sur les deux machines, puis effectuez un `ping`
```
[user1@localhost ~]$ sudo ip neigh flush all
```

🦈 **Capture réseau `tp3_arp.pcapng`** qui contient un ARP request et un ARP reply

> **Si vous ne savez pas comment récupérer votre fichier `.pcapng`** sur votre hôte afin de l'ouvrir dans Wireshark, et me le livrer en rendu, demandez-moi.

## II. Routage

Vous aurez besoin de 3 VMs pour cette partie. **Réutilisez les deux VMs précédentes.**

| Machine  | `10.3.1.0/24` | `10.3.2.0/24` |
|----------|---------------|---------------|
| `router` | `10.3.1.254`  | `10.3.2.254`  |
| `john`   | `10.3.1.11`   | no            |
| `marcel` | no            | `10.3.2.12`   |

> Je les appelés `marcel` et `john` PASKON EN A MAR des noms nuls en réseau 🌻

```schema
   john                router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └───┘    └─────┘    └───┘    └─────┘
```

### 1. Mise en place du routage

🌞**Activer le routage sur le noeud `router`**

```
[user1@localhost ~]$ sudo firewall-cmd --list-all

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

[sudo] password for user1: 
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3 enp0s8
  sources: 
  services: cockpit dhcpv6-client ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: yes
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
[user1@localhost ~]$ sudo firewall-cmd --get-active-zone
public
  interfaces: enp0s3 enp0s8
[user1@localhost ~]$ sudo firewall-cmd --add-masquerade --zone=public
Warning: ALREADY_ENABLED: masquerade already enabled in 'public'
success
[user1@localhost ~]$ sudo firewall-cmd --add-masquerade --zone=public --permanent
Warning: ALREADY_ENABLED: masquerade
success
```

> Cette étape est nécessaire car Rocky Linux c'est pas un OS dédié au routage par défaut. Ce n'est bien évidemment une opération qui n'est pas nécessaire sur un équipement routeur dédié comme du matériel Cisco.

🌞**Ajouter les routes statiques nécessaires pour que `john` et `marcel` puissent se `ping`**

- il faut taper une commande `ip route add` pour cela, voir mémo
- il faut ajouter une seule route des deux côtés
```
[user1@localhost ~]$ cat /etc/sysconfig/network-scripts/route-enp0s3 
10.3.2.0/24 via 10.3.2.254 dev eth0
```
```
[user1@localhost ~]$ cat /etc/sysconfig/network-scripts/route-enp0s3 
10.3.1.0/24 via 10.3.1.254 dev eth0
```
- une fois les routes en place, vérifiez avec un `ping` que les deux machines peuvent se joindre
```
[user1@localhost ~]$ ping 10.3.2.12
PING 10.3.2.12 (10.3.2.12) 56(84) bytes of data.
64 bytes from 10.3.2.12: icmp_seq=1 ttl=63 time=1.60 ms
64 bytes from 10.3.2.12: icmp_seq=2 ttl=63 time=1.67 ms
64 bytes from 10.3.2.12: icmp_seq=3 ttl=63 time=1.76 ms
64 bytes from 10.3.2.12: icmp_seq=4 ttl=63 time=1.26 ms
^C
--- 10.3.2.12 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3006ms
rtt min/avg/max/mdev = 1.256/1.571/1.759/0.190 ms
```
```
[user1@localhost ~]$ ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=63 time=1.51 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=63 time=1.78 ms
64 bytes from 10.3.1.11: icmp_seq=3 ttl=63 time=1.72 ms
64 bytes from 10.3.1.11: icmp_seq=4 ttl=63 time=1.78 ms
^C
--- 10.3.1.11 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 1.514/1.696/1.777/0.108 ms
```

![THE SIZE](./pics/thesize.png)

### 2. Analyse de trames

🌞**Analyse des échanges ARP**

- videz les tables ARP des trois noeuds
- effectuez un `ping` de `john` vers `marcel`
  - **le `tcpdump` doit être lancé sur la machine `john`**

  ```
  [user1@localhost ~]$ sudo tcpdump -w mon_fichier.pcap
  ```
- essayez de déduire un les échanges ARP qui ont eu lieu
  - en regardant la capture et/ou les tables ARP de tout le monde
- répétez l'opération précédente (vider les tables, puis `ping`), en lançant `tcpdump` sur `marcel`
- **écrivez, dans l'ordre, les échanges ARP qui ont eu lieu, puis le ping et le pong, je veux TOUTES les trames** utiles pour l'échange

> Vous pourriez, par curiosité, lancer la capture sur `marcel` aussi, pour voir l'échange qu'il a effectué de son côté.

🦈 **Capture réseau `tp3_routage_marcel.pcapng` et `tp3_routage_john.pcap`**

### 3. Accès internet

🌞**Donnez un accès internet à vos machines**

- ajoutez une carte NAT en 3ème inteface sur le `router` pour qu'il ait un accès internet
- ajoutez une route par défaut à `john` et `marcel`

  - vérifiez que vous avez accès internet avec un `ping`
  - le `ping` doit être vers une IP, PAS un nom de domaine
```
[user1@localhost ~]$ sudo nano /etc/sysconfig/network
[sudo] password for user1: 
[user1@localhost ~]$ sudo systemctl restart NetworkManager
[user1@localhost ~]$ ping 216.58.198.206
PING 216.58.198.206 (216.58.198.206) 56(84) bytes of data.
64 bytes from 216.58.198.206: icmp_seq=1 ttl=61 time=43.4 ms
64 bytes from 216.58.198.206: icmp_seq=2 ttl=61 time=38.2 ms
64 bytes from 216.58.198.206: icmp_seq=3 ttl=61 time=31.5 ms
^C
--- 216.58.198.206 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 31.538/37.682/43.358/4.836 ms
```

```
[user1@localhost ~]$ ping 216.58.198.206
PING 216.58.198.206 (216.58.198.206) 56(84) bytes of data.
64 bytes from 216.58.198.206: icmp_seq=1 ttl=61 time=58.4 ms
64 bytes from 216.58.198.206: icmp_seq=2 ttl=61 time=45.1 ms
^C
--- 216.58.198.206 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 45.138/51.786/58.435/6.648 ms
```
- donnez leur aussi l'adresse d'un serveur DNS qu'ils peuvent utiliser
  - vérifiez que vous avez une résolution de noms qui fonctionne avec `dig`
  - puis avec un `ping` vers un nom de domaine

```
[user1@localhost ~]$ sudo nano /etc/resolv.conf
[user1@localhost ~]$ dig google.com

; <<>> DiG 9.16.23-RH <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 50963
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;google.com.			IN	A

;; ANSWER SECTION:
google.com.		188	IN	A	142.250.178.142

;; Query time: 87 msec
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Thu Oct 20 18:36:50 CEST 2022
;; MSG SIZE  rcvd: 55

[user1@localhost ~]$ ping google.com
PING google.com (142.250.201.174) 56(84) bytes of data.
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=1 ttl=61 time=95.0 ms
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=2 ttl=61 time=71.2 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 71.210/83.088/94.967/11.878 ms
```

🌞**Analyse de trames**

- effectuez un `ping 8.8.8.8` depuis `john`
- capturez le ping depuis `john` avec `tcpdump`
- analysez un ping aller et le retour qui correspond et mettez dans un tableau :

| ordre | type trame | IP source          | MAC source              | IP destination | MAC destination |     |
|-------|------------|--------------------|-------------------------|----------------|-----------------|-----|
| 1     | ping       | `marcel` `10.3.1.12` | `marcel` `AA:BB:CC:DD:EE` | `8.8.8.8`      | ?               |     |
| 2     | pong       | ...                | ...                     | ...            | ...             | ... |

🦈 **Capture réseau `tp3_routage_internet.pcapng`**

## III. DHCP

On reprend la config précédente, et on ajoutera à la fin de cette partie une 4ème machine pour effectuer des tests.

| Machine  | `10.3.1.0/24`              | `10.3.2.0/24` |
|----------|----------------------------|---------------|
| `router` | `10.3.1.254`               | `10.3.2.254`  |
| `john`   | `10.3.1.11`                | no            |
| `bob`    | oui mais pas d'IP statique | no            |
| `marcel` | no                         | `10.3.2.12`   |

```schema
   john               router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └─┬─┘    └─────┘    └───┘    └─────┘
   dhcp        │
  ┌─────┐      │
  │     │      │
  │     ├──────┘
  └─────┘
```

### 1. Mise en place du serveur DHCP

🌞**Sur la machine `john`, vous installerez et configurerez un serveur DHCP** (go Google "rocky linux dhcp server").

- installation du serveur sur `john`
```
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#

default-lease-time 900;
max-lease-time 10800;
ddns-update-style none;
authoritative;
subnet 10.3.2.0 netmask 255.255.255.0 {
  range 10.3.1.12 10.3.2.200;
  option routers 10.3.1.254;
  option subnet-mask 255.255.255.0;
  option domain-name-servers 8.8.8.8;

}
```
- créer une machine `bob`
- faites lui récupérer une IP en DHCP à l'aide de votre serveur
```
[user1@localhost ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:d3:05:77 brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.12/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 801sec preferred_lft 801sec
    inet 10.3.1.13/24 brd 10.3.1.255 scope global secondary dynamic enp0s3
       valid_lft 876sec preferred_lft 876sec
    inet6 fe80::a00:27ff:fed3:577/64 scope link 
       valid_lft forever preferred_lft forever
```

> Il est possible d'utilise la commande `dhclient` pour forcer à la main, depuis la ligne de commande, la demande d'une IP en DHCP, ou renouveler complètement l'échange DHCP (voir `dhclient -h` puis call me et/ou Google si besoin d'aide).

🌞**Améliorer la configuration du DHCP**

- ajoutez de la configuration à votre DHCP pour qu'il donne aux clients, en plus de leur IP :
  - une route par défaut
  - un serveur DNS à utiliser
- récupérez de nouveau une IP en DHCP sur `bob` pour tester :
  - `bob` doit avoir une IP
    - vérifier avec une commande qu'il a récupéré son IP
    - vérifier qu'il peut `ping` sa passerelle
```
[user1@localhost ~]$ ping 10.3.1.254
PING 10.3.1.254 (10.3.1.254) 56(84) bytes of data.
64 bytes from 10.3.1.254: icmp_seq=1 ttl=64 time=0.652 ms
64 bytes from 10.3.1.254: icmp_seq=2 ttl=64 time=1.01 ms
64 bytes from 10.3.1.254: icmp_seq=3 ttl=64 time=0.658 ms
^C
--- 10.3.1.254 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 0.652/0.773/1.009/0.166 ms
[user1@localhost ~]$ 
```
  - il doit avoir une route par défaut
    - vérifier la présence de la route avec une commande
```
[user1@localhost ~]$ ip r s
default via 10.3.1.254 dev enp0s3 
default via 10.3.1.254 dev enp0s3 proto dhcp src 10.3.1.12 metric 100 
```

   

```
[user1@localhost ~]$ ping 142.250.201.174
PING 142.250.201.174 (142.250.201.174) 56(84) bytes of data.
64 bytes from 142.250.201.174: icmp_seq=1 ttl=61 time=33.3 ms
64 bytes from 142.250.201.174: icmp_seq=2 ttl=61 time=33.8 ms
64 bytes from 142.250.201.174: icmp_seq=3 ttl=61 time=25.8 ms
^C
--- 142.250.201.174 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 25.789/30.966/33.826/3.667 ms
```
  - il doit connaître l'adresse d'un serveur DNS pour avoir de la résolution de noms
    - vérifier avec la commande `dig` que ça fonctionne

```
[user1@localhost ~]$ dig google.com

; <<>> DiG 9.16.23-RH <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 36008
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;google.com.			IN	A

;; ANSWER SECTION:
google.com.		300	IN	A	142.250.179.78

;; Query time: 31 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Fri Oct 21 14:51:49 CEST 2022
;; MSG SIZE  rcvd: 55
```
```
[user1@localhost ~]$ ping google.com
PING google.com (142.250.74.238) 56(84) bytes of data.
64 bytes from par10s40-in-f14.1e100.net (142.250.74.238): icmp_seq=1 ttl=61 time=24.6 ms
64 bytes from par10s40-in-f14.1e100.net (142.250.74.238): icmp_seq=2 ttl=61 time=39.9 ms
64 bytes from par10s40-in-f14.1e100.net (142.250.74.238): icmp_seq=3 ttl=61 time=24.6 ms
^C
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 24.583/29.697/39.876/7.197 ms
```

### 2. Analyse de trames

🌞**Analyse de trames**

- lancer une capture à l'aide de `tcpdump` afin de capturer un échange DHCP
- demander une nouvelle IP afin de générer un échange DHCP
- exportez le fichier `.pcapng`

🦈 **Capture réseau `tp3_dhcp.pcapng`**

