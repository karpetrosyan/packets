import typing
import socket

class Transport:

    def __init__(self,
                 interface: typing.Optional[str] = None,

                 ):
        self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        if interface:
            self.socket.bind((interface, 0))

    def serve(self, handlers):
        raise NotImplementedError()

    def receive_frame(self):
        raise NotImplementedError()


class SyncTransport(Transport):

    def serve(self, handlers):
        ...

    def receive_frame(self):
        ...