import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv

def getData(gameID:int):
    """
    Gets data about specified NFL game.

    @param gameID: int
        The ESPN game ID for the NFL game.
    @return response: requests.models.Response
        Returns HTML response i.e. Response [200] means success
    """
    url = "https://www.espn.com/nfl/matchup?gameId="+str(gameID)
    response = requests.get(url)
    # Response of 200 means data was successfully accessed
    return response

def parse(response):
    """
    Parse HTML with Beautiful Soup, turns into Beautiful Soup data structure

    @param response
        The HTML reponse from accessing the data.
    @return soup
        Beautiful Soup data structure of the website's HTML.
    """
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def isPackersGame(title:str)->bool:
    """
    Returns true if the game is a Packers game.

    @param title: str
        Title of the football game (i.e. team vs team)
    @return isPacker: bool
        Returns True if this is a Packer's game.
        Returns False otherwise.
    """
    if "Packers" in title:
        return True
    return False

def isHome(title: str)->bool:
    """
    Title must contain "Packers"
    Returns true if the Packers are home.

    @param title: str
        Title of the football game (i.e. team vs team)
    @return isPacker: bool
        Returns True if this is a Packer's game.
        Returns False otherwise.
    """
    assert "Packers" in title
    if title.find("Packers")==0:
        return False
    return True

def getTable(soup):
    """
    Returns the table of game statistics.

    @param soup
        Beautiful Soup data structure of the website's HTML.
    @return table
        Beautiful Soup data structure of the football game's statistics.
    """
    return soup.find("table", attrs={"class": "mod-data"})

def getVariables(table)->list:
    """
    Given data about the game, return a list of the relevant variables or features
    found in the table.

    @param table
        Beautiful Soup data structure of the football game's statistics.
    @return variables: list
        Returns list of relevant variables to track in the feature space.
    """
    tableData = table.tbody.find_all("tr")
    variables = []
    # Add variables to feature space
    for i in range(len(tableData)):
        # Each row is a football statistic
        row = tableData[i].find_all("td")
        # Values are organized as [Football Category, Visitor Stat, Home Stat]
        var = str(row[0].text).strip() #converts to string and removes whitespace
        # Features/ variables to omit
        if var== "Defensive / Special Teams TDs" or var == "Yards per Play" \
            or var == "Yards per pass" or var == "Yards per rush" or var == "Turnovers"\
            or var == "Passing 1st downs" or var == "Rushing 1st downs" or\
            var == "1st downs from penalties" or (var == "Interceptions thrown"\
            and variables[-1]=="Pass attempts"):
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
            variables.append("Number of red zone attempts")
        elif var == "Penalties":
            variables.append("Number of penalties")
            variables.append("Penalty yards")
        elif var == "Passing" or var=="Rushing":
            variables.append(var+" yards")
        else:
            variables.append(var)
    # Now add opponents statistics
    size = len(variables)
    for i in range(size):
        opp = "Opp. "+ variables[i]
        variables.append(opp)
    variables.append("Home game") #was this a Packers home game or not
    return variables


response = getData(280908009)
soup = parse(response)
title = soup.title.text

table = getTable(soup)
columns = getVariables(table)
print(len(columns))
tableData = table.tbody.find_all("tr")

# Grabs data from table in a nice string format
for i in range(len(tableData)): #len(tableData)
    # Each row is a football statistic
    row = tableData[i].find_all("td")
    # Values are organized as [Category, Visitor Stat, Home Stat]
    for value in row:
        v = str(value.text).strip()
        print(v)
