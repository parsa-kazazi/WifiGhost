#!/bin/python3
# -*- coding: utf-8 -*-

# This is a Python script for Linux systems to automate wireless auditing
# Required tools: aircrack-ng, aireplay-ng, reaver, pixiewps, airmon-ng, iw, iwconfig
# Suported operation systems: Kali Linux, Parrot OS, BlachArch Linux

# Coded by parsa kazazi
# GitHub: https://github.com/parsa-kazazi


import os
import subprocess
import sys
from threading import Thread
import time


# Colors
red = "\033[91m"
green = "\033[92m"
cyan = "\033[96m"
unset_color = "\033[0m"

os.system("clear && printf '\033]2;WiFiGhost\a'")

print(r"""
                                            _______
 __      ___  __ _  ___ _           _      / _____ \
 \ \    / (_)/ _(_)/ __| |_  ___ __| |_     / ___ \
  \ \/\/ /| |  _| | (_ | ' \/ _ (_-<  _|     /   \
   \_/\_/ |_|_| |_|\___|_||_\___/__/\__|       O

    Automate wireless auditing script

""")

time.sleep(2)


def exit_script():
    s = subprocess.getoutput("ps -e | grep xterm")

    if s != "":
        PID = s.split()[0]
        os.system("kill " + PID)
    
    exit()


def show_networks_list():
    q = input("Show networks list? (y/n) ")
    print()

    if q == "y" or q == "Y":
        subprocess.Popen("xterm -title 'Networks list' -e 'airodump-ng " + interface + "'", shell=True)
    elif q == "n" or q == "N":
        pass
    else:
        print("Aborted.")


print(cyan + "######################### Start #########################" + unset_color + "\n")
sys.stdout.write("Root permission: ")

if subprocess.getoutput("id -u") != "0":
    sys.stdout.write(red + "NO" + unset_color + "\n")
    print("This script needs root permission.")
    print("re-run as sudo. exiting.\n")
    exit_script()
else:
    sys.stdout.write(green + "OK" + unset_color + "\n\n")

print("Checking required tools.\n")

required_tools = ["aircrack-ng", "aireplay-ng", "reaver", "pixiewps", "airmon-ng", "iw", "iwconfig", "xterm"]
not_found_tools = 0

for tool in required_tools:
    sys.stdout.write(tool + " ... ")
    sys.stdout.flush()
    time.sleep(0.3)

    if subprocess.getstatusoutput("which " + tool)[0] != 0:
        sys.stdout.write(red + "Not found" + unset_color + "\n")
        not_found_tools += 1
    else:
        sys.stdout.write(green + "Found: " + unset_color + subprocess.getoutput("which " + tool) + "\n")

if not_found_tools >= 1:
    print("\n" + str(not_found_tools) + " tool(s) was not found. script can't continue.\n")
    exit_script()
else:
    print("\nAll required tools found.\n")

input("Press Enter to continue... ")

print("\n" + cyan + "####################### Interface #######################\n" + unset_color)
print("Select an wireless interface to work with.\n")
print("IFACE               INFO")
print("--------------------------------------------")
print(subprocess.getoutput("iwconfig"))

interface = input("Interface name: ")

if "No such device" in subprocess.getoutput("iwconfig " + interface):
    print("\n" + interface + " : No such device.")
    print("Exiting.\n")
    exit_script()
elif "No such device" in subprocess.getoutput("iw " + interface + " info"):
    print("\n" + interface + " : Not a wireless interface.")
    print("Exiting.\n")
    exit_script()
elif " " in interface:
    print("\nInvalid input.\n")
    exit_script()
else:
    print("\n" + subprocess.getoutput("iw " + interface + " info"))

sys.stdout.write("\n\nEnabling monitor mode on interface " + green + interface + unset_color + " with " + green + "airmon-ng " + unset_color + "... ")
os.system("airmon-ng start " + interface + " > " + os.devnull)
sys.stdout.write(green + "enabled" + unset_color + "\n\n")

input("Press Enter to continue... ")
os.system("clear")

print(cyan + "####################### Main menu #######################" + unset_color + "\n")
print("Select an option:")
print("------------------------------")
print("""1- WPA/WEP key crack
2- WPS pin crack
3- DoS attack
4- Handshake capture
5- Exit
""")

try:
    option = int(input("Option number: "))
except ValueError:
    print("\nInvalid input.\n")
    exit_script()

if option not in [1, 2, 3, 4, 5]:
    print("\nInvalid input.\n")
    exit_script()
else:
    pass


if option == 1:
    print("\n" + cyan + "##################### WPA/WEP crack #####################" + unset_color + "\n")

    show_networks_list()
    
    target_essid = input("Target essid (AP name): ")
    handshake = input("Handshake file address: ")
    wordlist = input("Wordlist file (Enter to default): ")

    if wordlist == "":
        wordlist = "Files/rockyou.txt"
    time.sleep(2)

    if wordlist == "":
        print("\nRunning " + green + " aircrack-ng" + unset_color + " with " + green + "default" + unset_color + " wordlist.\n")
    else:
        print("\nRunning " + green + " aircrack-ng" + unset_color + " with '" + green + wordlist + unset_color + " wordlist.\n")
    
    time.sleep(3)
    os.system("aircrack-ng " + handshake + " -w " + wordlist + " -e " + target_essid)
    print("\nAttack finished. exiting.\n")
    exit_script()
elif option == 2:
    print("\n" + cyan + "####################### WPS crack #######################" + unset_color + "\n")
        
    show_networks_list()
    
    target_bssid = input("Target bssid (mac address): ")

    print("\nRunning " + green + "reaver" + unset_color + " with bssid " + target_bssid + "\n")
    time.sleep(3)
    os.system("reaver -i " + interface + " -b " + target_bssid + " --pixie-dust -vv")
    print("\nAttack finished. exiting.\n")
    exit_script()
elif option == 3:
    print("\n" + cyan + "##################### DoS attacking #####################" + unset_color + "\n")
    print("Select attack mode:")
    print("------------------------------")
    print("1- DeAuth DoS attack")
    print("2- FakeAuth DoS attack")

    try:
        attack_mode = int(input("\nAttack mode (1 or 2): "))
    except ValueError:
        print("\nInvalid input.\n")
        exit_script()
    
    if attack_mode not in [1, 2]:
        print("\nInvalid input.\n")
        exit_script()
        
    show_networks_list()
    
    if attack_mode == 1:
        target_bssid = input("Target bssid (mac address): ")

        try:
            deauth_count = int(input("DeAuth count: "))
        except ValueError:
            print("\nInvalid input.\n")
            exit_script()
        
        if deauth_count > 100000000000000000:
            print("\nDeAuth count too big.\n")
            exit_script()
        
        print("\nRunning " + green + "aireplay-ng" + unset_color + " , attack mode: DeAuth DoS attack")
        print("Press CTRL+C to finish attack.\n")

        time.sleep(5)

        os.system("aireplay-ng -a " + target_bssid + " --deauth " + str(deauth_count) + " " + interface)
        print("\nAttack finished. exiting.\n")
        exit_script()

    elif attack_mode == 2:
        target_bssid = input("Target bssid (mac address): ")

        try:
            fakeauth_count = int(input("FakeAuth count: "))
        except ValueError:
            print("\nInvalid input.\n")
            exit_script()
        
        if fakeauth_count > 100000000000000000:
            print("\nFakeAuth count too big.\n")
            exit_script()
        
        print("\nRunning " + green + "aireplay-ng" + unset_color + " , attack mode: FakeAuth DoS attack")
        print("Press CTRL+C to finish attack.\n")

        time.sleep(5)

        os.system("aireplay-ng -a " + target_bssid + " --fakeauth " + str(fakeauth_count) + " " + interface)
        print("\nAttack finished. exiting.\n")
        exit_script()

elif option == 4:
    print("\n" + cyan + "################### Handshake capture ###################" + unset_color + "\n")
            
    show_networks_list()
    
    target_essid = input("Target essid (AP name): ")

    print("\nRunning " + green + "airodump-ng" + unset_color + " to capture handshake.")
    print("Press q to finish capture.\n")

    time.sleep(5)

    handshake_filename = "Handshake-" + target_essid
    os.mkdir("Handshake")
    os.system("airodump-ng --essid " + target_essid + " -w " + "Handshake/" + handshake_filename + " " + interface)

    print("\nCapture finished. handshake saved to directory: " + green + os.getcwd() + "/Handshake/" + unset_color + "\n")

    exit_script()

elif option == 5:
    print("\nExiting.\n")
    exit_script()
