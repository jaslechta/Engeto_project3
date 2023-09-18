# Engeto_project3 - election sraper
- **Author:** Jan Slechta
- **Email:** janslechta31@gmail.com
- **Discord:** honzas0100

## Description: 
This Python script is designed to scrape parlament election results data from website volby.cz (link [here](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)) and save it to a CSV file. It retrieves data about registered voters, issued envelopes, valid votes, and results for various political parties in different regions.

## Instalation: 
Packages that are used in the code are saved in file "requirements.txt". For instalation is recomended create new virtual enviroment and use pip3 to install packages:
```
pip3 --version                              #validate version of the pip3
pip install -r requirements.txt             #install packages from requirements.txt file
```

## Execution of the scipt:
For execution file election-scraper.py in cmd are required two arguments.
- link-to-location: URL of the choosen territorial unit from website https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
- output-file: name of the output file - consist of the name and .csv extension (example: results_prostejov.csv)
```
python election-scraper.py <link-to-location> <output-file>
python election-scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "results_prostejov.csv" #example of the command
```

## Example of the program:
On the website https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ choose one territorial unit "Prostejov" by clicking on the "X" in the column "Výběr obce". Then execute the election-scraper.py with two arguments:
  1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
  2. argument: results_prostejov.csv
### Exucution of the program:
```
python election-scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "results_prostejov.csv"
```

### Ouptut of the terminal:
```
Data processing
Results saved as: 'results_prostejov.csv'
quiting election-scraper
```

### Example of the file "results_prostejov.csv":
```
Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana,....
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,Bílovice-Lutotín,431,279,275,13,0,0,32,0,8,40,1,0,4,0,0,30,0,3,83,0,0,22,0,0,0,1,38,0
589284,Biskupice,238,132,131,14,0,0,9,0,5,24,2,1,1,0,0,10,2,0,34,0,0,10,0,0,0,0,19,0
589292,Bohuslavice,376,236,236,20,0,0,23,0,3,22,3,4,6,0,1,17,0,4,53,1,1,39,0,0,3,0,36,0
....
```
