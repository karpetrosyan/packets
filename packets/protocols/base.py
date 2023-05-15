import typing


class ProtocolPacket:

    def get_layer(self):
        raise NotImplementedError()


class DataLinkPacket(ProtocolPacket):
    def get_type(self):
        raise NotImplementedError()

    def get_layer(self):
        return 2

    def __len__(self):
        raise NotImplementedError()


class NetworkPacket(ProtocolPacket):
    def get_proto(self):
        raise NotImplementedError()

    def get_layer(self):
        return 3

    def __len__(self):
        raise NotImplementedError()

class TransportPacket(ProtocolPacket):
    def get_layer(self):
        return 4


class PacketStack:
    def __init__(
        self,
        datalink_packet: typing.Optional[DataLinkPacket] = None,
        network_packet: typing.Optional[NetworkPacket] = None,
        transport_packet: typing.Optional[TransportPacket] = None,
    ):
        self.datalink_packet = datalink_packet
        self.network_packet = network_packet
        self.transport_packet = transport_packet
        self._iter_pointer = 0

    def __len__(self):
        return sum(packet for packet in (self.datalink_packet, self.network_packet, self.transport_packet))

    def __iter__(self):
        for packet in self.datalink_packet, self.network_packet, self.transport_packet:
            if packet is None:
                return
            yield packet
        return

    def push(self, packet: ProtocolPacket):
        if not self.datalink_packet:
            if not isinstance(packet, DataLinkPacket):
                raise Exception("Invalid Packet")
            self.datalink_packet = packet
        elif not self.network_packet:
            if not isinstance(packet, NetworkPacket):
                raise Exception("Invalid Packet")
            self.network_packet = packet
        elif not self.transport_packet:
            if not isinstance(packet, TransportPacket):
                raise Exception("Invalid Packet")
            self.transport_packet = packet
        else:
            assert "Packet can not be received"
