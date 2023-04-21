import typing
import socket
from .ip import IPPacket
from .ethernet import EthernetPacket

class RawTransport:

    def __init__(self,
                 interface: typing.Optional[str],
                 ipv4: bool = True,
                 ipv6: bool = False,
                 socket_options: typing.Optional[typing.Iterable[typing.Tuple[int, int, int]]] = None):
        self._socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        # if interface:
            # self._socket.bind((interface, 0))
        if socket_options:
            for option in socket_options:
                self._socket.setsockopt(*option)

    def listen_packets(self):
        raise NotImplementedError


class SyncRawTransport(RawTransport):


    def listen_packets(self):

        while True:
            packet = self._socket.recv(1024*1024)
            p = EthernetPacket.parse(packet=packet[:14])
            ip = IPPacket.parse(packet[14:])
            print(p)
            print(ip)
            try:
                print(ip.icmp)
            except Exception: ...
class AsyncRawTransport(RawTransport):

    async def listen_packets(self):
        ...