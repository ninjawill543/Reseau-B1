# TP1 - Premier pas réseau

# I. Exploration locale en solo

## 1. Affichage d'informations sur la pile TCP/IP locale

### En ligne de commande

En utilisant la ligne de commande (CLI) de votre OS :

**🌞 Affichez les infos des cartes réseau de votre PC**

```
lucashanson@Lucass-MacBook-Pro ~ % ifconfig
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=6463<RXCSUM,TXCSUM,TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether 74:8f:3c:be:6e:b6
	inet6 fe80::42e:fb9c:7a0c:781a%en0 prefixlen 64 secured scopeid 0xb
	inet 10.33.16.202 netmask 0xfffffc00 broadcast 10.33.19.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
```

Je n'ai pas de carte ethernet

**🌞 Affichez votre gateway**

```
lucashanson@Lucass-MacBook-Pro ~ % netstat -nr|grep default
default            10.33.19.254       UGScg             en0
default                                 fe80::%utun0                    UGcIg           utun0
default                                 fe80::%utun1                    UGcIg           utun1
default                                 fe80::%utun2                    UGcIg           utun2
```

**🌞 Déterminer la MAC de la passerelle**

```
lucashanson@Lucass-MacBook-Pro ~ % arp -a|grep 10.33.19.254
? (10.33.19.254) at 0:c0:e7:e0:4:4e on en0 ifscope [ethernet]

```

### En graphique (GUI : Graphical User Interface)

En utilisant l'interface graphique de votre OS :

**🌞 Trouvez comment afficher les informations sur une carte IP (change selon l'OS)**

![](Images/1.png)
![](Images/2.png)

## 2. Modifications des informations

### A. Modification d'adresse IP (part 1)

🌞 Utilisez l'interface graphique de votre OS pour **changer d'adresse IP** :

![](Images/3.png)

🌞 **Il est possible que vous perdiez l'accès internet.** Que ce soit le cas ou non, expliquez pourquoi c'est possible de perdre son accès internet en faisant cette opération.

C'est possible de perdre son accès car le routeur ne reconnait pas l'adresse ip qu'on a marqué.

---

- **NOTE :** si vous utilisez la même IP que quelqu'un d'autre, il se passerait la même chose qu'en vrai avec des adresses postales :
  - deux personnes habitent au même numéro dans la même rue, mais dans deux maisons différentes
  - quand une de ces personnes envoie un message, aucun problème, l'adresse du destinataire est unique, la lettre sera reçue
  - par contre, pour envoyer un message à l'une de ces deux personnes, le facteur sera dans l'impossibilité de savoir dans quelle boîte aux lettres il doit poser le message
  - ça marche à l'aller, mais pas au retour

# II. Exploration locale en duo

Owkay. Vous savez à ce stade :

- afficher les informations IP de votre machine
- modifier les informations IP de votre machine
- c'est un premier pas vers la maîtrise de votre outil de travail

On va maintenant répéter un peu ces opérations, mais en créant un réseau local de toutes pièces : entre deux PCs connectés avec un câble RJ45.

## 1. Prérequis

- deux PCs avec ports RJ45
- un câble RJ45
- **firewalls désactivés** sur les deux PCs

## 2. Câblage

Ok c'est la partie tendue. Prenez un câble. Branchez-le des deux côtés. **Bap.**

## Création du réseau (oupa)

Cette étape pourrait paraître cruciale. En réalité, elle n'existe pas à proprement parlé. On ne peut pas "créer" un réseau.

**Si une machine possède une carte réseau, et si cette carte réseau porte une adresse IP**, alors cette adresse IP se trouve dans un réseau (l'adresse de réseau). Ainsi, **le réseau existe. De fait.**

**Donc il suffit juste de définir une adresse IP sur une carte réseau pour que le réseau existe ! Bap.**

## 3. Modification d'adresse IP

🌞 **Modifiez l'IP des deux machines pour qu'elles soient dans le même réseau**

- Si vos PCs ont un port RJ45 alors y'a une carte réseau Ethernet associée
- choisissez une IP qui commence par "10.10.10."
  - /24 pour la longueur de masque, ou 255.255.255.0 pour le masque (suivant les OS, l'info est demandée différement, mais c'est la même chose)

![](https://i.imgur.com/86TZvvQ.png)

🌞 **Vérifier à l'aide d'une commande que votre IP a bien été changée**

```
ipconfig /all
Ethernet adapter:
`IPv4 Address. . . . . . . . . . . : 10.10.10.69(Preferred)`
```

🌞 **Vérifier que les deux machines se joignent**

```
PS C:\Users\alexa> ping -t 10.10.10.70
Pinging 10.10.10.70 with 32 bytes of data:
Reply from 10.10.10.70: bytes=32 time=2ms TTL=128
Reply from 10.10.10.70: bytes=32 time=2ms TTL=128
Reply from 10.10.10.70: bytes=32 time=2ms TTL=128
Reply from 10.10.10.70: bytes=32 time=2ms TTL=128
Reply from 10.10.10.70: bytes=32 time=2ms TTL=128
Reply from 10.10.10.70: bytes=32 time=2ms TTL=128
Ping statistics for 10.10.10.70:
    Packets: Sent = 6, Received = 6, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 2ms, Maximum = 2ms, Average = 2ms
```

- utilisez la commande `ping` pour tester la connectivité entre les deux machines

> La commande `ping` est un message simple envoyé à une autre machine. Cette autre machine retournera alors un message tout aussi simple. `ping` utilise un protocole frère de IP : le protocole ICMP. On mesure souvent la latence réseau grâce à un `ping` : en mesurant la durée entre l'émission du `ping` et la réception du retour.
> 🌞 **Déterminer l'adresse MAC de votre correspondant**

- pour cela, affichez votre table ARP

```
arp -a
10.10.10.70           54-ab-3a-dd-97-f9     dynamic
```

## 4. Utilisation d'un des deux comme gateway

Ca, ça peut toujours dépann irl. Comme pour donner internet à une tour sans WiFi quand y'a un PC portable à côté, par exemple.

L'idée est la suivante :

- vos PCs ont deux cartes avec des adresses IP actuellement
  - la carte WiFi, elle permet notamment d'aller sur internet, grâce au réseau YNOV
  - la carte Ethernet, qui permet actuellement de joindre votre coéquipier, grâce au réseau que vous avez créé :)
- si on fait un tit schéma tout moche, ça donne ça :

```schema
  Internet           Internet
     |                   |
    WiFi                WiFi
     |                   |
    PC 1 ---Ethernet--- PC 2

- internet joignable en direct par le PC 1
- internet joignable en direct par le PC 2
```

- vous allez désactiver Internet sur une des deux machines, et vous servir de l'autre machine pour accéder à internet.

```schema
  Internet           Internet
     X                   |
     X                  WiFi
     |                   |
    PC 1 ---Ethernet--- PC 2

- internet joignable en direct par le PC 2
- internet joignable par le PC 1, en passant par le PC 2
```

- pour ce faiiiiiire :
  - désactivez l'interface WiFi sur l'un des deux postes
  - s'assurer de la bonne connectivité entre les deux PCs à travers le câble RJ45
  - **sur le PC qui n'a plus internet**
    - sur la carte Ethernet, définir comme passerelle l'adresse IP de l'autre PC
  - **sur le PC qui a toujours internet**
    - sur Windows, il y a une option faite exprès (google it. "share internet connection windows 10" par exemple)
    - sur GNU/Linux, faites le en ligne de commande ou utilisez [Network Manager](https://help.ubuntu.com/community/Internet/ConnectionSharing) (souvent présent sur tous les GNU/Linux communs)
    - sur MacOS : toute façon vous avez pas de ports RJ, si ? :o (google it sinon)

---

🌞**Tester l'accès internet**

- pour tester la connectivité à internet on fait souvent des requêtes simples vers un serveur internet connu
- essayez de ping l'adresse IP `1.1.1.1`, c'est un serveur connu de CloudFlare (demandez-moi si vous comprenez pas trop la démarche)

```
ping 1.1.1.1
Envoi d’une requête 'Ping'  1.1.1.1 avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=22 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=23 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=28 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=25 ms TTL=54
Statistiques Ping pour 1.1.1.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 22ms, Maximum = 28ms, Moyenne = 24ms
```

🌞 **Prouver que la connexion Internet passe bien par l'autre PC**

- utiliser la commande `traceroute` ou `tracert` (suivant votre OS) pour bien voir que les requêtes passent par la passerelle choisie (l'autre le PC)

> La commande `traceroute` retourne la liste des machines par lesquelles passent le `ping` avant d'atteindre sa destination.

```
tracert -4 10.10.10.69
Détermination de l’itinéraire vers belalexandre [10.10.10.69]
avec un maximum de 30 sauts :
  1     2 ms     2 ms     2 ms  belalexandre [10.10.10.69]
Itinéraire déterminé.
```

## 5. Petit chat privé

![Netcat](./pics/netcat.jpg)

On va créer un chat extrêmement simpliste à l'aide de `netcat` (abrégé `nc`). Il est souvent considéré comme un bon couteau-suisse quand il s'agit de faire des choses avec le réseau.

Sous GNU/Linux et MacOS vous l'avez sûrement déjà, sinon débrouillez-vous pour l'installer :). Les Windowsien, ça se passe [ici](https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip) (from https://eternallybored.org/misc/netcat/).

Une fois en possession de `netcat`, vous allez pouvoir l'utiliser en ligne de commande. Comme beaucoup de commandes sous GNU/Linux, Mac et Windows, on peut utiliser l'option `-h` (`h` pour `help`) pour avoir une aide sur comment utiliser la commande.

Sur un Windows, ça donne un truc comme ça :

```schema
C:\Users\It4\Desktop\netcat-win32-1.11>nc.exe -h
[v1.11 NT www.vulnwatch.org/netcat/]
connect to somewhere:   nc [-options] hostname port[s] [ports] ...
listen for inbound:     nc -l -p port [options] [hostname] [port]
options:
        -d              detach from console, background mode
        -e prog         inbound program to exec [dangerous!!]
        -g gateway      source-routing hop point[s], up to 8
        -G num          source-routing pointer: 4, 8, 12, ...
        -h              this cruft
        -i secs         delay interval for lines sent, ports scanned
        -l              listen mode, for inbound connects
        -L              listen harder, re-listen on socket close
        -n              numeric-only IP addresses, no DNS
        -o file         hex dump of traffic
        -p port         local port number
        -r              randomize local and remote ports
        -s addr         local source address
        -t              answer TELNET negotiation
        -u              UDP mode
        -v              verbose [use twice to be more verbose]
        -w secs         timeout for connects and final net reads
        -z              zero-I/O mode [used for scanning]
port numbers can be individual or ranges: m-n [inclusive]
```

L'idée ici est la suivante :

- l'un de vous jouera le rôle d'un _serveur_
- l'autre sera le _client_ qui se connecte au _serveur_

Précisément, on va dire à `netcat` d'_écouter sur un port_. Des ports, y'en a un nombre fixe (65536, on verra ça plus tard), et c'est juste le numéro de la porte à laquelle taper si on veut communiquer avec le serveur.

Si le serveur écoute à la porte 20000, alors le client doit demander une connexion en tapant à la porte numéro 20000, simple non ?

Here we go :

🌞 **sur le PC _serveur_** avec par exemple l'IP 192.168.1.1

- `nc.exe -l -p 8888`
  - "`netcat`, écoute sur le port numéro 8888 stp"
- il se passe rien ? Normal, faut attendre qu'un client se connecte

```
nc.exe -l -p 8888
salut
pp
salut
bravo
ggwp
```

🌞 **sur le PC _client_** avec par exemple l'IP 192.168.1.2

- `nc.exe 192.168.1.1 8888`
  - "`netcat`, connecte toi au port 8888 de la machine 192.168.1.1 stp"
- une fois fait, vous pouvez taper des messages dans les deux sens
- appelez-moi quand ça marche ! :)
- si ça marche pas, essayez d'autres options de `netcat`

```
[alex@fedora ~]$ nc 10.10.10.70 8888
salut
pp
salut
bravo
```

---

🌞 **Visualiser la connexion en cours**

- sur tous les OS, il existe une commande permettant de voir les connexions en cours
- ouvrez un deuxième terminal pendant une session `netcat`, et utilisez la commande correspondant à votre OS pour repérer la connexion `netcat` :

```bash
# Windows (dans un Powershell administrateur)
$ netstat -a -n -b
# Linux
$ ss -atnp
# MacOS
$ netstat -a -n # je crois :D
```

```
ESTAB       0        0            10.10.10.69:48888          10.10.10.70:8888    users:(("nc",pid=16933,fd=3))
```

🌞 **Pour aller un peu plus loin**

- si vous faites un `netstat` sur le serveur AVANT que le client `netcat` se connecte, vous devriez observer que votre serveur `netcat` écoute sur toutes vos interfaces
  - c'est à dire qu'on peut s'y connecter depuis la wifi par exemple :D
- il est possible d'indiquer à `netcat` une interface précise sur laquelle écouter
  - par exemple, on écoute sur l'interface Ethernet, mais pas sur la WiFI

```bash
# Sur Windows/MacOS
$ nc.exe -l -p PORT_NUMBER -s IP_ADDRESS
# Par exemple
$ nc.exe -l -p 9999 -s 192.168.1.37
```

```
C:\Users\maelf\Downloads\netcat-win32-1.11(2)\netcat-1.11>netstat
Connexions actives
  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.17.18:52828      52.97.16.130:https     ESTABLISHED
  TCP    10.33.17.18:53161      52.112.120.13:https    ESTABLISHED
  TCP    10.33.17.18:53168      20.90.152.133:https    ESTABLISHED
  TCP    10.33.17.18:53169      20.90.152.133:https    ESTABLISHED
  TCP    10.33.17.18:56650      ec2-34-202-207-135:https  ESTABLISHED
  TCP    10.33.17.18:57006      ec2-63-32-136-173:https  ESTABLISHED
  TCP    10.33.17.18:57020      ec2-54-225-152-45:https  ESTABLISHED
  TCP    10.33.17.18:57029      162.159.134.234:https  ESTABLISHED
  TCP    10.33.17.18:57034      20.199.120.85:https    ESTABLISHED
  TCP    10.33.17.18:57035      20.199.120.85:https    ESTABLISHED
  TCP    10.33.17.18:57037      52.112.120.19:https    ESTABLISHED
  TCP    10.33.17.18:57046      104.18.12.33:https     ESTABLISHED
  TCP    10.33.17.18:59977      162.159.129.232:https  ESTABLISHED
  TCP    10.33.17.18:60048      172.65.251.78:https    ESTABLISHED
  TCP    10.33.17.18:60059      a96-16-249-35:https    CLOSE_WAIT
  TCP    10.33.17.18:60060      a96-16-249-35:https    CLOSE_WAIT
  TCP    10.33.17.18:60063      52.97.146.194:https    ESTABLISHED
  TCP    10.33.17.18:60159      20.189.173.6:https     ESTABLISHED
  TCP    10.33.17.18:60175      server-52-222-158-19:https  ESTABLISHED
  TCP    127.0.0.1:58399        LAPTOP-5JDPJGNB:60441  ESTABLISHED
  TCP    127.0.0.1:60183        LAPTOP-5JDPJGNB:27300  SYN_SENT
  TCP    127.0.0.1:60441        LAPTOP-5JDPJGNB:58399  ESTABLISHED
```

## 6. Firewall

Toujours par 2.

Le but est de configurer votre firewall plutôt que de le désactiver

🌞 **Activez et configurez votre firewall**

- autoriser les `ping`
  - configurer le firewall de votre OS pour accepter le `ping`
  - aidez vous d'internet
  - on rentrera dans l'explication dans un prochain cours mais sachez que `ping` envoie un message _ICMP de type 8_ (demande d'ECHO) et reçoit un message _ICMP de type 0_ (réponse d'écho) en retour

```
systemctl enable firewalld
```

```
firewall-cmd --permanent --direct --add-rule ipv4 filter INPUT 0 -p icmp -s 0.0.0.0/0 -d 0.0.0.0/0 -j ACCEPT
sudo systemctl restart firewalld.service
```

- autoriser le traffic sur le port qu'utilise `nc`
  - on parle bien d'ouverture de **port** TCP et/ou UDP
  - on ne parle **PAS** d'autoriser le programme `nc`
  - choisissez arbitrairement un port entre 1024 et 20000
  - vous utiliserez ce port pour communiquer avec `netcat` par groupe de 2 toujours
  - le firewall du _PC serveur_ devra avoir un firewall activé et un `netcat` qui fonctionne

```
[alex@fedora ~]$ nc 10.10.10.70 8888
feak
faekf
eafeak
fea
en legende
```

# III. Manipulations d'autres outils/protocoles côté client

## 1. DHCP

Bon ok vous savez définir des IPs à la main. Mais pour être dans le réseau YNOV, vous l'avez jamais fait.

C'est le **serveur DHCP** d'YNOV qui vous a donné une IP.

Une fois que le serveur DHCP vous a donné une IP, vous enregistrer un fichier appelé _bail DHCP_ qui contient, entre autres :

- l'IP qu'on vous a donné
- le réseau dans lequel cette IP est valable

🌞**Exploration du DHCP, depuis votre PC**

- afficher l'adresse IP du serveur DHCP du réseau WiFi YNOV

```
lucashanson@Lucass-MacBook-Pro ~ % ipconfig getpacket en0
server_identifier (ip): 10.33.19.254
```

- cette adresse a une durée de vie limitée. C'est le principe du **_bail DHCP_** (ou _DHCP lease_). Trouver la date d'expiration de votre bail DHCP

```
lucashanson@Lucass-MacBook-Pro ~ % ipconfig getpacket en0
lease_time (uint32): 0x15040
```

- vous pouvez vous renseigner un peu sur le fonctionnement de DHCP dans les grandes lignes. On aura un cours là dessus :)

> Chez vous, c'est votre box qui fait serveur DHCP et qui vous donne une IP quand vous le demandez.

## 2. DNS

Le protocole DNS permet la résolution de noms de domaine vers des adresses IP. Ce protocole permet d'aller sur `google.com` plutôt que de devoir connaître et utiliser l'adresse IP du serveur de Google.

Un **serveur DNS** est un serveur à qui l'on peut poser des questions (= effectuer des requêtes) sur un nom de domaine comme `google.com`, afin d'obtenir les adresses IP liées au nom de domaine.

Si votre navigateur fonctionne "normalement" (il vous permet d'aller sur `google.com` par exemple) alors votre ordinateur connaît forcément l'adresse d'un serveur DNS. Et quand vous naviguez sur internet, il effectue toutes les requêtes DNS à votre place, de façon automatique.

🌞** Trouver l'adresse IP du serveur DNS que connaît votre ordinateur**

![](Images/4.png)

🌞 Utiliser, en ligne de commande l'outil `nslookup` (Windows, MacOS) ou `dig` (GNU/Linux, MacOS) pour faire des requêtes DNS à la main

- faites un _lookup_ (_lookup_ = "dis moi à quelle IP se trouve tel nom de domaine")
  - pour `google.com`

```
  lucashanson@Lucass-MacBook-Pro ~ % nslookup google.com
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
Name:	google.com
Address: 142.250.179.110
```

- pour `ynov.com`

```
lucashanson@Lucass-MacBook-Pro ~ % nslookup ynov.com
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
Name:	ynov.com
Address: 104.26.10.233
Name:	ynov.com
Address: 104.26.11.233
Name:	ynov.com
Address: 172.67.74.226
```

- interpréter les résultats de ces commandes

Cette commande nous montre le serveur DNS du serveur et le/les adresses ip du/des serveur. ynov.com a plusieurs adresses car il utilise une pépartition de charge dns

- déterminer l'adresse IP du serveur à qui vous venez d'effectuer ces requêtes

**Google:**

142.250.179.110

**Ynov:**

104.26.10.233

104.26.11.233

172.67.74.226

- faites un _reverse lookup_ (= "dis moi si tu connais un nom de domaine pour telle IP")
  - pour l'adresse `78.73.21.21`

```
lucashanson@Lucass-MacBook-Pro ~ % nslookup 78.73.21.21
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
21.21.73.78.in-addr.arpa	name = 78-73-21-21-no168.tbcn.telia.com.
```

- pour l'adresse `22.146.54.58`

```
lucashanson@Lucass-MacBook-Pro ~ % nslookup 22.146.54.58
Server:		8.8.8.8
Address:	8.8.8.8#53

** server can't find 58.54.146.22.in-addr.arpa: NXDOMAIN
```

- interpréter les résultats

- _si vous vous demandez, j'ai pris des adresses random :)_

# IV. Wireshark

**Wireshark est un outil qui permet de visualiser toutes les trames qui sortent et entrent d'une carte réseau.**

On appelle ça un **sniffer**, ou **analyseur de trames.**

![Wireshark](./pics/wireshark.jpg)

Il peut :

- enregistrer le trafic réseau, pour l'analyser plus tard
- afficher le trafic réseau en temps réel

**On peut TOUT voir.**

Un peu austère aux premiers abords, une manipulation très basique permet d'avoir une très bonne compréhension de ce qu'il se passe réellement.

➜ **[Téléchargez l'outil Wireshark](https://www.wireshark.org/).**

🌞 Utilisez le pour observer les trames qui circulent entre vos deux carte Ethernet. Mettez en évidence :

Je n'ai pas pu faire cette partie car je n'ai pas de carte ethernet étant sur mac.

- un `ping` entre vous et votre passerelle
  ![](Images/ping.png)
- un `netcat` entre vous et votre mate, branché en RJ45
  ![](Images/netcat.png)
- une requête DNS. Identifiez dans la capture le serveur DNS à qui vous posez la question.
  ![](Images/dns.png)
- prenez moi des screens des trames en question
- on va prendre l'habitude d'utiliser Wireshark souvent dans les cours, pour visualiser ce qu'il se passe

Youtube:
![](Images/yt.png)

# Bilan

**Vu pendant le TP :**

- visualisation de vos interfaces réseau (en GUI et en CLI)
- extraction des informations IP
  - adresse IP et masque
  - calcul autour de IP : adresse de réseau, etc.
- connaissances autour de/aperçu de :
  - un outil de diagnostic simple : `ping`
  - un outil de scan réseau : `nmap`
  - un outil qui permet d'établir des connexions "simples" (on y reviendra) : `netcat`
  - un outil pour faire des requêtes DNS : `nslookup` ou `dig`
  - un outil d'analyse de trafic : `wireshark`
- manipulation simple de vos firewalls

**Conclusion :**

- Pour permettre à un ordinateur d'être connecté en réseau, il lui faut **une liaison physique** (par câble ou par _WiFi_).
- Pour réceptionner ce lien physique, l'ordinateur a besoin d'**une carte réseau**. La carte réseau porte une adresse MAC
- **Pour être membre d'un réseau particulier, une carte réseau peut porter une adresse IP.**
  Si deux ordinateurs reliés physiquement possèdent une adresse IP dans le même réseau, alors ils peuvent communiquer.
- **Un ordintateur qui possède plusieurs cartes réseau** peut réceptionner du trafic sur l'une d'entre elles, et le balancer sur l'autre, servant ainsi de "pivot". Cet ordinateur **est appelé routeur**.
- Il existe dans la plupart des réseaux, certains équipements ayant un rôle particulier :
  - un équipement appelé _passerelle_. C'est un routeur, et il nous permet de sortir du réseau actuel, pour en joindre un autre, comme Internet par exemple
  - un équipement qui agit comme **serveur DNS** : il nous permet de connaître les IP derrière des noms de domaine
  - un équipement qui agit comme **serveur DHCP** : il donne automatiquement des IP aux clients qui rejoigne le réseau
  - **chez vous, c'est votre Box qui fait les trois :)**
