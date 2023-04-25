

def enforce_mac_address(address: bytes):
    ip_parts = []
    for byte in address:
        ip_parts.append(str(byte))
    return "-".join(ip_parts)


def enforce_ipv4(ip: bytes):
    ip_parts = []
    for byte in ip:
        ip_parts.append(str(byte))
    return ".".join(ip_parts)