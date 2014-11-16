import json
import requests
import time
from random import randrange
import xlrd
from xlrd import open_workbook
import xlwt
from tempfile import TemporaryFile

class Data:
    def __init(self): pass

D = Data()

#initialize some global variables to use\
D.blueTeamWin = False
D.purpleTeamWin = False
D.championWinRates = {}
D.championPosition = {}

def getWinRateForEachSummoner(championID , summonerID):
    """ Gets champion data and returns the win rate of that champ """

    stats = requests.get('https://prod.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' +str(summonerID)+'/ranked?api_key=d9f79478-95ed-4def-8060-e8945b834809')
    time.sleep(1)
    
    if stats.status_code == 404:
        return .5
    statsdata = stats.json()

    if "champions" not in statsdata:
        return .5
    
    listOfChampionStats = statsdata["champions"]
    
    for x in range(len(listOfChampionStats)):
        element = listOfChampionStats[x]
        if element["id"] == championID:
            champStats = listOfChampionStats[x]
            winRate = champStats['stats']["totalSessionsWon"] / champStats['stats']["totalSessionsPlayed"]
            return winRate
    return .5


def getDataForEveryone(hostId):


    # Make arrays for our data
    blueTeamWinRates = []
    purpleTeamWinRates = []
    blueTeamChampionWin = []
    purpleTeamChampionWin = []
    blueTeamChampPos = []
    purpleTeamChampPos = []

    time.sleep(1)
    gamestats = requests.get('https://prod.api.pvp.net/api/lol/na/v1.3/game/by-summoner/' +str(hostId)+'/recent?api_key=d9f79478-95ed-4def-8060-e8945b834809')
    gamestatsdata = gamestats.json()

    gameHistory = gamestatsdata['games']
    numberOfGamesInHistory = len(gameHistory)
    gameNumber = randrange(numberOfGamesInHistory)
    
    latestGame = gamestatsdata['games'][gameNumber]
    hostChampionID = latestGame['championId']
    teamID = latestGame['teamId']
    winOrLose = latestGame['stats']['win']
    winRate = getWinRateForEachSummoner(hostChampionID, hostId)
    champName = getChampionNameFromID(hostChampionID)
    championWinRate = D.championWinRates[champName]
    championPosition = D.championPosition[champName]
    
    if teamID == 100:
        blueTeamWinRates.append(winRate)
        blueTeamChampionWin.append(championWinRate)
        blueTeamChampPos.append(championPosition)
        D.blueTeamWin = winOrLose
        D.purpleTeamWin = not winOrLose
    else:
        purpleTeamWinRates.append(winRate)
        purpleTeamChampionWin.append(championWinRate)
        purpleTeamChampPos.append(championPosition)
        D.blueTeamWin = not winOrLose
        D.purpleTeamWin = winOrLose


    if "fellowPlayers" in latestGame:
        allPlayersExceptOrigin = latestGame["fellowPlayers"]
    else:
        print("No fellow players - trying again.")
        return hostId, ['Bad data']
    
    for x in allPlayersExceptOrigin:
        summonerID = x['summonerId']
        championID = x['championId']
        teamID = x['teamId']
        winRate = getWinRateForEachSummoner(championID, summonerID)
        champName = getChampionNameFromID(championID)
        championWinRate = D.championWinRates[champName]
        championPosition = D.championPosition[champName]
        
        if teamID == 100:
            blueTeamWinRates.append(winRate)
            blueTeamChampionWin.append(championWinRate)
            blueTeamChampPos.append(championPosition)
        else:
            purpleTeamWinRates.append(winRate) 
            purpleTeamChampionWin.append(championWinRate)
            purpleTeamChampPos.append(championPosition)

            
    if len(purpleTeamWinRates) + len(blueTeamWinRates) == 10:
        blueTeamWinRates, purpleTeamWinRates, blueTeamChampionWin, purpleTeamChampionWin = sortByPosition(blueTeamWinRates, purpleTeamWinRates,
                    blueTeamChampionWin, purpleTeamChampionWin, blueTeamChampPos, purpleTeamChampPos)

    data = blueTeamWinRates + purpleTeamWinRates + blueTeamChampionWin + purpleTeamChampionWin + \
            [sum(blueTeamWinRates)] + [sum(purpleTeamWinRates)] + [sum(blueTeamChampionWin)] + [sum(purpleTeamChampionWin)] + [int(D.blueTeamWin)]

    return summonerID, data


def sortByPosition(blueTeamWinRates, purpleTeamWinRates, blueTeamChampionWin, purpleTeamChampionWin, blueTeamChampPos, purpleTeamChampPos):
    """ Sorts the teams into: top lane, jungle, mid, adc, support """
    
    sortedBlueTeamWinRates = [None] * len(blueTeamWinRates)
    sortedPurpleTeamWinRates = [None] * len(purpleTeamWinRates)
    sortedBlueTeamChampionWin = [None] * len(blueTeamChampionWin)
    sortedPurpleTeamChampionWin = [None] * len(purpleTeamChampionWin)

    for x in range(len(blueTeamWinRates)):
        if blueTeamChampPos[x] == "Top Lane" and sortedBlueTeamWinRates[0] == None:
            sortedBlueTeamWinRates[0] = blueTeamWinRates[x]
            sortedBlueTeamChampionWin[0] = blueTeamChampionWin[x]
            blueTeamWinRates[x] = None

        elif blueTeamChampPos[x] == "Jungler" and sortedBlueTeamWinRates[1] == None:
            sortedBlueTeamWinRates[1] = blueTeamWinRates[x]
            sortedBlueTeamChampionWin[1] = blueTeamChampionWin[x]
            blueTeamWinRates[x] = None

        elif blueTeamChampPos[x] == "Middle Lane" and sortedBlueTeamWinRates[2] == None:
            sortedBlueTeamWinRates[2] = blueTeamWinRates[x]
            sortedBlueTeamChampionWin[2] = blueTeamChampionWin[x]
            blueTeamWinRates[x] = None
  
        elif blueTeamChampPos[x] == "AD Carry" and sortedBlueTeamWinRates[3] == None:
            sortedBlueTeamWinRates[3] = blueTeamWinRates[x]
            sortedBlueTeamChampionWin[3] = blueTeamChampionWin[x]
            blueTeamWinRates[x] = None

        elif blueTeamChampPos[x] == "Support" and sortedBlueTeamWinRates[4] == None:
            sortedBlueTeamWinRates[4] = blueTeamWinRates[x]
            sortedBlueTeamChampionWin[4] = blueTeamChampionWin[x]
            blueTeamWinRates[x] = None

    for x in range(len(blueTeamWinRates)):
        if blueTeamWinRates[x] != None:
            for y in range(len(sortedBlueTeamWinRates)):
                if sortedBlueTeamWinRates[y] == None:
                    sortedBlueTeamWinRates[y] = blueTeamWinRates[x]
                    sortedBlueTeamChampionWin[y] = blueTeamChampionWin[x]
                    blueTeamWinRates[x] = None
                    
    for x in range(len(purpleTeamWinRates)):
        if purpleTeamChampPos[x] == "Top Lane" and sortedPurpleTeamWinRates[0] == None:
            sortedPurpleTeamWinRates[0] = purpleTeamWinRates[x]
            sortedPurpleTeamChampionWin[0] = purpleTeamChampionWin[x]
            purpleTeamWinRates[x] = None

        elif purpleTeamChampPos[x] == "Jungler" and sortedPurpleTeamWinRates[1] == None:
            sortedPurpleTeamWinRates[1] = purpleTeamWinRates[x]
            sortedPurpleTeamChampionWin[1] = purpleTeamChampionWin[x]
            purpleTeamWinRates[x] = None

        elif purpleTeamChampPos[x] == "Middle Lane" and sortedPurpleTeamWinRates[2] == None:
            sortedPurpleTeamWinRates[2] = purpleTeamWinRates[x]
            sortedPurpleTeamChampionWin[2] = purpleTeamChampionWin[x]
            purpleTeamWinRates[x] = None
  
        elif purpleTeamChampPos[x] == "AD Carry" and sortedPurpleTeamWinRates[3] == None:
            sortedPurpleTeamWinRates[3] = purpleTeamWinRates[x]
            sortedPurpleTeamChampionWin[3] = purpleTeamChampionWin[x]
            purpleTeamWinRates[x] = None

        elif purpleTeamChampPos[x] == "Support" and sortedPurpleTeamWinRates[4] == None:
            sortedPurpleTeamWinRates[4] = purpleTeamWinRates[x]
            sortedPurpleTeamChampionWin[4] = purpleTeamChampionWin[x]
            purpleTeamWinRates[x] = None

    for x in range(len(purpleTeamWinRates)):
        if purpleTeamWinRates[x] != None:
            for y in range(len(sortedPurpleTeamWinRates)):
                if sortedPurpleTeamWinRates[y] == None:
                    sortedPurpleTeamWinRates[y] = purpleTeamWinRates[x]
                    sortedPurpleTeamChampionWin[y] = purpleTeamChampionWin[x]
                    purpleTeamWinRates[x] = None

    print("Data has been sorted")  
    return sortedBlueTeamWinRates, sortedPurpleTeamWinRates, sortedBlueTeamChampionWin, sortedPurpleTeamChampionWin
    

def getChampionNameFromID(championID):
        """ Get the champion name from the ID"""
        staticdata = requests.get('https://prod.api.pvp.net/api/lol/static-data/na/v1.2/champion/'+str(championID)+'?api_key=d9f79478-95ed-4def-8060-e8945b834809')
        staticdatajson = staticdata.json()
        championName = staticdatajson['name']
        return championName

def importDataFromExcel():
    book = open_workbook('championWinRate.xlsx')
    sheet1 = book.sheet_by_index(0)
    championWinRateData = {}

    for i in range(sheet1.nrows):
        cell_value_class = sheet1.cell(i,1).value
        cell_value_id = sheet1.cell(i,0).value
        championWinRateData[cell_value_id] = cell_value_class

    D.championWinRates = championWinRateData


def importChampionPositions():
    book = open_workbook('championWinRate.xlsx')
    sheet1 = book.sheet_by_index(0)
    championWinRateData = {}

    for i in range(sheet1.nrows):
        cell_value_class = sheet1.cell(i,2).value
        cell_value_id = sheet1.cell(i,0).value
        championWinRateData[cell_value_id] = cell_value_class

    D.championPosition = championWinRateData



def exportToExcel(data):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet')
    counter = 0
    for x in range(len(data) - 1):
        if len(data[x]) == 25:
            for i , e in enumerate(data[x]):
                sheet1.write(x-counter,i,e)
        else:
            counter += 1

    name = "testSheet.xls"
    book.save(name)
    book.save(TemporaryFile())

    


def getAllData():

    importDataFromExcel()
    importChampionPositions()

    datasets = 0
    totalData = []
    
    summonername = "burningarrows"
    summonerinfo = requests.get('https://prod.api.pvp.net/api/lol/na/v1.4/summoner/by-name/'+summonername+'?api_key=d9f79478-95ed-4def-8060-e8945b834809')
    summonerdata = summonerinfo.json()
    hostId = summonerdata[summonername]["id"]

    while datasets < 2000:
        print("This is dataset: ", datasets) 
        hostId, data = getDataForEveryone(hostId)
        totalData.append(data)
        datasets += 1
        

    return totalData

        
def run():
    data = getAllData()
    exportToExcel(data)
    








    


if __name__ == "__main__":
    run()

