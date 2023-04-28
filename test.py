from packets.handlers import Handler
from packets.transports import SyncTransport

handler = Handler(name="test")

transport = SyncTransport(handlers=[handler])

transport.serve()
