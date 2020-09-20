import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv

# TODO: WRITE METHOD TO SEE WIN/ LOSS MARGIN
# TODO: TIME OF POSSESION FROM STRING TO SECONDS

IGNORED_VARS = {"Defensive / Special Teams TDs","Yards per Play","Yards per pass", \
"Yards per rush","Turnovers","Passing 1st downs","Rushing 1st downs", \
"1st downs from penalties","Total Yards"}

"""
Gets data about specified NFL game from the web.

@param gameID: int
    The ESPN game ID for the NFL game.
@return requests.models.Response
    Returns HTML response i.e. Response [200] means success
"""
def getWebData(gameID):
    url = "https://www.espn.com/nfl/matchup?gameId="+str(gameID)
    response = requests.get(url)
    # Response of 200 means data was successfully accessed
    return response

"""
Parse HTML with Beautiful Soup, turns into Beautiful Soup data structure

@param response
    The HTML reponse from accessing the data.
@return soup
    Beautiful Soup data structure of the website's HTML.
"""
def parse(response):
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

"""
Returns true if the game is a Packers game.

@param title: str
    Title of the football game (i.e. team vs team)
@return bool
    Returns True if this is a Packer's game.
    Returns False otherwise.
"""
def isPackersGame(title):
    if "Packers" in title:
        return True
    return False

"""
Title must contain "Packers"
Returns true if the Packers are home.

@param title: str
    Title of the football game (i.e. team vs team)
@return bool
    Returns True if this is a Packer's home game.
    Returns False if away.
"""
def isHome(title):
    assert "Packers" in title
    if title.find("Packers")==0:
        return False
    return True

"""
Returns the table of game statistics.

@param soup
    Beautiful Soup data structure of the website's HTML.
@return table
    Beautiful Soup data structure of the football game's statistics.
"""
def getTable(soup):
    return soup.find("table", attrs={"class": "mod-data"})


"""
Given data about the game, return a list of the relevant variables or features
found in the table.

@param table
    Beautiful Soup data structure of the football game's statistics.
@return list
    Returns list of relevant variables to track in the feature space.
"""
def getVariables(table):
    tableData = table.tbody.find_all("tr")
    variables = []
    # Add variables to feature space
    for i in range(len(tableData)):
        # Each row is a football statistic
        row = tableData[i].find_all("td")
        # Values are organized as [Football Category, Visitor Stat, Home Stat]
        var = str(row[0].text).strip() #converts to string and removes whitespace
        # Features/ variables to omit
        if var in IGNORED_VARS or (var == "Interceptions thrown" and variables[-1]=="Pass attempts"):
            continue
        elif var == "3rd down efficiency":
            variables.append("3rd down completions")
            variables.append("3rd down attempts")
        elif var == "4th down efficiency":
            variables.append("4th down completions")
            variables.append("4th down attempts")
        elif var == "Comp-Att":
            variables.append("Pass completions")
            variables.append("Pass attempts")
        elif var == "Sacks-Yards Lost":
            variables.append("Number of sacks")
            variables.append("Yards lost to sacks")
        elif var == "Red Zone (Made-Att)":
            variables.append("Red zone attempts")
        elif var == "Penalties":
            variables.append("Number of penalties")
            variables.append("Penalty yards")
        elif var == "Passing" or var=="Rushing":
            variables.append(var+" yards")
        else:
            variables.append(var)
    # Now add opponent's statistics
    size = len(variables)
    for i in range(size):
        opp = "Opp. "+ variables[i]
        variables.append(opp)
    variables.append("Home game") #was this a Packers home game or not
    return variables

def getGameData(tableData, title, numVariables):
    """"
    find out if packers are home or away
        home means that second value is packers val
        visitor means that first value is packers val
    place packer data in the appropriate place (front half of variables)
    place visitor data in the back half
    if the variable is in the feature space or if the variable
    is 3rd down efficiency, 4th down efficiency, Comp-Att
    Sacks-Yards Lost, Red Zone (Made-Att), Penalties, Passing, Rushing
    """
    # List to hold the game data
    rowOfDataFromGame = [-1]*numVariables
    # Indices for the teams' game data
    packerIndex = 0
    oppIndex = numVariables//2
    # Where data is located in the web scraped table
    packerColInTable = 0
    otherColInTable = 1
    # Swap indices if the Packers are home
    if isHome(title):
        packerColInTable = 1
        otherColInTable = 0
    # Set of varialbes that need to be split into two sections
    twoPartVars = {"3rd down efficiency","4th down efficiency","Comp-Att", \
    "Sacks-Yards Lost","Red Zone (Made-Att)","Penalties"}
    # Grabs game data from the web table
    for i in range(len(tableData)):
        # Each row is a football statistic.
        row = tableData[i].find_all("td")
        stats = getStatsForCategory(row)
        # Only consider non-ignored categories.
        category = stats[0]
        if category not in IGNORED_VARS:
            # Stat for one category for the two teams
            packerStat = stats[packerColInTable]
            otherStat = stats[otherColInTable]
            # Category is a two part category
            if category in twoPartVars:
                if category=="Red Zone (Made-Att)":
                    # Only add the attempts when splitting into two parts
                    # Convert to int
                    pass
                else:
                    # Add both parts of the variable and increment indices
                    # when splitting into two parts.
                    # Convert to int
                    pass
            # Category is a simple one part category
            else:
                # Convert to int
                # Then add to data for game
                pass
            # Increment both indices for data
    return rowOfDataFromGame

"""
Returns statistics for a game category.

@param webTableRow
    Row from the data table scraped from the web.
@returns list
    Lists stats for a given category as [Category, Visitor Stat, Home Stat]
    where each element in the list is a string.
"""
def getStatsForCategory(webTableRow):
    # Values are organized as [Category, Visitor Stat, Home Stat]
    stats=[]
    for value in webTableRow:
        stats.append(str(value.text).strip())
    return stats

"""
Returns the two parts of a two part variable .

@param twoPartVar: string
    Two part variable separated by a hypen (-)
@returns list
    Returns list with two string elements in it, containing the two
    parts data in the variable.
"""
def splitTwoPartVariable(twoPartVar):
    return  twoPartVar.split("-")



# Grab raw HTML data about game from the web
response = getWebData(280908009)
soup = parse(response)
table = getTable(soup)
title = soup.title.text
# Get relevant variables for feature space
columns = getVariables(table)
# Relevant football data, but still with HTML tags
tableData = table.tbody.find_all("tr")
#print(tableData)
