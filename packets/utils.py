import ipaddress


def enforce_mac_address(address: bytes) -> str:
    ip_parts = []
    for byte in address:
        ip_parts.append(str(byte))
    return "-".join(ip_parts)


def enforce_ipv4(ip: bytes) -> str:
    ip_parts = []
    for byte in ip:
        ip_parts.append(str(byte))
    return ".".join(ip_parts)


def enforce_ipv6(ip: bytes) -> str:
    return str(ipaddress.IPv6Address(ip))
