# moustache
Step by step tutorial of how to use OpenCV library with Python in a GNU/Linux environnement

![Moustache](https://github.com/nicolastrote/moustache/blob/master/moustache.png)

## Installation

This tutorial is done with a Raspberry Pi and typical webcam. But you find all informations needed for a typical GNU/Linux OS.
The tutorial is in french, but I will translate it.

## INSTALLATION DE RASPBMC


Nous allons installer la distribution Raspbian, un fork de Debian dédié au Raspberry Pi. L’installation se passera depuis un poste sous Debian depuis le terminal et le dos calé dans le fauteuil ;-)  Ubuntu et dérivées sont compatibles avec ce tutoriel.


Ouvrez votre terminal ( touche SUPER + T) ou avec Gnome-Panel : Applications → Accessoires → Terminal, et téléchargez en ligne de commande la dernière image de Raspbian :
$ cd ~/Téléchargements
$ wget http://downloads.raspberrypi.org/raspbian_latest


Dézippez l’archive de Raspbian en adaptant la date dans le nom du fichier. Pour afficher les fichiers reçus avec le nom raspbian, utilisez la commande:
$ ls | grep ‘raspbian’
Le fichier a du apparaître, vous pouvez corriger le nom du fichier zip :
$ unzip 2014-01-07-wheezy-raspbian.zip


Vérifiez l’emplacement de la carte SD sur laquelle nous allons transférer l’image de Raspbian :
$ sudo fdisk -l
En regardant la taille des différents disque j’en déduis que ma carte SD est reconnue sous /dev/sdb.


Vous aller maintenant copier le fichier image de Raspbian vers la carte SD avec la commande dd:
$ sudo dd bs=4M if=~/Téléchargements/2014-01-07-wheezy-raspbian.img  of=/dev/sdb    
(adaptez les chemins et noms)
Pour être sûr que la copy soit finie avant de rejeter la carte SD, utilisez sync et attendez d’avoir repris la main:
$ sudo sync


Vous pouvez maintenant retirer la carte SD, l’insérer dans votre Raspberry Pi éteint, puis mettre sous alimentation votre Raspberry Pi. L’installation est longue (30min environ) mais automatisée. Il vous sera demandé votre langue, pays et locale à utiliser.




## PRENDRE LE CONTRÔLE DE RPi


A ce stade, il existe deux manière de prendre le controle du RPi. La méthode classique dite “physique” avec un clavier et une souris sur les ports USB, ou la méthode à distance via une connexion sécurisée SSH.


## SE CONNECTER PHYSIQUEMENT


Connectez au RPi un clavier et une souris sur les ports usb, ainsi qu’un écran en connectique HDMI. Dans ce cas là, il est fort probable que le clavier soit reconnu comme un clavier anglosaxon QWERTY. Attention à la façon de taper le mot de passe “raspbian” qui devra être tapé “rqsbiqn” sans les guillemets!


## SE CONNECTER EN SSH


Pour se connecter à distance, j’utilise dans ce tutoriel un pc installé sous une distribution Debian ou dérivée (Ubuntu, LinuxMint,..) et le programme openSSH.


Ouvrez le terminal sur votre PC et installez le programme openssh-client:
$ sudo apt-get install openssh-client


Connectez-vous en ssh sur le RaspBMC
$ ssh pi@192.168.1.35
le mot de passe demandé sera: raspberry


## CONFIGURATION DU CLAVIER EN FR DES LE DÉMARRAGE


Mon clavier est bien Azerty sous le terminal, par contre une fois que je lance X11 (startx), mon clavier est a nouveau en qwerty… La solution est de rajouter dans le fichier /etc/X11/xinit/xinitrc, l’information “setxkbmap fr” avant la ligne “. /etc/X11/Xsession”.
voici mon fichier xinitrc apres.
setxkbmap fr
. /etc/X11/Xsession


## CONFIGURATION DE LA ZONE DE TEMPS


Lancez dans le terminal la commande : 
# dpkg-reconfigure tzdata
et choisir Paris par exemple : >Europe > Paris

## CONFIGURATION DES LOCALES


Lancez dans le terminal les commandes : 
# apt-get install locales
# dpkg-reconfigure locales
Décochez la case :
[] en_GB.UTF-8 UTF-8
Cochez les cases :
[*] fr_FR ISO-8859-1
[*] fr_FR.UTF-8 UTF-8
Puis pour Default locale for the system environement choisir  fr_FR.UTF-8.


## CONFIGURATION DU CLAVIER

Lancez dans le terminal les commandes : 
# apt-get install keyboard-configuration
# dpkg-reconfigure keyboard-configuration
Choisir Generic 105-key (intl) PC  puis other > French > French-french (legacy, alternative).


Valider les autres options par défaut, mais répondez “oui” pour le raccourcis alt+ctrl+backspace pour redémarrer l’interface graphique.


## CORRIGER LES ERREURS DE LOCALES


Pour corriger les erreurs sur les locales faites: 
# dpkg-reconfigure locales 
et si tout se passe bien
# sudo apt-get update pour trouver le compiler en fr!


## INSTALLATIONS UTILES

Installation du compilateur Gnu C/C++:
 $ sudo apt-get install build-essential


Désinstallons Midori qui est très lent pour netsurf-gtk:
$ sudo  apt-get purge midori && apt-get autoremove
$ sudo apt-get install netsurf-gtk


Outils d’administration utiles : 
    $ sudo apt-get install htop


Rechercher des Paquets
    $ sudo apt-get install apt-file && sudo apt-file update

LANCEMENT DU BUREAU LXDE


Pour lancer la session sous LXDE, lancez la commande : 
$  startx &


VERIFICATIONS DES RESSOURCES

La commande Free permet de connaitre à ce stade les ressources consommées par Debian :


pi@raspbian ~ $ free -h
                                               total         used        free     shared    buffers     cached
Mem:                                   183M           48M      135M         0B          8.3M            21M
-/+ buffers/cache:                              19M     164M
Swap:                                     99M              0B        99M




La ligne “buffers/cache” indique que Raspbian consomme 19MB de la mémoire vive sans LXDE, ce qui nous reste 164MB à utiliser pour d’autres applications. 
MISE A JOUR DE RASPBIAN ET FIRMWARE
Voici la commande universelle pour bien mettre à jour votre Raspbian:
$ sudo apt-get update && apt-get -y upgrade && sudo  apt-get -y dist-upgrade && sudo  apt-get autoremove --purge

Il est recommandé aussi de mettre à jour le firmware du rpi-update depuis son site Github,
en lançant la commande (vérifiez que le temps système est bien à jour) :
               $ sudo rpi-update


## ACTIVER LE HDMI EN HOTPLUG


Étrangement après une grosse mise à jour la connexion HDMI ne fonctionne plus. Pour réactiver manuellement la sortie utilisez : 
# hdmi_force_hotplug=1


De manière permanente, sous /boot/config.txt décommenter
config_hdmi_boost=4






## INSTALLER LA CLEF WIFI D-LINK DWA-131


Installons les outils pour utiliser le wifi : 
# apt-get install wireless-tools firmware-realtek 


Activons le dongle wifi
# ifconfig wlan0 up
Vérifions que nous détectons un réseau wifi à priximité
# iwlist scan
Configurer le fichier de connexion
# nano /etc/network/interfaces
auto lo
iface lo inet loopback
iface eth0 inet dhcp
allow-hotplug wlan0
iface wlan0 inet dhcp
wireless-essid Soleil
wireless-key off


## EMPÊCHER LE WIFI DE SE METTRE EN VEILLE
La configuration de base du raspbian fait que si vous n’utilisez pas votre raspberry pi, au bout d’un certains temps vous n’aurez plus accès à celui-ci. La connectique wifi sera tout simplement en veille, et impossible de l’en faire sortir depuis une connexion distante ssh. 
Pour éviter la mise en veille changez le paramètre automatiquement au démarrage de Raspbian :
$ sudo nano /etc/modprobe.d/r8712u.conf
en ajoutant cette commande qui désactivera la mise en veille :
options  r8712u  power_mgnt=0


## CHANGER LE MOT DE PASSE UTILISATEUR


Il est vivement conseillé de changer le mot de passe utilisateur:
# passwd pi


## DONNER UN NOM RESEAU PERSONNALISE AU RPi


Remplacez  “raspberry” par “mon_super_RPi” dans les fichiers
# nano /etc/hosts
# nano /etc/hostname


## CREER L’UTILISATEUR ROOT


$ sudo passwd root
CREER UN NOUVEL UTILISATEUR


Nous allons créer l’utilisateur “linuxmoi” et son répertoire
$ sudo adduser linuxmoi  --home /home/linuxmoi
$ sudo chown linuxmoi:users /home/linuxmoi  (surement pas nécessaire)


Connaitre les groups de pi
$ sudo groups pi
i : pi adm disk lp dialout cdrom audio video


Rajouter linuxmoi aux mêmes groupes que pi
$ sudo adduser linuxmoi  adm && 
   sudo adduser linuxmoi  dialout && 
sudo adduser linuxmoi  cdrom && 
sudo adduser linuxmoi  sudo && 
sudo adduser linuxmoi  audio && 
sudo adduser linuxmoi  video && 
sudo adduser linuxmoi  plugdev && 
sudo adduser linuxmoi  games && 
sudo adduser linuxmoi  users && 
sudo adduser linuxmoi  netdev && 
sudo adduser linuxmoi  input && 
sudo adduser linuxmoi  spi && 
sudo adduser linuxmoi  gpio


Vérifions que l’ajout s’est bien réalisé:
$ sudo groups linuxmoi
linuxmoi : linuxmoi adm disk lp dialout cdrom sudo audio video


Rajouter linuxmoi au groupe sudo
$ sudo adduser linuxmoi sudo


Configurer sudoers
$ sudo visudo
rajouter la même ligne que pi pour linuxmoi


Configurons les droits
$ sudo cp -R /home/pi/  /home/linuxmoi/
$ sudo chown -R linuxmoi:linuxmoi  /home/linuxmoi/
Vous pouvez redémarrer.


Si vous souhaitez supprimer l’utilisateur pi : 
$ sudo deluser pi --remove-home
Et supprimons le group pi
$ sudo groupdel pi




## CONFIGURATION DE LA CONNEXION SSH


La bonne nouvelle est que l’utilitaire pour la connexion SSH utilisée est OpenSSH. Historiquement l’équipe raspbian avait opté pour Dropbear, qui ne propose pas de connexion avec clef publique/privée.


Ouvre votre terminal puis taper la commande:
$ ssh pi@192.168.1.35
mot de passe: raspberry (si vous ne l’avez pas changé)


## Créer un couple de clef publique/privé pour se connecter


Pour ne plus avoir à se connecter via un mot de passe, vous pouvez utiliser un couple de clef publique/privé d’authentification.
Sur votre pc générez des clefs avec la commande:
$ ssh-keygen


Utilisez une phrase de pass, cela permet de bien sécuriser votre accès.
Maintenant vous allez envoyer votre clef publique au RPi en vous reconnectant via ssh
$ ssh votre-login@ip-du-rapsberry


Puis en copiant la clef public dans le dossier authorized de ssh avec l’outil ssh-copy-id
Déconnectez vous du ssh du RPI, puis tapez dans le terminal
$ ssh-copy-id votre-login@ip-du-rapsberry


Nous allons configurer ssh pour n’utiliser que ce mode de fonctionnement
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
UsePrivilegeSeparation yes
KeyRegenerationInterval 3600
ServerKeyBits 768
SyslogFacility AUTH
LogLevel INFO
LoginGraceTime 120
PermitRootLogin no
StrictModes yes
RSAAuthentication yes
PubkeyAuthentication yes
AuthorizedKeysFile      %h/.ssh/authorized_keys
IgnoreRhosts yes
RhostsRSAAuthentication no
HostbasedAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication yes
PasswordAuthentication no
X11Forwarding yes
X11DisplayOffset 10
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
MaxStartups 10:30:60
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
UsePAM no


Redémarrez pour prendre en compte les paramètres
$ sudo shutdown -r now

## SECURISER LES CONNEXIONS OUVERTES AVEC FAIL2BAN


Installons fail2ban qui aura pour effet de mettre en prison les IP ratant leur authentification.
$ sudo apt-get install fail2ban


Editez la configuration
$ sudo nano /etc/fail2ban/jail.conf


Vérifiez que pour ssh la protection est active
[ssh]
enabled  = true
ports = ssh, sftp


Mettez fail2ban actif pour proftpd
[proftpd]
enabled  = True


Idem pour Apache si vous installez un serveur web LAMP


## MISE A JOUR AUTOMATIQUE AVEC CRON-APT


Nous allons configurer cron-apt pour qu'il vérifie les mises à jour de sécurité seulement. 
Installer cron-apt :
$ sudo apt-get install cron-apt


Récupérons la liste des dépôts Debian Security:
# grep security /etc/apt/sources.list > /etc/apt/sources.list.d/security.list


Configurons le fichier /etc/cron-apt/config :
APTCOMMAND=/usr/bin/aptitude
OPTIONS="-o quiet=1 -o Dir::Etc::SourceList=/etc/apt/sources.list.d/security.list"
MAILTO="honeyshell@honeyshell.com"
MAILON="always"


À condition qu'un serveur SMTP soit installé et configuré, l'administrateur recevra un mail sur honeyshell@honeyshell.com, par défaut toutes les nuits à 4h du matin. La fréquence des mails se modifie dans /etc/cron.d/cron-apt, comme n'importe quelle tâche cron.
$ cat /etc/cron.d/cron-apt
#
# Regular cron jobs for the cron-apt package
#
# Every night at 4 o'clock.
0 4     * * *   root    test -x /usr/sbin/cron-apt && /usr/sbin/cron-apt
# Every hour.
# 0 *   * * *   root    test -x /usr/sbin/cron-apt && /usr/sbin/cron-apt /etc/cron-apt/config2
# Every five minutes.
# */5 * * * *   root    test -x /usr/sbin/cron-apt && /usr/sbin/cron-apt /etc/cron-apt/config2


Comme je l'ai déjà dit, par défaut cron-apt ne fait que télécharger les mises à jour, sans les appliquer. Pour également installer automatiquement les mises à jours, modifiez le fichier /etc/cron-apt/action.d/3-download, qui ressemble à l’origine à ceci :
autoclean -y
dist-upgrade -d -y -o APT::Get::Show-Upgraded=true
en ceci :
autoclean -y
full-upgrade -y -o APT::Get::Show-Upgraded=true
Vous pouvez adapter la ligne en fonction de vos besoins, en préférant par exemple un safe-upgrade.


## SAUVEGARDER VOTRE INSTALLATION 
Dans d'une installation sur une carte SSD, je vous recommande de sauvegarder votre environnement de programmation à cette étape. Il peut l'objet d'une futur application. Donc pour bien faire, éteignez votre raspberry pi, retirez la carte SD et insérez-la dans un pc muni d'un OS GNU/Linux pour utiliser la commande dd. (nb: marche aussi sous OSX)

La commande est du type:
$ dd if=<support à sauvegarder> of=/home/user/sauvegarde/<support sauvegardé>.iso

exemple:
$ dd if=/dev/sde of=/home/$USER/Documents/moustache.iso 
nb: la commande sudo fdisk -l vous indiquera la partition de la carte SD (ici /dev/sde pour l'exemple)
puis pour monter l'image et la tester:
$ mkdir /mnt/moncd
$ mount -o loop /home/user/moncd.iso /mnt/moncd


## INSTALLATION WEBCAM





Les tests s’effectueront avec une webcam Microsoft LifeCam HD3000 compatible avec le module uvcvideo installé par défaut sous linux. Si vous souhaitez une liste des webcams compatibles Linux, allez sur http://www.ideasonboard.org/uvc/




Verifiez si votre webcam est reconnue en la connectant puis en tapant : 
$  sudo dmesg
[    7.198004] usbcore: registered new interface driver uvcvideo
[    7.318708] USB Video Class driver (1.1.1)
[   12.318675] 4:3:1: cannot get freq at ep 0x82
[   12.353092] usbcore: registered new interface driver snd-usb-audio




sudo lsusb -t
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=dwc_otg/1p, 480M
    |__ Port 1: Dev 2, If 0, Class=hub, Driver=hub/3p, 480M
        |__ Port 1: Dev 3, If 0, Class=vend., Driver=smsc95xx, 480M
        |__ Port 2: Dev 4, If 0, Class='bInterfaceClass 0x0e not yet handled', Driver=uvcvideo, 480M
        |__ Port 2: Dev 4, If 1, Class='bInterfaceClass 0x0e not yet handled', Driver=uvcvideo, 480M
        |__ Port 2: Dev 4, If 2, Class=audio, Driver=snd-usb-audio, 480M
        |__ Port 2: Dev 4, If 3, Class=audio, Driver=snd-usb-audio, 480M


Chargez le module qui gère les webcams UVC
$ sudo modprobe uvcvideo
$ lsmod|grep uvcvideo


Pour que le module se charge automatiquement au démarrage : 
    $ sudo nano /etc/modules
et ajouter en fin de fichier :
uvcvideo






## STREAMER SA WEBCAM SUR LE NET AVEC APACHE


Pour streamer votre webcam, nous allons utiliser Apache2 et php5. Avant cela, vérifiez que vous êtes bien dans le groupe “video” avec la commande : 
    $ groups
Si ce n’est pas le cas faites : 
    $ sudo adduser mon_login video && su mon_login 


Nous avons besoin d’apache et de php5, profitons en pour installer un système LAMP (Linux Apache Mysql Php).
 
Installation de MySQL
$ sudo apt-get install -y build-essential make mysql-server


Lancez mysql-secure-installation et suivez les recommandations préconisées
$ sudo mysql_secure_installation

Installation d’Apache2
$ sudo apt-get install -y apache2
Vérifiez l’installation d’Apache 2 en allant sur : http://localhost ou distant http://nom_du_pc





## Installation de PHP5


$ sudo apt-get install -y php5 php5-mysql


Maintenant les fichiers peuvent être créés et sauvegardés sous /var/www/
Créez un fichier phpinfo.php pour tester l’installation de php : 
$ sudo mkdir /var/www/apache2-default
$ sudo nano /var/www/apache2-default/phpinfo.php
ajoutez dedans : 
<?php phpinfo(); ?>
et redémarrez apache2 :
$ sudo service apache2 restart


Via votre navigateur web en local à l’adresse http://localhost/apache2-default/phpinfo.php ou distant http://mon_pc/apache2-default/phpinfo.php vous devrez avoir cette page apparaître avec les différentes informations sur php.





## Installation du programme webcam


Pour une fois le nom est assez évocateur :
$ sudo apt-get install webcam


Créons le fichier de configuration :
$ sudo nano /etc/webcam.conf
[ftp]
host = localhost
user = nobody
pass = xxxxxx
dir =  /var/www/webcam
file = webcam.jpg
tmp = imageup.jpg
local = 1


[grab]
device = /dev/video0
text = Raspbian webcam - %d/%m/%Y %H:%M:%S On Line
delay = 0.5
quality = 640
fg_red = 480
fg_green = 255
fg_blue = 255
#width = 352
#height = 288
delay = 0
#wait = 1
rotate = 0
top = 0
left = 0
bottom = -1
right = -1
#quality = 75
trigger = 0
once = 0


Créons la page php qui affichera les images :
$ sudo mkdir /var/www/webcam
$ sudo nano /var/www/webcam/index.php
<html>
  <head>
    <META HTTP-EQUIV="pragma" CONTENT="no-cache">
    <META HTTP-EQUIV="refresh" CONTENT="0.5">
  </head>
  <body>
     <center>
      <h2>Raspbian’s Webcam</h2>
      <img src="webcam.jpg" >
    </center>
  </body>
</html>


Lancez la webcam : 
    $ sudo webcam /etc/webcam.conf
et allez voir le résultat sur la page web http://mon_pc/webcam/index.php


Avec cette solution, Webcam utilise 44% du CPU, ce qui nous reste 24% du CPU non utilisé. Et niveau mémoire nous utilisons au total 70Mo/118Mo. C’est une solution simple et viable pour streamer sa Webcam, et en utilisant des solutions plus légères qu’Apache il peut etre possible d’obtenir un meilleur rendement.









## STREAMER SA WEBCAM SUR LE NET AVEC FFSERVER


Pour streamer votre webcam, nous allons cette fois-ci utiliser Ffserver. L’avantage de cette solution est d’envoyer une vrai vidéo, au-lieu d’images par images.
Installation
Revenez dans votre terminal et installez mplayer et ffmpeg : 
$ sudo apt-get install mplayer ffmpeg


## Configuration


Créez le fichier ffserver.conf de configuration sous le dossier /root : 
    $ sudo nano /root/ffserver.conf


Port 8090
BindAddress 0.0.0.0    
MaxClients 4
MaxBandwidth 10000
NoDaemon
 
<Feed webcam.ffm>
File /tmp/webcam.ffm
FileMaxSize 5M
</Feed>
 
<Stream webcam.asf>
Feed webcam.ffm
Format asf
VideoCodec msmpeg4
VideoFrameRate 2
VideoBufferSize 80000
VideoBitRate 200
VideoQMin 1
VideoQMax 10
VideoSize qvga
PreRoll 0
Noaudio
</Stream>
 
<Stream webcam.mjpeg>
Feed webcam.ffm
Format mpjpeg
VideoSize qvga
VideoFrameRate 2
VideoIntraOnly
Noaudio
Strict -1
</Stream>




FFserver a créé deux flux vidéos : 
- un flux nommé  webcam.asf lisible par VLC
- un flux nommé webcam.mjpeg lisible par tout navigateur internet


Pour économiser votre carte SD, je supprimerai surement le flux “asf” que je n’utiliserai pas.


## Utilisation


Le flux mjpeg est lisible à l’adresse : http://localhost:8090/webcam.mjpeg
Vous pouvez modifier le nom, le port ou la taille (...), il suffit de bien lire le fichier de configuration et l’adapter à vos besoins.
On le lance ainsi : 
ffserver -f /root/ffserver.conf & ffmpeg -v 2 -r 5 -s 640x480 -f video4linux2 -i /dev/video0 http://localhost:8090/webcam.ffm



## CONTROLER DES SERVOSMOTEURS AVEC LE RASPBERRY PI


source : http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/overview


Les Branchements
Le raspberry pi peut controler des servos moteur via sa sortie i2C sur le connecteur GPIO.



## Installation i2c


Intallez les bibliothèques i2c-tools et  python-smbus pour programmer utiliser l’i2c et Python :
$ sudo apt-get install python i2c-tools python-smbus


Vous pouvez charger immédiatement les modules : 
$ sudo modprobe  -a i2c-bcm2708
$ sudo modprobe  -a i2c-bcm2708i2c-dev


Pour charger automatiquement les modules au démarrage rajoutez-les dans le fichier modules:
$ sudo nano /etc/modules
i2c-bcm2708
i2c-dev


Par défaut ces modules sont blacklistés, pour enlevé cette sécurité veuillez éditez et commenter : 
$ sudo nano /etc/modprobe.d/raspi-blacklist.conf
avant : 
blacklist spi-bcm2708
blacklist i2c-bcm2708
après :
# blacklist spi-bcm2708
# blacklist i2c-bcm2708






## Découverte du matériel disponible via i2c


La bibliothèque i2c-tools va nous servir à scanner nos ports:
$ sudo i2cdetect -y -a 0 (pour la version 1 du Raspberry Pi qui a 256Mo de RAM)
$ sudo i2cdetect -y -a 1 (pour la version 2 du Raspberry Pi qui a 512Mo de RAM) 


sudo i2cdetect -y -a 0
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00: 00 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: 70 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


voir maintenant pour la suite : http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/using-the-adafruit-library









## OPENCV ET RASPBERRY PI


Pour streamer votre webcam c’est bien, mais disposer de la bibliothèque d’Open CV vous ouvrira de nouveaux horizons.


Installation d’OpenCV Python Geany Python-pygame
http://www.samontab.com/web/2012/06/installing-opencv-2-4-1-ubuntu-12-04-lts/


## Prérequis pour OpenCV


La compilation d’OpenCV n’est possible que sur des cartes SD supérieures à 4 Gigas. Sur une carte 4 Gigas, même avec 1Giga de livre, vous aurez des problèmes pour compiler le projet. Une autre solution est de cross-compiler, mais ça complique.


Pour commencer nous allons nous donner les droits de compilation : 
$ sudo usermod -aG src mon_login
$ su mon_login


Et comme tout bon élève nous faisons nos mises à jour, pour éviter les soucis de dépendances non à jour :
$ sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade


## Installons les paquets nécessaires à OpenCV : 


sous wheezy
$ sudo apt-get install build-essential libgtk2.0-dev libjpeg8-dev libtiff4-dev libjasper-dev libopenexr-dev cmake python-dev python-numpy python-tk libtdb-dev libeigen2-dev yasm libfaad-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libqt4-dev libqt4-opengl-dev sphinx-common texlive-latex-extra libv4l-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev murrine-themes gtk2-engines-pixbuf


sous jeanny
$ sudo apt-get install build-essential libgtk2.0-dev libjpeg-dev libtiff4-dev libjasper-dev libopenexr-dev cmake python-dev python-numpy python-tk libtdb-dev libeigen2-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libqt5-dev libqt5-opengl-dev sphinx-common texlive-latex-extra libv4l-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev murrine-themes gtk2-engines-pixbuf


## Puis téléchargeons manuellement l’archive d’OpenCV :
 $ cd ~/
$ wget https://github.com/Itseez/opencv/archive/2.4.8.tar.gz.  
Dezippez là puis copiez le dossier obtenu directement sous home:
$ tar -xvf  2.4.8.tar.gz. 








## Compilation d’OpenCV


Créons le dossier “release” de compilation dans le dossier d’OpenCV
$ cd opencv-2.4.8/
$ mkdir release
$ cd release/




$ cmake -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_OPENGL=ON ..


Voici le retour de la commande CMAKE  : 


--   Java:
--     ant:                         NO
--     JNI:                         NO
--     Java tests:                  NO
--
--   Documentation:
--     Build Documentation:         YES
--     Sphinx:                      /usr/bin/sphinx-build (ver 1.1.3)
--     PdfLaTeX compiler:           /usr/bin/pdflatex
--
--   Tests and samples:
--     Tests:                       YES
--     Performance tests:           YES
--     C/C++ Examples:              YES
--
--   Install path:                  /usr/local
--   cvconfig.h is in:              /home/mon_login/opencv-2.4.8/release
-- -----------------------------------------------------------------
--
-- Configuring done
-- Generating done
-- Build files have been written to: /home/mon_login/opencv-2.4.8/release




$ make
$ sudo make install
 
nb : /usr/local/share/OpenCV/haarcascades/haarcascade_fullbody.xml




## Configuration d’OpenCV


Il nous reste maintenant à configurer OpenCV. Pour cela nous allons créer le fichier opencv.conf:
$ sudo nano /etc/ld.so.conf.d/opencv.conf
Et rajouter le code : 
/usr/local/lib
Puis nous reconfigurons la bibliothèque avec cet ajout :
$ sudo ldconfig
Editons aussi le fichier bash.bashrc
$ sudo nano /etc/bash.bashrc
Et rajoutons les deux lignes qui indiquent les chemins des bibliothèques
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
export PKG_CONFIG_PATH





Pour prendre en compte tous les changements, il faut redémarrer Raspbian : 
$ sudo shutdown -r now









Capturez en live de votre webcam avec OpenCV
#!/usr/bin/env python


import cv2.cv as cv
import time


cv.NamedWindow("camera", 1)


capture = cv.CaptureFromCAM(0)


continuer = True
while(continuer):
    img = cv.QueryFrame(capture)
    cv.ShowImage("camera", img)
    if cv.WaitKey(10) != -1:
            break


Capturez en live votre webcam avec PyGame
#!/usr/bin/env python
import pygame, sys, pygame.camera


from pygame.locals import *
pygame.init()
pygame.camera.init()


cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()
image = cam.get_image()


size = width, height = 640, 480
screen = pygame.display.set_mode(size)
imagerect = image.get_rect()
screen.blit(image, imagerect)
pygame.display.flip()


continuer = True
while(continuer):
  image = cam.get_image()
  screen.blit(image, imagerect)
  pygame.display.flip()
  for event in pygame.event.get():
    if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
      continuer=False
cam.stop()
pygame.quit()


Capturez en live Laplacien avec OpenCV


#!/usr/bin/python
import urllib2
import cv2.cv as cv
import sys


if __name__ == "__main__":
    laplace = None
    colorlaplace = None
    planes = [ None, None, None ]
    capture = None


    capture = cv.CreateCameraCapture(0)


    if not capture:
        print "Could not initialize capturing..."
        sys.exit(-1)
        
    cv.NamedWindow("Laplacian", 1)


    while True:
        frame = cv.QueryFrame(capture)
        if frame:
            if not laplace:
                planes = [cv.CreateImage((frame.width, frame.height), 8, 1) for i in range(3)]
                laplace = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_16S, 1)
                colorlaplace = cv.CreateImage((frame.width, frame.height), 8, 3)


            cv.Split(frame, planes[0], planes[1], planes[2], None)
            for plane in planes:
                cv.Laplace(plane, laplace, 3)
                cv.ConvertScaleAbs(laplace, plane, 1, 0)


            cv.Merge(planes[0], planes[1], planes[2], None, colorlaplace)


            cv.ShowImage("Laplacian", colorlaplace)


        if cv.WaitKey(10) != -1:
            break


    cv.DestroyWindow("Laplacian")




## Prendre une photo avec OpenCV



#!/usr/bin/python
import cv2.cv as cv
import datetime


cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)
i=1
while i < 10 :
    img = cv.QueryFrame(capture)
    i = i+1
now = datetime.datetime.now()
now = str(now)
fname='image_'+now+'.jpg'
cv.SaveImage(fname, img)    




















## Reconnaissance faciale simple


source : http://blog.jozilla.net/2008/06/27/fun-with-python-opencv-and-face-detection/


#!/usr/bin/python

import sys
import cv2.cv as cv
from optparse import OptionParser


# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size


min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0


def detect_and_draw(img, cascade):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)


    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)


    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)


    cv.EqualizeHist(small_img, small_img)


    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)


    cv.ShowImage("result", img)


if __name__ == '__main__':


    parser = OptionParser(usage = "usage: %prog [options] [camera_index]")
    parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
    (options, args) = parser.parse_args()


    cascade = cv.Load(options.cascade)
    capture = cv.CreateCameraCapture(0)
    #if len(args) != 1:
    #    parser.print_help()
    #    sys.exit(1)


    #input_name = args[0]
    #if input_name.isdigit():
    #    capture = cv.CreateCameraCapture(int(input_name))
    #else:
    #    capture = None


    cv.NamedWindow("result", 1)


    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
            
            detect_and_draw(frame_copy, cascade)            


            if cv.WaitKey(10) != -1:
                break
    #else:
    #    image = cv.LoadImage(input_name, 1)
    #    detect_and_draw(image, cascade)
    #    cv.WaitKey(0)


    cv.DestroyWindow("result")






### Reconnaissance faciale + MOUSTACHE







#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This program is demonstration of OpenCV
Python implementation by: Nicolas TROTE
"""
import sys
import cv2.cv as cv
from optparse import OptionParser


# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size


min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0


def detect_and_draw(img, cascade, mask):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)


    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)


    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)


    cv.EqualizeHist(small_img, small_img)


    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            for ((x, y, w, h), n) in faces:
                
                # Affichage du carré de recherche
                xmoustache = int((x * image_scale)+w * 0.5)
                ymoustache = int((y * image_scale)+ h * 1.25)
                wmoustache = int(w * 0.5 * image_scale)
                hmoustache = int(h * 0.19 * image_scale)
                img_mask = cv.CreateImage((wmoustache,hmoustache),mask.depth,mask.nChannels)
                cv.SetImageROI(img,(xmoustache, ymoustache, wmoustache ,hmoustache))
                cv.Resize(mask,img_mask,cv.CV_INTER_LINEAR)
                
                # Affichage du carré de recherche
                cv.Sub(img,img_mask,img)
                cv.ResetImageROI(img)
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                #cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)


    cv.ShowImage("result", img)


if __name__ == '__main__':


    parser = OptionParser(usage = "usage: %prog [options] [camera_index]")
    parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
    (options, args) = parser.parse_args()
    mask = cv.LoadImage("moustache-383-129.png")
    
    cascade = cv.Load(options.cascade)
    capture = cv.CreateCameraCapture(0)
    cv.NamedWindow("result", 1)


    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
            
            detect_and_draw(frame_copy, cascade, mask)            


            if cv.WaitKey(10) != -1:
                break


    cv.DestroyWindow("result")
