"""
election-scraper.py: třetí projekt do Engeto Online Python Akademie
author: Jan Slechta
email: janslechta31@gmail.com
discord: honzas0100
"""

import csv
from requests import get
from bs4 import BeautifulSoup 
import sys
import urllib.request

#if len(sys/argv) != 3:
#        print("zadej dva argumenty")



def get_page(url):
    response = get(url)
    return BeautifulSoup(response.text, features="html.parser") 

def scrape_web_page(url):
    soup = get_page(url)
    extracted_data = {}
    all_tr = soup.find_all("tr")   
    for tr in all_tr:
        try:
            pomocna = tr.find('td', class_='cislo')
            cislo = pomocna.find('a').string
            url = pomocna.find('a', href= True)
            data_url_obce = "https://volby.cz/pls/ps2017nss/"+url['href']
            nazev = tr.find('td', class_="overflow_name").string


            soup2 = get_page(data_url_obce)
            table_data2 = soup2.find_all("td", class_ ='cislo')
            volici = table_data2[3].string
            vydane_obalky = table_data2[4].string
            platne_hlasy = table_data2[7].string

            extracted_data[cislo] = {
                'Kód obce' : cislo,
                'Název obce': nazev,
                'URL obce' : data_url_obce,
                'Voliči v seznamu' : volici,
                'Vydané obálky' : vydane_obalky,
                'Platné hlasy' : platne_hlasy,
            }

            table2 = soup2.find_all('table', class_='table')
            trs_2 = table2[1].find_all('tr') + table2[2].find_all('tr')
            
            for tr in trs_2:
                try:       
                    strana = tr.find('td',class_ = "overflow_name").text
                    strana_hlasy = tr.find('td', {"class" : "cislo", "headers" : "t1sa2 t1sb3"}).text
                    extracted_data[cislo][strana] = strana_hlasy
                except AttributeError:
                   continue

            for tr in trs_2:
                try:       
                    strana = tr.find('td',class_ = "overflow_name").text
                    strana_hlasy = tr.find('td', {"class" : "cislo", "headers" : "t2sa2 t2sb3"}).text
                    extracted_data[cislo][strana] = strana_hlasy
                except AttributeError:
                    continue
    
        except AttributeError:
            continue
        
    return extracted_data


def header(url):
    soup = get_page(url)
    try:
        obec = soup.find('td', attrs= {'class': 'cislo', 'headers': 't1sa1 t1sb1'}).a
        url_obce = "https://volby.cz/pls/ps2017nss/"+obec['href']
        response = get(url_obce)
        soup_2 = BeautifulSoup(response.content, 'html.parser')
        strany = soup_2.find_all('tr')
        zahlavi = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    except AttributeError:
        print("Nastala chyba při stahování nebo řazení dat,zkontrolujte správnost adresy pro stažení. Ukončuji program.")
        quit()
    
    for i in strany:
        try:
            strana = i.find('td', class_='overflow_name').string
            zahlavi.append(strana)
        except AttributeError:
            continue
    return list(zahlavi)


def write_to_csv(extracted_data,output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        zahlavi = header(url)
        writer.writerow(zahlavi)
        for obec_data in extracted_data.values():
            obec_data_filtered = {key: obec_data[key] for key in zahlavi}
            writer.writerow(obec_data_filtered.values())

if __name__ == '__main__':
    url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'
    extracted_data = scrape_web_page(url)
    output_file = 'vysledky.csv'
    write_to_csv(extracted_data,output_file)
    