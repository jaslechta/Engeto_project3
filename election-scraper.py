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

"""
    Retrieves the content of a web page based on the provided URL using an HTTP GET request and parses it with BeautifulSoup.

    :param url: URL address of the web page to analyze.
    :return: BeautifulSoup object representing the analyzed page.
"""
def get_page(url):
    response = get(url)
    return BeautifulSoup(response.text, features="html.parser") 


"""
    Scrapes information about election results from a web page and stores it in a dictionary.

    :param url: URL address of the web page with election results.
    :return: Dictionary containing extracted data about election results.
"""
def scrape_web_page(url):
    soup = get_page(url)
    extracted_data = {}
    all_tr = soup.find_all("tr")   
    for tr in all_tr:
        try:
            td = tr.find('td', class_='cislo')
            code = td.find('a').string
            url = td.find('a', href= True)
            data_url_location = "https://volby.cz/pls/ps2017nss/"+url['href']
            location = tr.find('td', class_="overflow_name").string
            soup2 = get_page(data_url_location)
            table_data2 = soup2.find_all("td", class_ ='cislo')
            registred = table_data2[3].string
            envelopes = table_data2[4].string
            valid = table_data2[7].string
            extracted_data[code] = {
                'Kód obce' : code,
                'Název obce': location,
                'URL obce' : data_url_location,
                'Voliči v seznamu' : registred,
                'Vydané obálky' : envelopes,
                'Platné hlasy' : valid,
            }

            table2 = soup2.find_all('table', class_='table')
            trs_2 = table2[1].find_all('tr') 
            trs_3 = table2[2].find_all('tr')
            
            for tr in trs_2:
                try:       
                    political_party = tr.find('td',class_ = "overflow_name").text
                    votes = tr.find('td', {"class" : "cislo", "headers" : "t1sa2 t1sb3"}).text
                    extracted_data[code][political_party] = votes
                except AttributeError:
                   continue

            for tr in trs_3:
                try:       
                    political_party = tr.find('td',class_ = "overflow_name").text
                    votes = tr.find('td', {"class" : "cislo", "headers" : "t2sa2 t2sb3"}).text
                    extracted_data[code][political_party] = votes
                except AttributeError:
                    continue
    
        except AttributeError:
            continue
        
    return extracted_data

"""
    Retrieves the header for a CSV file based on a web page with election results.

    :param url: URL address of the web page with election results.
    :return: List containing the header for the CSV file.
"""
def get_header(url):
    soup = get_page(url)
    try:
        location = soup.find('td', attrs= {'class': 'cislo', 'headers': 't1sa1 t1sb1'}).a
        url_location = "https://volby.cz/pls/ps2017nss/"+location['href']
        soup_2 = get_page(url_location)
        political_parties = soup_2.find_all('tr')
        header = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    except AttributeError:
        print("There was an error in downloading or processing data, check the addresses for download. Terminating the program.")
        quit()
            
    for i in political_parties:
        try:
            party = i.find('td', class_='overflow_name').string
            header.append(party)
        except AttributeError:
            continue
    return list(header)

"""
    Writes extracted data to a CSV file with consideration of a predefined header.

    :param extracted_data: Extracted data about election results.
    :param output_file: Name of the output CSV file.
    :param url: URL address of the web page with election results.
"""
def write_to_csv(extracted_data,output_file,url):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = get_header(url)
        writer.writerow(header)
        for location_data in extracted_data.values():
            obec_data_filtered = {key: location_data[key] for key in header}
            writer.writerow(obec_data_filtered.values())


"""
    Checks the validity of command-line arguments when running the program.

    :param argv: List of arguments passed to the program.
"""
def check_arguments(argv):
    if len(argv) != 3:
        print(f"Invalid number of arguments,need to be 2 arguments,inserted {(len(argv) - 1)}")
        quit()
    elif "https://volby.cz/pls/ps2017nss/" not in argv[1]:
        print("Invalid URL for download data")
        quit()
    elif not argv[2].endswith(".csv"):
        print("Invalid syntax of output file, name of the file must have a .csv extension")
        quit()

"""
    Main function of the program for scraping election results and saving them to a CSV file.

    :param url: URL address of the web page with election results.
    :param output_file: Name of the output CSV file.
"""
def main(url,output_file):
    try:
        print(f"Data processing")
    except AttributeError:
        print("Unexpected error, ending the program")
        quit()
    
    extracted_data = scrape_web_page(url)
    print(f"Results saved as: '{output_file}'")
    write_to_csv(extracted_data,output_file,url)
    print("quiting election-scraper")

if __name__ == '__main__':
    check_arguments(sys.argv)
    main(sys.argv[1], sys.argv[2])