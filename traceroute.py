import socket
import random
from collections import namedtuple

HOST = 'wp.pl'

PortRange = namedtuple('PortRange', ['min', 'max'])


class UDPProbePacket:
    def __init__(self, dst_addr, ttl=1):
        self.ttl = ttl
        self.dst_addr = dst_addr


class ICMPRespPacket:
    pass


class TraceCommunication:
    port_range = PortRange(min=33434, max=33464)
    max_hop = 30
    probe_num = 3
    receive_timeout = 1
    ICMP_MAX_SIZE = 1508

    def __init__(self, dst_host):
        self.ttl = 1
        self.dst_host = dst_host
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
        self.recv_sock.settimeout(self.receive_timeout)
        self.set_ttl(self.ttl)

    def set_ttl(self, ttl):
        self.send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    def probe(self):
        port = random.randint(self.port_range.min, self.port_range.max)
        hop = None
        address = None
        dst_addr = socket.gethostbyname(self.dst_host)
        while address != dst_addr and hop != self.dst_host and self.ttl < self.max_hop:
            self.send_sock.sendto(b'', (self.dst_host, port))
            try:
                data, address = self.recv_sock.recvfrom(self.ICMP_MAX_SIZE)
                address = address[0]
            except socket.timeout:
                address = None
            try:
                hop = socket.gethostbyaddr(address)[0] if address is not None else None
            except socket.herror:
                hop = None
            print(hop, address)
            self.ttl += 1
            self.set_ttl(self.ttl)

if __name__ == '__main__':
    trace = TraceCommunication(HOST)
    trace.probe()
