import sys
import argparse

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?')
    parser.add_argument('--list', action='store_const', const=True)
    return parser



def gethost(hostname):
    hostname1={ "ansible_ssh_host":  "127.0.0.1",  "ansible_ssh_port":  22, "ansible_ssh_user":  "sergey"}
    hostname2={ "ansible_ssh_host":  "127.0.0.2",  "ansible_ssh_port":  22, "ansible_ssh_user":  "sergey"}
    hostsinfo = {"main": hostname1, "sec": hostname2}
    hostinfo = hostsinfo.get(hostname)
    return hostinfo
 
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
 
    #print (namespace)
 
    if namespace.host:
        hostinfo = gethost(namespace.host)
        print(hostinfo)
    if namespace.list:
        print("list need")