from packets.handlers import Handler
from packets.transports import SyncTransport
from packets.filters import Filter
from packets.protocols.ipv4 import IPv4Packet
from packets.protocols.base import NetworkPacket
def callback(packet_stack):
    print(packet_stack.network_packet)

def network_filter(packet: NetworkPacket):
    if isinstance(packet, IPv4Packet):
        return packet.src_addr == "10.0.2.15"
    return False

f = Filter(name="test", network_filter=network_filter)

handler = Handler(name="test", filters=[f], callback=callback)

transport = SyncTransport(handlers=[handler])

transport.serve()
