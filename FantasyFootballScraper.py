import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np

player_name, player_team, player_position, player_bye = [], [], [], []
fantasyRankings = {'Name': player_name, 'Team': player_team, 'Position': player_position}
column_values = ['Name', 'Team', 'Position']


def scrape_results(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("tbody")
    fantasy_elements = results.find_all("tr")
    return fantasy_elements


def player_search(name, player_list):
    item_index = np.where(player_list == name)[0]
    return item_index


def name_generalizer(name):
    name = name.replace(u'.', u'')
    name = name.replace(u' Jr', u'')
    name = name.replace(u' III', u'')
    name = name.replace(u' II', u'')
    if name == "Robby Anderson":
        name = "Robbie Anderson"
    if name == "Kenneth Walker":
        name = "Ken Walker"
    if name == "Josh Palmer":
        name = "Joshua Palmer"
    return name


# FantasyPros
URL = "https://www.fantasypros.com/nfl/cheatsheets/top-half-ppr-players.php"
fantasypros_rank = [None] * 400
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("li")
x = 0
for row in results:
    rowtext = row.text.split('\n')
    for newrow in rowtext:
        newrow = newrow.replace(u'\xa0', u' ')
        newrow = newrow.split(' ')
        newrow[0] = newrow[0].replace(u'.', u'')

        if newrow[0].isdigit() and newrow[0] != '2022':
            rank = newrow[0]
            name = ' '.join(newrow[1:-2])
            position = newrow[-2].split("-")[0]
            team = newrow[-2].split("-")[1]
            name = name_generalizer(name)
            if team == "JAC":
                team = "JAX"
            player_name.append(name)
            player_team.append(team)
            player_position.append(position)
            fantasypros_rank[x] = rank
            x = x + 1

np_array = np.array(player_name)

# Fantasy Football Calculator
URL = "https://fantasyfootballcalculator.com/rankings/half-ppr"
fantasy_elements = scrape_results(URL)
fantasyfootballcalc = [None] * 400
for player in fantasy_elements:
    playertext = player.text
    playertext = playertext.split("\n")
    rank = playertext[1].split(".")[0]
    name = playertext[2]
    name = name_generalizer(name)
    team = playertext[3]
    position = playertext[4]
    ByeWeek = playertext[5]

    test_index = player_search(name, np_array)
    if ((name == player_name[test_index[0]]) & (team == player_team[test_index[0]])):
        fantasyfootballcalc[test_index[0]] = rank
    else:
        print("error!", name)

# BetIQ TeamRankings
URL = "https://betiq.teamrankings.com/fantasy-football/rankings/half-ppr/"
fantasy_elements = scrape_results(URL)
betiq = [None] * 400
for player in fantasy_elements:
    playertext = player.text
    playertext = playertext.split("\n")
    rank = playertext[1]
    playername = playertext[2]
    playername = name_generalizer(playername)
    team = playertext[3].split(" ")[1]
    position = playertext[3].split(" ")[0]
    position = re.sub(r'\d+', '', position)
    team = re.sub(r'\d+', '', team)
    if team == "JAC":
        team = "JAX"

    test_index = player_search(playername, np_array)
    try:
        if ((playername == player_name[test_index[0]]) & (team == player_team[test_index[0]])):
            betiq[test_index[0]] = rank
    except:
        player_name.append(playername)
        player_team.append(team)
        player_position.append(position)
        np_array = np.array(player_name)
        test_index = player_search(playername, np_array)
        if ((playername == player_name[test_index[0]]) & (team == player_team[test_index[0]])):
            betiq[test_index[0]] = rank

# 4for4
URL = "https://www.4for4.com/adp"
fantasy_elements = scrape_results(URL)
x = 1
UnderdogRanking = [None] * 400
CBSRanking = [None] * 400
ESPNRanking = [None] * 400
FFPCRanking = [None] * 400
BB10sRanking = [None] * 400
NFLRanking = [None] * 400
YahooRanking = [None] * 400
for player in fantasy_elements:
    td_list = player.find_all("td")
    name = td_list[1].text
    name = name_generalizer(name)
    position = td_list[3].text.split("-")[0]
    try:
        position = re.sub(r'\d+', '', position)
    except:
        print("Error!")
    try:
        team = td_list[2].text
    except:
        team = "FA"
    x = x + 1
    rankings = player.find_all("td", class_="text-center numeric-cell")
    adpCount = 1
    Underdog_Rank = ""
    CBS_Rank = ""
    ESPN_Rank = ""
    FFPC_Rank = ""
    BB10s_Rank = ""
    NFL_Rank = ""
    Yahoo_Rank = ""
    while adpCount < 8:
        adpRank = rankings[adpCount].text
        if adpRank != "-":
            if adpCount == 1:
                Underdog_Rank = adpRank
            elif adpCount == 2:
                CBS_Rank = adpRank
            elif adpCount == 3:
                ESPN_Rank = adpRank
            elif adpCount == 4:
                FFPC_Rank = adpRank
            elif adpCount == 5:
                BB10s_Rank = adpRank
            elif adpCount == 6:
                NFL_Rank = adpRank
            elif adpCount == 7:
                Yahoo_Rank = adpRank
        adpCount = adpCount + 1
    np_array = np.array(player_name)
    test_index = player_search(name, np_array)
    try:
        if ((name == player_name[test_index[0]]) & (team == player_team[test_index[0]])):
            UnderdogRanking[test_index[0]] = Underdog_Rank
            CBSRanking[test_index[0]] = CBS_Rank
            ESPNRanking[test_index[0]] = ESPN_Rank
            FFPCRanking[test_index[0]] = FFPC_Rank
            BB10sRanking[test_index[0]] = BB10s_Rank
            NFLRanking[test_index[0]] = NFL_Rank
            YahooRanking[test_index[0]] = Yahoo_Rank
    except:
        player_name.append(name)
        player_team.append(team)
        player_position.append(position)
        np_array = np.array(player_name)
        test_index = player_search(name, np_array)
        if ((name == player_name[test_index[0]]) & (team == player_team[test_index[0]])):
            UnderdogRanking[test_index[0]] = Underdog_Rank
            CBSRanking[test_index[0]] = CBS_Rank
            ESPNRanking[test_index[0]] = ESPN_Rank
            FFPCRanking[test_index[0]] = FFPC_Rank
            BB10sRanking[test_index[0]] = BB10s_Rank
            NFLRanking[test_index[0]] = NFL_Rank
            YahooRanking[test_index[0]] = Yahoo_Rank
        else:
            print(name, player_name[test_index[0]], team, player_team[test_index[0]], "Error!")

if len(player_name) != len(player_team):
    print("Big error")

if len(player_name) != len(player_position):
    print("Position Error")

if len(player_name) != len(fantasyfootballcalc):
    fantasyfootballcalc = fantasyfootballcalc[: len(player_name)]

if len(player_name) != len(fantasypros_rank):
    fantasypros_rank = fantasypros_rank[: len(player_name)]

if len(player_name) != len(betiq):
    betiq = betiq[: len(player_name)]

if len(player_name) != len(CBSRanking):
    CBSRanking = CBSRanking[: len(player_name)]

if len(player_name) != len(ESPNRanking):
    ESPNRanking = ESPNRanking[: len(player_name)]

if len(player_name) != len(FFPCRanking):
    FFPCRanking = FFPCRanking[: len(player_name)]

if len(player_name) != len(BB10sRanking):
    BB10sRanking = BB10sRanking[: len(player_name)]

if len(player_name) != len(NFLRanking):
    NFLRanking = NFLRanking[: len(player_name)]

if len(player_name) != len(UnderdogRanking):
    UnderdogRanking = UnderdogRanking[: len(player_name)]

if len(player_name) != len(YahooRanking):
    YahooRanking = YahooRanking[: len(player_name)]

fantasyRankings["FantasyFootballCalc"] = fantasyfootballcalc
fantasyRankings["BetIQ"] = betiq
fantasyRankings["FantasyPros"] = fantasypros_rank
fantasyRankings["CBSRanking"] = CBSRanking
fantasyRankings["ESPNRanking"] = ESPNRanking
fantasyRankings["FFPCRanking"] = FFPCRanking
fantasyRankings["BB10sRanking"] = BB10sRanking
fantasyRankings["NFLRanking"] = NFLRanking
fantasyRankings["UnderdogRanking"] = UnderdogRanking
fantasyRankings["YahooRanking"] = YahooRanking

df = pd.DataFrame(fantasyRankings)
df.to_csv('Fantasy_Sheet.csv')
# print(df)
