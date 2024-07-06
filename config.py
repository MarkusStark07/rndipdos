#  _   _   _  __          __     _____  _   _ _____ _   _  _____   _   _   _ 
# | | | | | | \ \        / /\   |  __ \| \ | |_   _| \ | |/ ____| | | | | | |
# | | | | | |  \ \  /\  / /  \  | |__) |  \| | | | |  \| | |  __  | | | | | |
# | | | | | |   \ \/  \/ / /\ \ |  _  /| . ` | | | | . ` | | |_ | | | | | | |
# |_| |_| |_|    \  /\  / ____ \| | \ \| |\  |_| |_| |\  | |__| | |_| |_| |_|
# (_) (_) (_)     \/  \/_/    \_\_|  \_\_| \_|_____|_| \_|\_____| (_) (_) (_)

#This software was made for educational, legal and ethical use, the author of this software is not liable for any unethical or illegal use of this software!
#By using this software, you agree to the legal and ethical use of this software!

import configparser
import os
import re

config_file_path = './rndipdos.ini'
config = configparser.ConfigParser()
config.read(config_file_path)

target_ip_value = config['DEFAULT'].get('target_ip', None)
target_port_value = config['DEFAULT'].get('target_port', None) 
packet_size_value = config['DEFAULT'].get('packet_size', None)
threads_value = config['DEFAULT'].get('threads', None)

def sp():
        print("")

def rt():
        os.system('python3 ./config.py')

def helplist():
        print("ip - Sets target ip address.\nport - Sets target port.\nsize - Sets packet size.\nhelp - Shows this menu.\ncurrent - Shows you the current configuration.\nback - Returns you back to [Menu].")

def current():
	print(f"target ip: {target_ip_value}")
	print(f"target port: {target_port_value}")
	print(f"packet size: {packet_size_value}")

def is_valid_ipv4(ip):
	pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
	if pattern.match(ip):
		parts = ip.split('.')
		for part in parts:
			if not 0 <= int(part) <= 255:
				return False
			return True
		return False

def save():
	with open(config_file_path, 'w') as configfile:
		config.write(configfile)

def target_ip():
	print("Please enter your target's ip address:")
	target_ip_input = input()
	if is_valid_ipv4(target_ip_input):
		config.set('DEFAULT', 'target_ip', target_ip_input)
		save()
	else:
		print("\nEntered input is not IPv4 format!")

def target_port():
	print("Please enter your target's port:")
	target_port_input = int(input())
	if 0 <= target_port_input <= 65535:
		target_port_input_string = str(target_port_input)
		config.set('DEFAULT', 'target_port', target_port_input_string)
		save()
	else:
		print("\nEntered input is not within rage of TCP ports!")

def packet_size():
	print("Please enter size of packets in bytes:")
	packet_size_input = int(input())
	if 1 <= packet_size_input <= 65535:
		packet_size_input_string = str(packet_size_input)
		config.set('DEFAULT', 'packet_size', packet_size_input_string)
		save()
	else:
		print("\nEntered input is not within rage of packet sizes! (min: 1 & max: 65535)")


print("\n[Menu/Configure]")
user_input = input()

if (user_input=="help"):
	sp()
	helplist()
	rt()
elif (user_input=="current"):
	sp()
	current()
	rt()
elif (user_input=="back"):
	sp()
	os.system('python3 ./menu.py')
elif (user_input=="ip"):
	sp()
	target_ip()
	rt()
elif (user_input=="port"):
	sp()
	target_port()
	rt()
elif (user_input=="size"):
	sp()
	packet_size()
	rt()
else:
	sp()
	print("Uknown command!")
	rt()
