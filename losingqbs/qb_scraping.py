from bs4 import BeautifulSoup
import requests
import re
from qb_info import qb
import numpy as np
import pandas as pd

winners = []
losers = []

url = 'https://en.wikipedia.org/wiki/List_of_Super_Bowl_starting_quarterbacks'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
for row in soup.find_all('table')[1].tbody.findAll('tr'):
    try:
        winner = row.findAll('td')[2].text.replace('\n', '').replace('MVP', '')
        loser = row.findAll('td')[4].text.replace('\n', '').replace('MVP', '')
        if winner not in winners:
            winners.append(winner)
        if loser not in losers:
            losers.append(loser)
    except:
        continue

# print(losers)

# print([re.sub('[^A-Za-z0-9\s]+', '',i) for i in winners])

winQBs = []
loseQBs = []

winningLosers = []
losingLosers = []

allQBs = []
skipped = []

for winner in winners:
    winQBs.append(qb(re.sub('[^A-Za-z0-9\s]+', '', winner)))
for loser in losers:
    loseQBs.append(qb(re.sub('[^A-Za-z0-9\s]+', '', loser)))

for qb in loseQBs:
    shouldSkip = True
    url = 'https://www.footballdb.com/players/' + qb.getShortName()
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    response = requests.get(url, headers=headers)
    
    #print(url)
    soup1 = BeautifulSoup(response.content, 'html.parser')
    tables = soup1.find_all('table')
    for table in tables:
        if table.attrs == {'class': ['statistics']}:
            for row in table.tbody.findAll('tr'):
                try:
                    qb.getRecord(row.findAll('td')[2].contents[0])
                except Exception as e:
                    print(e)
                    continue
                if qb.wins != 0 or qb.losses != 0:
                    if qb.pct < 0.500:
                        losingLosers.append(qb.name)
                    shouldSkip = False
                    break
        if shouldSkip == False:
            break
    if shouldSkip:
        skipped.append(qb.name)
    
for qb in winQBs:
    shouldSkip = True
    url = 'https://www.footballdb.com/players/' + qb.getShortName()
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    response = requests.get(url, headers=headers)
    
    soup2 = BeautifulSoup(response.content, 'html.parser')
    tables = soup1.find_all('table')
    for table in tables:
        if table.attrs == {'class': ['statistics']}:
            for row in table.tbody.findAll('tr'):
                try:
                    qb.getRecord(row.findAll('td')[2].contents[0])
                except Exception as e:
                    print(e)
                    continue
                if qb.wins != 0 or qb.losses != 0:
                    if qb.pct < 0.500:
                        winningLosers.append(qb.name)
                    shouldSkip = False
                    break
        if shouldSkip == False:
            break
    if shouldSkip:
        skipped.append(qb.name)

print("Starting QBs with a losing overall record that have lost a super bowl are: ")
print(losingLosers)
print("\n")
print("Starting QBs with a losing overall record that have won a super bowl are: ")
print(winningLosers)
print("\nHad to skip: ")
print(skipped)