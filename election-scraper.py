"""
election-scraper.py: třetí projekt do Engeto Online Python Akademie
author: Jan Slechta
email: janslechta31@gmail.com
discord: honzas0100
"""

from requests import get
from bs4 import BeautifulSoup 
import sys

#if len(sys/argv) != 3:
#        print("zadej dva argumenty")

address = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
answer = get(address)

rozdelene_html = BeautifulSoup(answer.text, features="html.parser")

table_tag_top = rozdelene_html.find("table", {"class": "table"})

#print(table_tag_top.prettify())
all_tr = table_tag_top.find_all("tr")
print(all_tr[3])
