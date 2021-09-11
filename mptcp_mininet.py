#!/usr/bin/python

"""
This is a simple example that demonstrates multiple links
between nodes.
"""
### CONFIGURATIONS ###

# sysctl net.mptcp
# sysctl net | grep congestion
# sysctl net | grep 'mptcp\|congestion'

from mininet.link import TCLink
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI

from threading import Timer
"congestion controls:"
#os.system('sysctl -w net.ipv4.tcp_congestion_control=cubic ')
#os.system('modprobe mptcp_coupled && sysctl -w net.ipv4.tcp_congestion_control=lia ')
#os.system('modprobe mptcp_olia && sysctl -w net.ipv4.tcp_congestion_control=olia ')
#os.system('modprobe mptcp_wvegas && sysctl -w net.ipv4.tcp_congestion_control=wvegas ')
#os.system('modprobe mptcp_balia && sysctl -w net.ipv4.tcp_congestion_control=balia ')

"path-managers:"
#os.system('sysctl -w net.mptcp.mptcp_path_manager=default ')
#os.system('sysctl -w net.mptcp.mptcp_path_manager=fullmesh ')
#os.system('echo 1 | sudo tee /sys/module/mptcp_fullmesh/parameters/num_subflows')
#os.system('modprobe mptcp_ndiffports && sysctl -w net.mptcp.mptcp_path_manager=ndiffports ')
#os.system('echo 1 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows')
#os.system('modprobe mptcp_binder && sysctl -w net.mptcp.mptcp_path_manager=binder ')

"scheduler:"
#os.system('sysctl -w net.mptcp.mptcp_scheduler=default ')
#os.system('modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin ')
#os.system('echo 1 | sudo tee /sys/module/mptcp_rr/parameters/num_segments')
#os.system('echo Y | sudo tee /sys/module/mptcp_rr/parameters/cwnd_limited')
#os.system('modprobe mptcp_redundant && sysctl -w net.mptcp.mptcp_scheduler=redundant ')


max_queue_size = 100

def updateLink(link, delay):
    link.intf1.config(delay=delay)
    link.intf2.config(delay=delay)

def updateDelay(link):    
    # global cnt
    # if cnt*5+1 > 5731:
    #     return
    delay = 0
    Timer(5, updateDelay).start()
    # now = datetime.datetime.now()
    # print('the '+ str(cnt) + ' is running')
    # ts = now.strftime('%Y-%m-%d %H:%M:%S')
    # line = f'{ts}'
    # print(line)
    # filename = '../StarLink/delay/' + str(cnt*40+1) + '.mat'
    # mat = loadmat(filename)
    # delay = mat['delay']
    # for i in range(num_orbit):
    #     for j in range(sat_per_orbit):
    #         num_sat1 = i*sat_per_orbit+j
    #         num_sat2 = i*sat_per_orbit+(j+1)%sat_per_orbit 
    #         num_sat3 = ((i+1)%num_orbit)*sat_per_orbit + j
    updateLink(link, delay)
    updateLink(link, delay)
    # cnt = cnt + 1

def multiPathSetting():
    net = Mininet(cleanup=True)

    h1 = net.addHost('h1', ip='10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.1.3')
    c0 = net.addController('c0')

    link1 = net.addLink(h1, h2, cls=TCLink, intfName1='h1-eth0',
                        intfName2='h2-eth0', bw=5, delay='1ms', max_queue_size=max_queue_size)
    link2 = net.addLink(h1, h2, cls=TCLink, intfName1='h1-eth1',
                        intfName2='h2-eth1', bw=5, delay='1ms', max_queue_size=max_queue_size)

    h1.setIP('10.0.1.1', intf='h1-eth0')
    h1.setIP('10.0.1.2', intf='h1-eth1')
    h2.setIP('10.0.1.3', intf='h2-eth0')
    h2.setIP('10.0.1.4', intf='h2-eth1')

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    multiPathSetting()
