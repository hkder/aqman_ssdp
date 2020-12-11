from ssdpy import SSDPServer
import socket
import fcntl
import struct
import subprocess

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24]
    )

def get_interfaces():
    out = subprocess.Popen(['cat', '/proc/net/dev'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    stdout = stdout.decode('utf-8')
    l = stdout.split('\n')

    interfaces = []
    for interface in l[2:]:
        iface = interface.split(":")[0]
        if iface != "":
            interfaces.append(iface.strip())
        
    return interfaces

if __name__ == '__main__':
    for interface in get_interfaces():
        if interface[0] == 'e':
            ip_address = get_ip_address(interface)
            break
        elif 'wlan' in interface:
            ip_address = get_ip_address(interface)

    port = 8297
    ssdp_response_server = SSDPServer(usn = "hass-main-server", device_type = "ssdp:kictechhass", location=f"http://{ip_address}:{port}") 
    ssdp_response_server.serve_forever()
