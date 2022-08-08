#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess, os, sys, socket
from itertools import cycle, izip

rDownloadURL = "http://tekosafe.net/xteko3/sub_xtreamcodes_reborn.tar.gz"
rPackages = ["libcurl4", "libxslt1-dev", "libgeoip-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "libpng16-16", "libzip5", "python-is-python2", "libonig-dev" , "mariadb-server"]

def getVersion():
    try: return subprocess.check_output("lsb_release -d".split()).split(":")[-1].strip()
    except: return ""

def prepare():
    global rPackages
    for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        try: os.remove(rFile)
        except: pass
    os.system("apt-get update > /dev/null")
    os.system("apt-get remove --auto-remove libcurl4 -y > /dev/null")
    for rPackage in rPackages: printc("Installing %s" % rPackage)
    os.system("apt-get install %s -y > /dev/null" % rPackage)
    printc("Installing pip2 and python2 paramiko")
    os.system("add-apt-repository universe > /dev/null 2>&1 && curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py > /dev/null 2>&1 && python2 get-pip.py > /dev/null 2>&1 && pip2 install paramiko > /dev/null 2>&1")
    os.system("apt-get install -f > /dev/null")
    try:
        subprocess.check_output("getent passwd xtreamcodes > /dev/null".split())
    except: pass
    os.system("adduser --system --shell /bin/false --group --disabled-login xtreamcodes 2> /dev/null")
    if not os.path.exists("/home/xtreamcodes"): os.mkdir("/home/xtreamcodes")
    return True

def install():
    global rInstall, rDownloadURL
    rURL = rDownloadURL
    os.system('wget -q -O "/tmp/xtreamcodes.tar.gz" "%s"' % rURL)
    if os.path.exists("/tmp/xtreamcodes.tar.gz"):
        os.system('tar -zxvf "/tmp/xtreamcodes.tar.gz" -C "/home/xtreamcodes/" > /dev/null')
        try: os.remove("/tmp/xtreamcodes.tar.gz")
        except: pass
        return True
    return False

def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    try: os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except: pass
    rf = open('/home/xtreamcodes/iptv_xtream_codes/config', 'wb')
    rf.write(''.join(chr(ord(c)^ord(k)) for c,k in izip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1'))).encode('base64').replace('\n', ''))
    rf.close()

def configure():
    rYou = "http://xcodes.mine.nu/XCodes/youtube-dl" 
    rCheckGeo = "http://xcodes.mine.nu/XCodes/check_geolite.sh"
    if not "/home/xtreamcodes/iptv_xtream_codes/" in open("/etc/fstab").read():
        rFile = open("/etc/fstab", "a")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        rFile.close()
    if not "/sbin/iptables" in open("/etc/sudoers").read(): os.system('sed -i "s|xtreamcodes|#xtreamcodes|g" /etc/sudoers && echo "xtreamcodes ALL=(root) NOPASSWD: /sbin/iptables" >> /etc/sudoers')
    if not os.path.exists("/etc/init.d/xtreamcodes"): os.system("touch /etc/init.d/xtreamcodes")
    if not "Provides" in open("/etc/init.d/xtreamcodes").read():
        os.system("rm /etc/init.d/xtreamcodes")
        rStart = open("/etc/init.d/xtreamcodes", "w")
        rStart.write("#!/bin/bash\n### BEGIN INIT INFO\n# Provides:          xtreamcodes\n# Required-Start:    $all\n# Required-Stop:\n# Default-Start:     2 3 4 5\n# Default-Stop:\n# Short-Description: Run /etc/init.d/xtreamcodes if it exist\n### END INIT INFO\n/home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")
        rStart.close()
        os.system("chmod 755 /etc/init.d/xtreamcodes 2>/dev/null")
        os.system("update-rc.d xtreamcodes defaults 2>/dev/null")
    try: os.remove("/usr/bin/ffmpeg 2>/dev/null || /usr/bin/ffmpeg 2>/dev/null")
    except: pass
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"): os.mkdir("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")
    os.system("ln -s /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/")
    os.system("chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    os.system("rm /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    os.system("wget -q http://xcodes.mine.nu/XCodes/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/XCodes/GeoLite2.mmdb")
    os.system("wget -q http://xcodes.mine.nu/XCodes/pid_monitor.php -O /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php")
    os.system("wget -q http://xcodes.mine.nu/XCodes/config.py -O /home/xtreamcodes/iptv_xtream_codes/config.py")
    os.system("rm /usr/local/bin/youtube-dl 2>/dev/null")
    os.system('wget -q -O "/usr/local/bin/youtube-dl" "%s"' % rYou)
    os.system("sudo chmod a+rx /usr/local/bin/youtube-dl")
    os.system('wget -q -O "/home/xtreamcodes/iptv_xtream_codes/check_geolite.sh" "%s"' % rCheckGeo)
    if not "check_geolite.sh" in open("/etc/crontab").read(): os.system('echo "*/1 *   * * * root /home/xtreamcodes/iptv_xtream_codes/./check_geolite.sh" >> /etc/crontab')
    if not "/home/xtreamcodes 2>/dev/null" in open("/home/xtreamcodes/iptv_xtream_codes/start_services.sh").read():   
        os.system("sed -i 's|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
        os.system("sed -i 's|chmod -R 777 /home/xtreamcodes|chmod -R 777 /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
    os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
    os.system("mount -a")
    os.system("chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null")
    os.system("chmod -R 0777 /home/xtreamcodes 2>/dev/null")
    os.system("chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    os.system("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php 2>/dev/null")
    if not "xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    if not "api.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts')
    if not "downloads.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts')
    if not "xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')

def setPorts(rPorts):
    os.system("sed -i 's/listen 25461;/listen %d;/g' /home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf" % rPorts[0])
    os.system("sed -i 's/:25461/:%d/g' /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf" % rPorts[0])
    os.system("sed -i 's/listen 25463 ssl;/listen %d ssl;/g' /home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf" % rPorts[1])
    os.system("sed -i 's/listen 25462;/listen %d;/g' /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf" % rPorts[2])
    
def start():
    os.system("chown xtreamcodes:xtreamcodes /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("chmod 777 /home/xtreamcodes/iptv_xtream_codes/config")
    os.system("/home/xtreamcodes/iptv_xtream_codes/start_services.sh 2>/dev/null")

if __name__ == "__main__":
    rHost = sys.argv[1]
    rPort = int(sys.argv[2])
    rUsername = sys.argv[3]
    rPassword = sys.argv[4]
    rDatabase = sys.argv[5]
    rServerID = int(sys.argv[6])
    try: rPorts = [int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])]
    except: rPorts = None
    prepare()
    if not install(): sys.exit(1)
    encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
    configure()
    if rPorts: setPorts(rPorts)
    start()
