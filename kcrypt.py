#!/usr/bin/python


import sys
import os, re, socket, time, select, random, getopt
from Crypto.Cipher import AES


# AES KEY
key = "fdsl;mewrjope456fds4fbvfnjwaugfo"

str1="".decode('hex')
str2="".decode('hex')
#str3="".decode('hex')
str3 = "".decode('hex')
#str4="".decode('hex')

str5 = "".decode('hex')
str6 = "".decode('hex')
# Encrypt or decrypt the passed string
def cipher(type, str):
    # AES requires the input length to be in multiples of 16 
    aesobj = AES.new(key, AES.MODE_ECB)
    if str is not None:
        while (len(str) % 16 is not 0):
            str = str + " "
        if type == "enc":
            return aesobj.encrypt(str)
        elif type == "dec":
            return aesobj.decrypt(str)
    else:
        return None



# Create the command string
# cmd => the command type
# cid => confirmation id for command type == confirm 
def createmsg(cmd,cid=None):
        sp = "%"
        msg = "lan_phone" + sp + rmac + sp + password + sp
        if cmd == "open":
                msg = msg + "open" + sp + "request"
        elif cmd == "close":
                msg = msg + "close" + sp + "request"
        elif cmd == "confirm":
            msg = msg + "confirm#"+ cid + sp + "request"
        return msg

## Get the confirmation ID
def get_confirmid(m):
    p = re.search(r"confirm#(\w+)", m)          # to printout the confirmation number only!!
    if p is not None:
        return p.group(1)
    else:
        return None

            

class Fonts:
    BOLD = '\033[1m'
    END = '\033[0m'

def main():
    print ""
    print Fonts.BOLD + "[+] kankun crypt script" + Fonts.END
    print ""
    cmd = None

    dec = cipher("dec", str1)
    print "Decrypted str1: (" + dec + ")"

    dec = cipher("dec", str2)
    print "Decrypted str2: (" + dec + ")"

    dec = cipher("dec", str3)
    print "Decrypted str3: (" + dec + ")"

    dec = cipher("dec", str6)
    print "Decrypted str6: (" + dec + ")"

if __name__ == "__main__":
    main()
