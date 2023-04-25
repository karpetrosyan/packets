from .data_units import DataUnit, Packet, Frame, Segment


class Layer:

    def incapsulate(self):
        raise NotImplementedError()

    def decapsulate(self, data: DataUnit):
        raise NotImplementedError()

    def get_layer(self):
        raise NotImplementedError()

class DataLinkLayer(Layer):

    def incapsulate(self):
        ...

    def decapsulate(self, data: Frame):
        ...

    def get_layer(self):
        ...

class NetworkLayer(Layer):

    def incapsulate(self):
        ...

    def decapsulate(self):
        ...

    def get_layer(self):
        ...

class TransportLayer(Layer):

    def incapsulate(self):
        ...

    def decapsulate(self):
        ...

    def get_layer(self):
        ...