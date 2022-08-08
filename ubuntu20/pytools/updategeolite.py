#!/usr/bin/python2
# -*- coding: utf-8 -*-
# update panel
import subprocess, os, sys
from itertools import cycle, izip

def updategeolite():
    os.system("apt-get install e2fsprogs -y && chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb ; wget http://xcodes.mine.nu/XCodes/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb && chown xtreamcodes.xtreamcodes /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb && chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    return True

def start():
    os.system("/home/xtreamcodes/iptv_xtream_codes/start_services.sh 2>/dev/null")

if __name__ == "__main__":
    updategeolite()
    #start()
