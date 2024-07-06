#  _   _   _  __          __     _____  _   _ _____ _   _  _____   _   _   _ 
# | | | | | | \ \        / /\   |  __ \| \ | |_   _| \ | |/ ____| | | | | | |
# | | | | | |  \ \  /\  / /  \  | |__) |  \| | | | |  \| | |  __  | | | | | |
# | | | | | |   \ \/  \/ / /\ \ |  _  /| . ` | | | | . ` | | |_ | | | | | | |
# |_| |_| |_|    \  /\  / ____ \| | \ \| |\  |_| |_| |\  | |__| | |_| |_| |_|
# (_) (_) (_)     \/  \/_/    \_\_|  \_\_| \_|_____|_| \_|\_____| (_) (_) (_)

#This software was made for educational, legal and ethical use, the author of this software is not liable for any unethical or illegal use of this software!
#By using this software, you agree to the legal and ethical use of this software!

import os
def sp():
	print("")
def rt():
	os.system('python3 ./menu.py')
def helplist():
	print("start - Starts the attack.\nconf - Configures attack.\nhelp - Shows this menu.\nexit - Exits program.")

print("\n[Menu]")
input = input()

if (input=="help"):
	sp()
	helplist()
	rt()
elif (input=="start"):
	sp()
	os.system('python3 ./flood.py')
	rt()
elif (input=="conf"):
	os.system('python3 ./config.py')
elif (input=="exit"):
	exit()
else:
	sp()
	print("Unknown command!")
	rt()
