from packets import transports
from packets.handlers import Handler
from packets.filters import Filter
from packets.protocols import Protocol

tr = transports.SyncRawTransport(interface="enp0s3")

def flt(packet):
    return False

filter = Filter(
                filter_functions=[flt],
                proto=Protocol.ip)

ipdestlogger = Handler(name="iplogger",
                       filters=(filter, ),
                       callback=None)

tr.listen_packets(handlers=[ipdestlogger])
