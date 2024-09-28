from colorama import Fore,Style
import requests as rq 
import argparse
import json
import re


print(Fore.YELLOW+"""
      ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
         ____                               _____           _     
       / ___|  __ _  ___  ___  __ _ _ __   |_   _|__   ___ | |___ 
       \___ \ / _` |/ _ \/ __|/ _` | '__|    | |/ _ \ / _ \| / __|
        ___) | (_| |  __/\__ \ (_| | |       | | (_) | (_) | \__ \ 
       |____/ \__,_|\___||___/\__,_|_|       |_|\___/ \___/|_|___/
          
          If you have any questions, ask me on Twitter: @bandar_b8
      ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
      
      """.title()+Style.RESET_ALL)



parser = argparse.ArgumentParser(description="this tools to scan by use passive scan ;")
parser.add_argument('-d', '--domain', type=str, required=True, help="please without https:// or http://")
args = parser.parse_args()

url = args.domain

if not url.startswith('https://') and url.startswith('http://'):
    url = 'http://' + url

hed = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/json',
    'Connection': 'close',
}


first_scan = f"https://crt.sh/?q={url}&output=json"


try:
    # إرسال الطلب إلى first_scan
    send_to = rq.get(first_scan, headers=hed)
    
    if send_to.status_code == 200:
        jss = send_to.json()
        for i in jss:
            # استرجاع وتجزئة الساب دومينات
            subdomains = i.get('name_value', 'N/A').split('\n')
            for subdomain in subdomains:
                # تحقق باستخدام تعبير منتظم لاستخراج الساب دومين فقط
                if re.match(r"^[*.\w-]+\.\w+$", subdomain):
                    print(f"Subdomain: --> {Fore.BLUE+subdomain}")
                    
                    
except rq.exceptions.RequestException as e:
    print(f"Connection error: {e}")