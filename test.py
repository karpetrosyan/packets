from packets import transports
tr = transports.SyncRawTransport("enp0s3", [])

tr.listen_packets()