import sys
import argparse
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

class Hostinfo():
    def __init__(self, name='inname') -> None:
        self.name = name
    
    def __str__(self) -> str:
        props = {}
        for (name,value) in self.__dict__.items():
            if name.find('ansible')>-1:
                props[name] = value
        return str(props)

    def getdict(self):
        props = {}
        for (name,value) in self.__dict__.items():
            if name.find('ansible')>-1:
                props[name] = value
        return props

    def sethost(self, host):
        self.ansible_ssh_host = host

class Groupinfo():
    def __init__(self, gname) -> None:
        self.gname = gname
        self.glist = []

class Groups():
    def __init__(self) -> None:
        self.gdict = {}
        self.hosts = {}

    def addgroup(self, gname):
        if gname not in self.gdict.keys():
            self.gdict[gname] = []
    
    def delgroup(self, gname):
        if gname in self.gdict.keys():
            del self.gdict[gname]
    
    def addhost(self, tmphost=Hostinfo()):
        if tmphost.name not in self.hosts.keys():
            self.hosts[tmphost.name] = tmphost

    def delhost(self, thost=Hostinfo()):
        hostname = thost.name
        if hostname in self.hosts.keys():
            del self.hosts[hostname]
            for tmpg in self.gdict.values():
                if hostname in tmpg:
                    tmpg.remove(hostname)

    def gethost(self, hostname=''):
        if hostname in self.hosts.keys():
            return(self.hosts[hostname].getdict())
        return ''

    def addhostgroup(self, gname, tmphost=Hostinfo()):
        self.addgroup(gname)
        if tmphost.name not in self.gdict[gname]:
            self.gdict[gname].append(tmphost.name)
        self.addhost(tmphost=tmphost)

    def delhostgroup(self, gname, tmphost=Hostinfo()):
        if gname in self.gdict.keys():
            if tmphost.name in self.gdict[gname]:
                self.gdict[gname].remove(tmphost.name)
    
    def __str__(self) -> str:
        outh = {}
        for host in self.hosts.values():
            outh[host.name] = host.getdict()
        outf = dict(hostvars=outh)
        outdict = {}
        for key,val in self.gdict.items():
            td = dict(hosts=val,vars="")
            outdict[key] = td
        out = str(dict(outdict, _meta=outf))
        return out.replace("'",'"')

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?')
    parser.add_argument('--list', action='store_const', const=True)
    return parser

def testinit():
    m1 = Hostinfo(name='testserver')
    m1.sethost('192.168.1.195')
    m2 = Groups()
    m2.addhostgroup('webservers', m1)
    return m2

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    ghlist = testinit()
    if namespace.host:
        hostinfo = ghlist.gethost(namespace.host)
        print(hostinfo)
    if namespace.list:
        print(ghlist)
    
    