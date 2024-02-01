from bs4 import BeautifulSoup
import requests
import re
from qb_info import qb
import numpy as np
import pandas as pd
import pymongo

print("Starting web scrape for QB records")

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

winQBs = []
loseQBs = []

winningLosers = []
losingLosers = []

skippedQBs = []
allQBs = []

for winner in winners:
    name = re.sub('[^A-Za-z0-9\s]+', '', winner)
    winQBs.append(qb(name))
    allQBs.append(name)
for loser in losers:
    name = re.sub('[^A-Za-z0-9\s]+', '', loser)
    loseQBs.append(qb(name))
    if name not in allQBs:
        allQBs.append(name)

qbVals = np.empty(shape=(len(allQBs), 4), dtype="S40")
i = 0

names = []

# loop through tables in soup
# qb is passed in so modifications can occur
# output is False if qb info was found, True if skipped occurred
def loopThroughSoup(soup, currQB):
    tables = soup.find_all('table')
    for table in tables:
        if table.attrs == {'class': ['statistics']}:
            for row in table.tbody.findAll('tr'):
                try:
                    currQB.getRecord(row.findAll('td')[2].contents[0])
                    if currQB.wins != 0 or currQB.losses != 0:
                        return False
                except Exception as e:
                        print(e)
                        continue
    return True

for qb in winQBs:
    names.append(qb.name)
    qbVals[i,0] = qb.name
    qbVals[i,3] = "Won"
    skipped = False
    if qb.name in qb.manualRecords:
        qb.getRecord(qb.manualRecords[qb.name])
    else:
        url = 'https://www.footballdb.com/players/' + qb.getShortName()
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        response = requests.get(url, headers=headers)
        soup2 = BeautifulSoup(response.content, 'html.parser')

        skipped = loopThroughSoup(soup2, qb)
    if skipped:
        skippedQBs.append(qb.name)
        qbVals[i,1] = ''
        qbVals[i,2] = ''
    else:
        qbVals[i,1] = str(qb.wins) + "-" + str(qb.losses) + "-" + str(qb.ties)
        qbVals[i,2] = "{:.3f}".format(qb.pct)
        if qb.pct < 0.500:
            winningLosers.append(qb.name)
    i+=1

for qb in loseQBs:
    skipped = False
    qbIsLoser = True
    if qb.name in names:
        qbIsLoser = False

    if qbIsLoser:
        qbVals[i,0] = qb.name
        qbVals[i,3] = "Lost"
        if qb.name in qb.manualRecords:
            qb.getRecord(qb.manualRecords[qb.name])
        else:
            url = 'https://www.footballdb.com/players/' + qb.getShortName()
            headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
            response = requests.get(url, headers=headers)
            soup1 = BeautifulSoup(response.content, 'html.parser')

            skipped = loopThroughSoup(soup1, qb)
        if skipped:
            skippedQBs.append(qb.name)
            qbVals[i,1] = ''
            qbVals[i,2] = ''
        else:
            qbVals[i,1] = str(qb.wins) + "-" + str(qb.losses) + "-" + str(qb.ties)
            qbVals[i,2] = "{:.3f}".format(qb.pct)
            if qb.pct < 0.500:
                losingLosers.append(qb.name)
        i+=1

qbValsDF = pd.DataFrame(data=qbVals, columns=["Name", "W-L-T", "Percentage", "Won_Lost_Superbowl"], dtype=str, index=[str(num) for num in range(len(qbVals))])
losersDF = pd.DataFrame(data=np.array(losingLosers), columns=["Name"], dtype=str, index=[str(num) for num in range(len(losingLosers))])
winnersDF = pd.DataFrame(data=np.array(winningLosers), columns=["Name"], dtype=str, index=[str(num) for num in range(len(winningLosers))])

# create or access existing MongoDB database to store records
client = pymongo.MongoClient()
db = client["superbowl_qb_records"]
collection = db["qb_records"]

db["qb_records"].insert_many(qbValsDF.to_dict('records'))

# send collections of each type of qb - losing records who won and lost a superbowl
loserCollection = db["lost_sb_with_losing_record"]
db["lost_sb_with_losing_record"].insert_many(losersDF.to_dict('records'))
winnerCollection = db["won_sb_with_losing_record"]
db["won_sb_with_losing_record"].insert_many(winnersDF.to_dict('records'))

print("Database \"superbowl_qb_records\" created with collections \"qb_records\", \"lost_sb_with_losing_record\", and \"won_sb_with_losing_record\"")