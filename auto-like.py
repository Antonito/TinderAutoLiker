#!/usr/bin/env python3

import sys
import argparse
import requests
import json

__author__="Antoine Bache"

def getUserInfo(header, user):
    r = requests.get(API_URL + "user/" + user, headers=header);
    if r.status_code == 200:
        data = json.loads(r.text)
        print(json.dumps(data, indent=2, sort_keys=False))
        return 0
    return 1

def autoLike(header):
    r = requests.get(API_URL + "user/recs", headers=header);
    if r.status_code == 200:
        data = json.loads(r.text)
        print("==== LIKING ====")
        with open("profile.txt", "a") as outfile:
            for profile in data["results"]:
                like_r = requests.get(API_URL + "like/" + profile["_id"], headers=header)
                if like_r.status_code == 200:
                    if profile["name"] == "Tinder Team":
                        print("[!] You ran out of likes")
                        return 1
                    line = "Liked " + profile["_id"] + " [ " + profile["name"] + " ]"
                    print(line)
                    outfile.write(line + "\n")
                else:
                    print("[!] Cannot like: " + profile["name"])
            print("==== DONE ====")
        return 0
    else:
        print("[!] Cannot like anyone.")
    return 1

# Parse arguments
parser = argparse.ArgumentParser(description='Automatically like Tinder profiles !')
parser.add_argument("user", metavar="user", help="Get information about this user", action="store", nargs='?')
args = parser.parse_args()

# General infos
API_URL="https://api.gotinder.com/"

# You can get this token by sniffing your phone's traffic
TINDER_TOKEN=""

# Tinder requests
if TINDER_TOKEN == "":
    print("[!] You must specify a TINDER_TOKEN")
    sys.exit(1)
header={"Content-Type": "application/json", "X-Auth-Token": TINDER_TOKEN}

ret = 0
if args.user is not None:
    ret = getUserInfo(header, args.user)
else:
    ret = autoLike(header)
sys.exit(ret)
