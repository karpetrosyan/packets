from packets.transports import SyncTransport
from packets.handlers import Handler

handler = Handler(name="test")

transport = SyncTransport(handlers=[handler])

transport.serve()