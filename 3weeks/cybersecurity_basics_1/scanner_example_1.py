# This was taken from the Medium article "Creating a Vulnerability Scanner in Python" by Aleksa Zatezalo, found at https://medium.com/offensive-security-walk-throughs/creating-a-vulnerability-scanner-in-python-b5b59817b38d

import sys
import os
import socket

def retBanner(ip, port):
    """
    Takes the ip, ip of a remote server and its respective port, port.
    Returns the banner running at the location.
    """

    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return
