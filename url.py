from colorama import Fore, Style
import requests as rq
import argparse
import json
import re
import os

print(Fore.YELLOW + """
      ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
  _____ _       _     _____          _   
/ ____ | |     | |   / ____|        | |  
| (___ | | __ _| | _| (___   ___  __| |  
 \___ \| |/ _` | |/ /\___ \ / _ \/ _` |  
 ____) | | (_| |   < ____) |  __/ (_| |  
|_____/|_|\__,_|_|\_\_____/ \___|\__,_|  

          
          If you have any questions, ask me on Twitter: @bandar_b8
      ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
      """.title() + Style.RESET_ALL)

parser = argparse.ArgumentParser(description="This tool scans for subdomains using passive methods.")
parser.add_argument('-d', '--domain', type=str, required=True, help="Please provide a domain without https:// or http://")
args = parser.parse_args()

url = args.domain



hed = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/json',
    'Connection': 'close',
}

first_scan = f"https://crt.sh/?q={url}&output=json"
domain_name = url.split("//")[-1] 
domain_name = domain_name.split("/")[0]


try:
    send_to = rq.get(first_scan, headers=hed)
    
    if send_to.status_code == 200:
        jss = send_to.json()
        subdomains_found = set()  
        for i in jss:
            
            subdomains = i.get('name_value', 'N/A').split('\n')
            for subdomain in subdomains:
                
                if re.match(r"^[*.\w-]+\.\w+$", subdomain):
                    subdomains_found.add(subdomain.strip())  

        
        with open(f"{domain_name}.txt", "w") as f:  
            for subdomain in subdomains_found:
                f.write(f"{subdomain}\n")
    
    else:
        print(f"Failed to retrieve data: {send_to.status_code}")

except rq.exceptions.RequestException as e:
    print(f"Connection error: {e}")
