import socket
import fcntl
import struct
import sys
import ipaddr
import os
from time import sleep
from p0f import P0f, P0fException
class host:
#class used to represent any active host detected on the network
    def __init__ (self, ipAddress):
        self.ipAddress=ipAddress
        self.OS=' '
        self.ports=dict.fromkeys(range(80,500), 1)
        #boolean dictionary to flag whether a port is open or not
    
    def analyzeHost(self,p0f):
    #Analyses host to find open ports and OS
        self.findOpenPorts()
        self.findOS(p0f)

    def findOpenPorts(self):
        try:
            for port, state in self.ports.iteritems():
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                #socket creats TCP connection to determine 
                s.settimeout(0.9)
                r=s.connect_ex((self.ipAddress,port))
                if r==0:
                    self.ports[port]=0
                s.close()
        except socket.error:
            print "Could not connect to host"
            sys.exit()


    def findOS(self,p0f):
        data=p0f.get_info(self.ipAddress)
        #Sends call to p0f API with host ip address as parameter which returns data object containing os information of passed host
        self.OS=str(data['os_name'])
        #Pulls name of OS
        self.OS+=str(data['os_flavor'])
        #Pulls OS version
                         
    def printIp(self):
        print ipAddres

    def printOS(self):
        print self.OS

    def writeToFile(self):
        f=open('Output.txt','a')
        f.write(self.ipAddress)
        f.write(' {}'.format(self.OS))
        for port, state in self.ports.iteritems():
            if state==0:
                f.write(' {}'.format(port))
        f.write('\n')
        f.close()


def get_netmask(intf):
#http://stackoverflow.com/questions/936444/retrieving-network-mask-in-python
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',intf))[20:24])

def get_ip_address(intf):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', intf[:15]))[20:24])

os.system('sudo p0f -f /etc/p0f.fp -i eth0 -s /var/run/p0f.sock -d > /dev/null ')
#Runs p0f in the background to capture all packets used throughout the host detection and performs analysis on them to later determine the OS of a remote host
intf='eth0'  
netmask=get_netmask(intf)

hostIp=get_ip_address(intf)
   
curSubnet= ipaddr.IPNetwork(hostIp+'/'+netmask)
#Creates an object using Google's ipaddr library that models the network based on the subnet and Ip give

networkAddr=curSubnet.network
#Stored in the IPnetwork object is the network address of the network which is automatically calculated on instanciation, this is needed to iterate through all IP addresses in the network


f=open('Output.txt','w').close()
#Clears file if one was already created from previous use of script
totalIPs=0
#Sets IP counter to 0
p0f=P0f('/var/run/p0f.sock')
#creats P0f object to handle API calls to background daemon which socket loc as parameter
for i in range(curSubnet.network,curSubnet.network+10):
#Counts total IPs between Network address and Broadcast Address
    totalIPs+=1
for j in range(1,totalIPs+1):
#Iterates through all Ip addresses in Subnet
    print 'Processing {} out of {} IP Addresses\r'.format(j, totalIPs),
    #Prints progress check for processing
    sys.stdout.flush()
    #http://stackoverflow.com/questions/3488704/how-to-rewrite-output-in-terminal 
    sleep(1)
    ip=curSubnet.network+j
    #Calculated current IP address
    response=os.system("ping {} -c1 > /dev/null".format(ip))
    #Sends ping to IP address 
    if response==0 and str(ip)!=str(hostIp):
    #Confirms Availability
        rHost=host(str(ip))
        #Creates a host object for host if found active
        rHost.analyzeHost(p0f)
        rHost.writeToFile()
sys.stdout.flush()
#Clears screen when script is finishing as to not leave output
print'\n' 	








