import socket
import re
from typing import final
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose = False):
    open_ports = []
    regexp = re.compile("[a-zA-Z]")
    argIsIp = True
    try:
        if regexp.search(target):
            argIsIp = False
            target = socket.gethostbyname(target)

        try:
            hostname = socket.gethostbyaddr(target)[0]
        except socket.herror:
            hostname = ""
        rg = range(port_range[0],port_range[1]+1)
        for port in rg:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            if(s.connect_ex((target, int(port)))):
                #  print(str(port) +" closed.")
                pass
            else:
                open_ports.append(port)
                #  print(str(port) +" is open.")

            s.close()
    except socket.gaierror:
        if argIsIp:
            return "Error: Invalid IP address"
        else:
            return "Error: Invalid hostname"


    if verbose:
        finalStr = ""
        if(hostname):
            finalStr += "Open ports for {} ({})".format(hostname,target)
        else:
            finalStr += "Open ports for {}".format(target)
        finalStr += "\nPORT     SERVICE"
        for port in open_ports:
            portlj = str(port).ljust(9)
            finalStr+= "\n{}{}".format(portlj,ports_and_services.get(port))
        return finalStr


    return(open_ports)