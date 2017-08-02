import threading
import psutil
import time
import os,  datetime
import sys
import csv
from time import gmtime, strftime 

import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM



AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}


def client_sock_count(port):
    count = 0
    for c in psutil.net_connections(kind='tcp4'):
        if ((c.laddr[0] != '0.0.0.0') and (c.laddr[1] == port)and (c.status == 'ESTABLISHED')):
            count += 1
    return count

def memory_usage_ps():
    import subprocess
    out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
    stdout=subprocess.PIPE).communicate()[0].split(b'\n')
    vsz_index = out[0].split().index(b'RSS')
    mem = float(out[1].split()[vsz_index]) / 1024
    return mem

def memory_usage_psutil():
    # return the memory usage in MB
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem
def memory_usage_resource():
    import resource
    rusage_denom = 1024.
    if sys.platform == 'darwin':
        # ... it seems that in OSX the output is different units ...
        rusage_denom = rusage_denom * rusage_denom
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / rusage_denom
    return mem
def show_system_stat():
    threading.Timer(1.0, show_system_stat).start()
    #print('show_system_stat')
    with open('sys_health.csv', 'a', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        #data = [['service', 'timestamp','cpu_percent', vm-total','vm-available', 'vm-percent','vm-used','vm-free','net-byte-sent','net-byte-recv','net-packet_sent','net-packet-recv','net-errin','net-errout','net-dropin','net-dropout']]
        #a.writerows(data)  
        #for i in range(10):
        print(client_sock_count(5000))
        a.writerows( [['system',strftime("%Y-%m-%d %H:%M:%S", gmtime()),  str(psutil.cpu_percent()), str(psutil.virtual_memory()[0]/1024), 
                                str(psutil.virtual_memory()[1]/1024), str(psutil.virtual_memory()[2]/1024 ), str(psutil.virtual_memory()[3]/1024), 
                                str(psutil.virtual_memory()[4]/1024), str(psutil.net_io_counters()[0]), str( psutil.net_io_counters()[1]), 
                                str(psutil.net_io_counters()[2]), str(psutil.net_io_counters()[3]), str(psutil.net_io_counters()[4]), 
                                str(psutil.net_io_counters()[5]), str(psutil.net_io_counters()[6]), str(psutil.net_io_counters()[7]), 
                                client_sock_count(5000)]]) 
            
def log_process_stat():
    threading.Timer(1.0, log_process_stat).start()
    #print('log_process_stat')
    with open('process_health.csv', 'a', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        #data = [['timestamp','pid', 'ppid','cwd','parent','status','username','create_time','cpu-percent','cpu-num','mem-rss', 'mem-vms','mem-shared','mem-percent','conn-count','num-thread','num-fds','is-running']]
        #a.writerows(data)  
        #for i in range(10):
        
        for i in range(len(sys.argv)-1):
            #print(sys.argv[i+1])        
            p = psutil.Process(pid= int(sys.argv[i+1]))
            timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            #print(p.pid)
            a.writerows( [[strftime("%Y-%m-%d %H:%M:%S", gmtime()), str(p.pid), str(p.ppid()), str(p.cwd()),
                           str(p.parent()), str(p.status()), str(p.username()),
                           str(p.create_time()), str(p.cpu_percent()), str( p.cpu_num()), 
                           str( p.memory_info()[0]), str( p.memory_info()[1]),
                           str(p.memory_info()[2]), str( p.memory_percent()), 
                           str(p.connections().count(0)), str(p.num_threads()),
                           str(p.num_fds()), str( p.is_running())
                           ]])   
def printit():
    threading.Timer(1.0, printit).start()
    print ("Hello, World!")

def init():
    #print(x)
    with open('process_health.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            data = [['timestamp','pid', 'ppid','cwd','parent','status','username','create_time',
                     'cpu-percent','cpu-num','mem-rss', 'mem-vms','mem-shared','mem-percent',
                     'conn-count','num-thread','num-fds','is-running']]
            a.writerows(data)   
    fp.close()
    with open('sys_health.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            data = [['service', 'timestamp','cpu_percent', 'vm-total','vm-available', 'vm-percent',
                     'vm-used','vm-free','net-byte-sent','net-byte-recv','net-packet_sent','net-packet-recv',
                     'net-errin','net-errout','net-dropin','net-dropout','clients']]
            a.writerows(data) 
    fp.close()
def main():
    
    x  = strftime("%Y%m%d_%H%M%S", gmtime())
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print(sys.argv)
    #print(len(sys.argv))
    #for i in range(len(sys.argv)-1):
        #print(sys.argv[i+1])

    init()    
    threading.Timer(1.0, show_system_stat).start()
    threading.Timer(1.0, log_process_stat).start()
    #show_system_stat()
    #log_process_stat()
    ##if len(sys.argv) == 1:
        ##show_system_stat()
    #print(memory_usage_ps())
    #print(memory_usage_psutil())
    #print(memory_usage_resource())
    
    
if __name__ == '__main__':
    #printit()
    main()