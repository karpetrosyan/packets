import logging
import socket
import typing

from .ethernet import EthernetPacket
from .handlers import Handler
from .ip import IPPacket
from .icmp import ICMPPacket

logger = logging.getLogger("packets")
class RawTransport:

    def __init__(self,
                 interface: typing.Optional[str],
                 socket_options: typing.Optional[typing.Iterable[typing.Tuple[int, int, int]]] = None):
        self._socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        # if interface:
        #     self._socket.bind((interface, 0))
        if socket_options:
            for option in socket_options:
                self._socket.setsockopt(*option)

    def listen_packets(self, handlers: typing.List[Handler]):
        raise NotImplementedError


class SyncRawTransport(RawTransport):

    def listen_packets(self, handlers: typing.List[Handler]):
        while True:
            logger.debug("Receiving a packet")
            packet = self._socket.recv(1024*1024)
            logger.debug("Packet was received")
            invalid_handlers = set()
            ethernet_packet = EthernetPacket.parse(packet=packet[:14])
            logger.debug("Packet successfully parsed to ethernet packet")
            for handler in handlers:
                if handler not in invalid_handlers:
                    logger.debug(f"Processing ethernet packet for handler `{handler.name}`")
                    is_valid = handler.process_datalink(ethernet_packet)
                    logger.debug(f"Ethernet packet is {'valid' if is_valid else 'invalid'} for handler `{handler.name}`")
                    if not is_valid:
                        invalid_handlers.add(handler)

            logger.debug("Packet successfully parsed to ip packet")
            ip_packet = IPPacket.parse(packet[14:])
            for handler in handlers:
                if handler not in invalid_handlers:
                    logger.debug(f"Processing ip packet for handler `{handler.name}`")
                    is_valid = handler.process_network(ip_packet)
                    logger.debug(f"Ip packet is {'valid' if is_valid else 'invalid'} for handler `{handler.name}`")
                    if not is_valid:
                        invalid_handlers.add(handler)

            try:
                icmp = ICMPPacket.get_from_packet(ip_packet.data)
            except Exception as e:
                ...
            # print([handler for handler in handlers if handler not in invalid_handlers])