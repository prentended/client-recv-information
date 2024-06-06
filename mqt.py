from scapy.all import ARP, Ether, srp

def scan_network(ip_range):
    # 创建一个Ether/ARP请求包
    arp_request = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp_request

    # 发送包并接收响应
    result = srp(packet, timeout=2, verbose=False)[0]

    # 创建一个字典来存储结果
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

# 示例使用
ip_range = "192.168.50.39/24"
devices = scan_network(ip_range)
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")
