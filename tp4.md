# TP4 : TCP, UDP et services réseau

Dans ce TP on va explorer un peu les protocoles TCP et UDP. 

**La première partie est détente**, vous explorez TCP et UDP un peu, en vous servant de votre PC.

La seconde partie se déroule en environnement virtuel, avec des VMs. Les VMs vont nous permettre en place des services réseau, qui reposent sur TCP et UDP.  
**Le but est donc de commencer à mettre les mains de plus en plus du côté administration, et pas simple client.**

Dans cette seconde partie, vous étudierez donc :

- le protocole SSH (contrôle de machine à distance)
- le protocole DNS (résolution de noms)
  - essentiel au fonctionnement des réseaux modernes

![TCP UDP](./pics/tcp_udp.jpg)

# Sommaire

- [TP4 : TCP, UDP et services réseau](#tp4--tcp-udp-et-services-réseau)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. First steps](#i-first-steps)
- [II. Mise en place](#ii-mise-en-place)
  - [1. SSH](#1-ssh)
  - [2. Routage](#2-routage)
- [III. DNS](#iii-dns)
  - [1. Présentation](#1-présentation)
  - [2. Setup](#2-setup)
  - [3. Test](#3-test)

# 0. Prérequis

➜ Pour ce TP, on va se servir de VMs Rocky Linux. On va en faire plusieurs, n'hésitez pas à diminuer la RAM (512Mo ou 1Go devraient suffire). Vous pouvez redescendre la mémoire vidéo aussi.  

➜ Si vous voyez un 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu

➜ **L'emoji 🖥️ indique une VM à créer**. Pour chaque VM, vous déroulerez la checklist suivante :

- [x] Créer la machine (avec une carte host-only)
- [ ] Définir une IP statique à la VM
- [ ] Donner un hostname à la machine
- [ ] Vérifier que l'accès SSH fonctionnel
- [ ] Vérifier que le firewall est actif
- [ ] Remplir votre fichier `hosts`, celui de votre PC, pour accéder au VM avec un nom
- [ ] Dès que le routeur est en place, n'oubliez pas d'ajouter une route par défaut aux autres VM pour qu'elles aient internet

> Toutes les commandes pour réaliser ces opérations sont dans [le mémo Rocky](../../cours/memo/rocky_network.md). Aucune de ces étapes ne doit figurer dan le rendu, c'est juste la mise en place de votre environnement de travail.

# I. First steps

Faites-vous un petit top 5 des applications que vous utilisez sur votre PC souvent, des applications qui utilisent le réseau : un site que vous visitez souvent, un jeu en ligne, Spotify, j'sais po moi, n'importe.

🌞 **Déterminez, pour ces 5 applications, si c'est du TCP ou de l'UDP**

- avec Wireshark, on va faire les chirurgiens réseau
- déterminez, pour chaque application :
  - IP et port du serveur auquel vous vous connectez
  - le port local que vous ouvrez pour vous connecter

> Dès qu'on se connecte à un serveur, notre PC ouvre un port random. Une fois la connexion TCP ou UDP établie, entre le port de notre PC et le port du serveur qui est en écoute, on parle de tunnel TCP ou de tunnel UDP.


> Aussi, TCP ou UDP ? Comment le client sait ? Il sait parce que le serveur a décidé ce qui était le mieux pour tel ou tel type de trafic (un jeu, une page web, etc.) et que le logiciel client est codé pour utiliser TCP ou UDP en conséquence.

🌞 **Demandez l'avis à votre OS**

- votre OS est responsable de l'ouverture des ports, et de placer un programme en "écoute" sur un port
- il est aussi responsable de l'ouverture d'un port quand une application demande à se connecter à distance vers un serveur
- bref il voit tout quoi
- utilisez la commande adaptée à votre OS pour repérer, dans la liste de toutes les connexions réseau établies, la connexion que vous voyez dans Wireshark, pour chacune des 5 applications

**Il faudra ajouter des options adaptées aux commandes pour y voir clair. Pour rappel, vous cherchez des connexions TCP ou UDP.**

```
# MacOS
$ netstat

# GNU/Linux
$ ss -p

# Windows
$ netstat
```

🦈🦈🦈🦈🦈 **Bah ouais, captures Wireshark à l'appui évidemment.** Une capture pour chaque application, qui met bien en évidence le trafic en question.

## Discord:
-Ip du serveur: 162.159.135.234

-Port du serveur: 443

-Port local: 39226

```
tcp                ESTAB               0                   0                                                          10.33.17.89:39226                                162.159.135.234:https                users:(("Discord",pid=6916,fd=87))                                                                                                                                     
```

## Ubuntu Store:
-Ip du serveur: 8.43.85.4

-Port du serveur: 443

-Port local: 44948

```
tcp    ESTAB   0       0                                                                 10.33.17.89:44948                                                         8.43.85.4:https                         users:(("snap-store",pid=2569,fd=29))                                                               
```


## Youtube.com:
-Ip du serveur:142.250.74.230

-Port du serveur:443

-Port local:34096

```
tcp            ESTAB             0               0                                                                                10.33.17.89:34096                         142.250.74.230:https            users:(("firefox",pid=4650,fd=214))                                                                                                                                                                      
```


## Tor browser:
-Ip du serveur: 23.88.75.121

-Port du serveur:9001

-Port local: 45872

```
tcp                ESTAB               0                    536                                                                           10.33.17.75:45872                                     23.88.75.121:19001                               users:(("tor",pid=17719,fd=12))                                                

```

## Crash drive 2:
-Ip du serveur:92.38.154.54

-Port du serveur:5056

-Port local:57619

```
udp            ESTAB               0               0                                                                                10.33.17.75:57619                          92.38.154.54:5056            users:(("Crash Drive 2",pid=18664,fd=44))                                                                                                                                                                 
```

# II. Mise en place

## 1. SSH

🖥️ **Machine `node1.tp4.b1`**

- n'oubliez pas de dérouler la checklist (voir [les prérequis du TP](#0-prérequis))
- donnez lui l'adresse IP `10.4.1.11/24`

Connectez-vous en SSH à votre VM.

🌞 **Examinez le trafic dans Wireshark**

- **déterminez si SSH utilise TCP ou UDP**
[handshake](./3-way-handshake.pcapng)
### 3-way-handshake.pcapng
  - pareil réfléchissez-y deux minutes, logique qu'on utilise pas UDP non ?

  Il utilise TCP car la connexion doit etre securisée afin que les personnes malveillantes ne puissent pas voir ce qu'on fait.
- **repérez le *3-Way Handshake* à l'établissement de la connexion**
  - c'est le `SYN` `SYNACK` `ACK`
- **repérez du trafic SSH**
- **repérez le FIN FINACK à la fin d'une connexion**
- entre le *3-way handshake* et l'échange `FIN`, c'est juste une bouillie de caca chiffré, dans un tunnel TCP

🌞 **Demandez aux OS**

- repérez, avec une commande adaptée (`netstat` ou `ss`), la connexion SSH depuis votre machine
- ET repérez la connexion SSH depuis votre VM

```
tcp                ESTAB               0                    0                                                                                10.4.1.0:44336                                        10.4.1.11:ssh                                                                                                                
```

🦈 **Je veux une capture clean avec le 3-way handshake, un peu de trafic au milieu et une fin de connexion**

## 2. Routage

Ouais, un peu de répétition, ça fait jamais de mal. On va créer une machine qui sera notre routeur, et **permettra à toutes les autres machines du réseau d'avoir Internet.**

🖥️ **Machine `router.tp4.b1`**

- n'oubliez pas de dérouler la checklist (voir [les prérequis du TP](#0-prérequis))
- donnez lui l'adresse IP `10.4.1.11/24` sur sa carte host-only
- ajoutez-lui une carte NAT, qui permettra de donner Internet aux autres machines du réseau
- référez-vous au TP précédent

> Rien à remettre dans le compte-rendu pour cette partie.

# III. DNS

## 1. Présentation

Un serveur DNS est un serveur qui est capable de répondre à des requêtes DNS.

Une requête DNS est la requête effectuée par une machine lorsqu'elle souhaite connaître l'adresse IP d'une machine, lorsqu'elle connaît son nom.

Par exemple, si vous ouvrez un navigateur web et saisissez `https://www.google.com` alors une requête DNS est automatiquement effectuée par votre PC pour déterminez à quelle adresse IP correspond le nom `www.google.com`.

> La partie `https://` ne fait pas partie du nom de domaine, ça indique simplement au navigateur la méthode de connexion. Ici, c'est HTTPS.

Dans cette partie, on va monter une VM qui porte un serveur DNS. Ce dernier répondra aux autres VMs du LAN quand elles auront besoin de connaître des noms. Ainsi, ce serveur pourra :

- résoudre des noms locaux
  - vous pourrez `ping node1.tp4.b1` et ça fonctionnera
  - mais aussi `ping www.google.com` et votre serveur DNS sera capable de le résoudre aussi

*Dans la vraie vie, il n'est pas rare qu'une entreprise gère elle-même ses noms de domaine, voire gère elle-même son serveur DNS. C'est donc du savoir ré-utilisable pour tous qu'on voit ici.*

> En réalité, ce n'est pas votre serveur DNS qui pourra résoudre `www.google.com`, mais il sera capable de *forward* (faire passer) votre requête à un autre serveur DNS qui lui, connaît la réponse.

![Haiku DNS](./pics/haiku_dns.png)

## 2. Setup

🖥️ **Machine `dns-server.tp4.b1`**

- n'oubliez pas de dérouler la checklist (voir [les prérequis du TP](#0-prérequis))
- donnez lui l'adresse IP `10.4.1.201/24`

Installation du serveur DNS :

```bash
# assurez-vous que votre machine est à jour
$ sudo dnf update -y

# installation du serveur DNS, son p'tit nom c'est BIND9
$ sudo dnf install -y bind bind-utils
```

La configuration du serveur DNS va se faire dans 3 fichiers essentiellement :

- **un fichier de configuration principal**
  - `/etc/named.conf`
  - on définit les trucs généraux, comme les adresses IP et le port où on veu écouter
  - on définit aussi un chemin vers les autres fichiers, les fichiers de zone
- **un fichier de zone**
  - `/var/named/tp4.b1.db`
  - je vous préviens, la syntaxe fait mal
  - on peut y définir des correspondances `IP ---> nom`
- **un fichier de zone inverse**
  - `/var/named/tp4.b1.rev`
  - on peut y définir des correspondances `nom ---> IP`

➜ **Allooooons-y, fichier de conf principal**

```bash
# éditez le fichier de config principal pour qu'il ressemble à :
$ sudo cat /etc/named.conf
options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
[...]
        allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };

        recursion yes;
[...]
# référence vers notre fichier de zone
zone "tp4.b1" IN {
     type master;
     file "tp4.b1.db";
     allow-update { none; };
     allow-query {any; };
};
# référence vers notre fichier de zone inverse
zone "1.4.10.in-addr.arpa" IN {
     type master;
     file "tp4.b1.rev";
     allow-update { none; };
     allow-query { any; };
};
```

➜ **Et pour les fichiers de zone**

```bash
# Fichier de zone pour nom -> IP

$ sudo cat /var/named/tp4.b1.db

$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

; Enregistrements DNS pour faire correspondre des noms à des IPs
dns-server IN A 10.4.1.201
node1      IN A 10.4.1.11
```

```bash
# Fichier de zone inverse pour IP -> nom

$ sudo cat /var/named/tp4.b1.rev

$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

;Reverse lookup for Name Server
201 IN PTR dns-server.tp4.b1.
11 IN PTR node1.tp4.b1.
```

➜ **Une fois ces 3 fichiers en place, démarrez le service DNS**

```bash
# Démarrez le service tout de suite
$ sudo systemctl start named

# Faire en sorte que le service démarre tout seul quand la VM s'allume
$ sudo systemctl enable named

# Obtenir des infos sur le service
$ sudo systemctl status named

# Obtenir des logs en cas de probème
$ sudo journalctl -xe -u named
```

🌞 **Dans le rendu, je veux**

- un `cat` des fichiers de conf
```
[user1@dns-server-tp4 ~]$ sudo cat /etc/named.conf
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
	listen-on port 53 { 127.0.0.1; };
	listen-on-v6 port 53 { ::1; };
	directory 	"/var/named";
	dump-file 	"/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	memstatistics-file "/var/named/data/named_mem_stats.txt";
	secroots-file	"/var/named/data/named.secroots";
	recursing-file	"/var/named/data/named.recursing";
	allow-query     { localhost; any; };
	allow-query-cache { localhost; any; };

	/* 
	 - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
	 - If you are building a RECURSIVE (caching) DNS server, you need to enable 
	   recursion. 
	 - If your recursive DNS server has a public IP address, you MUST enable access 
	   control to limit queries to your legitimate users. Failing to do so will
	   cause your server to become part of large scale DNS amplification 
	   attacks. Implementing BCP38 within your network would greatly
	   reduce such attack surface 
	*/
	recursion yes;

	dnssec-validation yes;

	managed-keys-directory "/var/named/dynamic";
	geoip-directory "/usr/share/GeoIP";

	pid-file "/run/named/named.pid";
	session-keyfile "/run/named/session.key";

	/* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
	include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
	type hint;
	file "named.ca";
};

zone "tp4.b1" IN {
     type master;
     file "tp4.b1.db";
     allow-update { none; };
     allow-query {any; };
};
# référence vers notre fichier de zone inverse
zone "1.4.10.in-addr.arpa" IN {
     type master;
     file "tp4.b1.rev";
     allow-update { none; };
     allow-query { any; };
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

```
[user1@dns-server-tp4 ~]$ sudo cat /var/named/tp4.b1.db
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

; Enregistrements DNS pour faire correspondre des noms à des IPs
dns-server IN A 10.4.1.201
node1      IN A 10.4.1.11
```

```
[user1@dns-server-tp4 ~]$ sudo cat /var/named/tp4.b1.rev
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

;Reverse lookup for Name Server
201 IN PTR dns-server.tp4.b1.
11 IN PTR node1.tp4.b1.
```

- un `systemctl status named` qui prouve que le service tourne bien

```
[user1@dns-server-tp4 ~]$ systemctl status named
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; vendor pre>
     Active: active (running) since Wed 2022-10-26 14:29:19 CEST; 4min 28s ago
   Main PID: 11772 (named)
      Tasks: 5 (limit: 5905)
     Memory: 18.0M
        CPU: 34ms
     CGroup: /system.slice/named.service
             └─11772 /usr/sbin/named -u named -c /etc/named.conf

Oct 26 14:29:19 dns-server-tp4 named[11772]: network unreachable resolving './D>
Oct 26 14:29:19 dns-server-tp4 named[11772]: network unreachable resolving './N>
Oct 26 14:29:19 dns-server-tp4 named[11772]: zone tp4.b1/IN: loaded serial 2019>
Oct 26 14:29:19 dns-server-tp4 named[11772]: zone localhost/IN: loaded serial 0
Oct 26 14:29:19 dns-server-tp4 named[11772]: zone localhost.localdomain/IN: loa>
Oct 26 14:29:19 dns-server-tp4 named[11772]: all zones loaded
Oct 26 14:29:19 dns-server-tp4 systemd[1]: Started Berkeley Internet Name Domai>
Oct 26 14:29:19 dns-server-tp4 named[11772]: running
Oct 26 14:29:19 dns-server-tp4 named[11772]: resolver priming query complete
Oct 26 14:29:19 dns-server-tp4 named[11772]: managed-keys-zone: Initializing au>
lines 1-20/20 (END)

```
- une commande `ss` qui prouve que le service écoute bien sur un port


```
[user1@dns-server-tp4 ~]$ ss -lnptu
Netid               State                Recv-Q                Send-Q                               Local Address:Port                               Peer Address:Port               Process               
tcp                 LISTEN               0                     10                                       127.0.0.1:53                                      0.0.0.0:*                                        
tcp                 LISTEN               0                     10                                           [::1]:53                                         [::]:*                                        
```

🌞 **Ouvrez le bon port dans le firewall**

- grâce à la commande `ss` vous devrez avoir repéré sur quel port tourne le service
  - vous l'avez écrit dans la conf aussi toute façon :)
- ouvrez ce port dans le firewall de la machine `dns-server.tp4.b1` (voir le mémo réseau Rocky)
```
[user1@dns-server-tp4 ~]$ sudo firewall-cmd --add-port=53/tcp --permanent
```

## 3. Test

🌞 **Sur la machine `node1.tp4.b1`**

- configurez la machine pour qu'elle utilise votre serveur DNS quand elle a besoin de résoudre des noms
- assurez vous que vous pouvez :
  - résoudre des noms comme `node1.tp4.b1` et `dns-server.tp4.b1`
  - mais aussi des noms comme `www.google.com`

🌞 **Sur votre PC**

- utilisez une commande pour résoudre le nom `node1.tp4.b1` en utilisant `10.4.1.201` comme serveur DNS

```
m4ul@thinkpad:~$ sudo cat /etc/resolv.conf 
# This is /run/systemd/resolve/stub-resolv.conf managed by man:systemd-resolved(8).
# Do not edit.
#
# This file might be symlinked as /etc/resolv.conf. If you're looking at
# /etc/resolv.conf and seeing this text, you have followed the symlink.
#
# This is a dynamic resolv.conf file for connecting local clients to the
# internal DNS stub resolver of systemd-resolved. This file lists all
# configured search domains.
#
# Run "resolvectl status" to see details about the uplink DNS servers
# currently in use.
#
# Third party programs should typically not access this file directly, but only
# through the symlink at /etc/resolv.conf. To manage man:resolv.conf(5) in a
# different way, replace this symlink by a static file or a different symlink.
#
# See man:systemd-resolved.service(8) for details about the supported modes of
# operation for /etc/resolv.conf.

#nameserver 127.0.0.53
nameserver 10.4.1.201
options edns0 trust-ad
search .
m4ul@thinkpad:~$ ping node1tp4
PING node1tp4 (10.4.1.11) 56(84) bytes of data.
64 bytes from node1tp4 (10.4.1.11): icmp_seq=1 ttl=64 time=0.455 ms
64 bytes from node1tp4 (10.4.1.11): icmp_seq=2 ttl=64 time=0.428 ms
^C
--- node1tp4 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1020ms
rtt min/avg/max/mdev = 0.428/0.441/0.455/0.013 ms
```

> Le fait que votre serveur DNS puisse résoudre un nom comme `www.google.com`, ça s'appelle la récursivité et c'est activé avec la ligne `recursion yes;` dans le fichier de conf.

🦈 **Capture d'une requête DNS vers le nom `node1.tp4.b1` ainsi que la réponse**
