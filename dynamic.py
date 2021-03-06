#/usr/bin/python3
import sys
import argparse

class Hostinfo():
    def __init__(self, name='inname') -> None:
        self.name = name
        self.ignorenames = ['name', 'ignorenames']
    
    def __str__(self) -> str:
        props = {}
        for (name,value) in self.__dict__.items():
            if name.find('ansible') ==0:
                props[name] = value
        return str(props)

    def getdict(self):
        props = {}
        for (name,value) in self.__dict__.items():
            if name not in self.ignorenames:
                props[name] = value
        return props

    def sethost(self, host):
        self.ansible_host = host

class GroupsInfo():
    def __init__(self) -> None:
        self.groups = {'unnamed':[]}
        self.hosts = {}
        self.groupvars = {}

    def addgroup(self, gname):
        if gname not in self.groups.keys():
            self.groups[gname] = []
    
    def delgroup(self, gname):
        if gname in self.groups.keys():
            del self.groups[gname]

    def checkhostswithoutgroups(self):
        for hostname, host in self.hosts.items():
            withoutgroup = True
            for group in self.groups.values():
                if hostname in group:
                    withoutgroup = False
                    break
            if withoutgroup:
                self.addhostgroup(tmphost=host)
    
    def addhost(self, tmphost=Hostinfo()):
        if tmphost.name not in self.hosts.keys():
            self.hosts[tmphost.name] = tmphost

    def delhost(self, thost=Hostinfo()):
        hostname = thost.name
        if hostname in self.hosts.keys():
            del self.hosts[hostname]
            for tmpg in self.groups.values():
                if hostname in tmpg:
                    tmpg.remove(hostname)

    def gethost(self, hostname=''):
        if hostname in self.hosts.keys():
            return(self.hosts[hostname].getdict())
        return ''

    def addhostgroup(self, gname='unnamed', tmphost=Hostinfo()):
        self.addgroup(gname)
        if tmphost.name not in self.groups[gname]:
            self.groups[gname].append(tmphost.name)
        self.addhost(tmphost=tmphost)
        if tmphost.name in self.groups['unnamed'] and gname != 'unnamed':
            self.groups['unnamed'].remove(tmphost.name)

    def delhostgroup(self, gname, tmphost=Hostinfo()):
        if gname in self.groups.keys():
            if tmphost.name in self.groups[gname]:
                self.groups[gname].remove(tmphost.name)
    
    def __str__(self) -> str:
        self.checkhostswithoutgroups()
        resinfo = {'_meta':{'hostvars':{}}}
        for host in self.hosts.values():
            resinfo['_meta']['hostvars'][host.name] = host.getdict()
        for key,val in self.groups.items(): # ?????????? ???????????????? ???????????? vars: vd = dict(envone='one',envtwo='two'), ?????????? td = dict(hosts=val,vars=vd)
            if len(val) > 0:
                resinfo[key] = dict(hosts=val)
        strout = str(resinfo)
        return strout.replace("'",'"')

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?')
    parser.add_argument('--list', action='store_const', const=True)
    return parser

def testinit():
    m1 = Hostinfo(name='testserver')
    m1.sethost('192.168.1.195')
    m1.key_file = "/etc/nginx/ssl/nginx.key"
    m1.cert_file = "/etc/nginx/ssl/nginx.crt"
    m1.conf_file = "/etc/nginx/sites-available/default"
    m1.server_name = "ansible.bobrobotirk.ru" 
    myall = GroupsInfo()
    myall.addhostgroup('webservers', m1)
    return myall

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    ghlist = testinit()
    if namespace.host:
        hostinfo = ghlist.gethost(namespace.host)
        print(hostinfo)
    if namespace.list:
        print(ghlist)
    
    