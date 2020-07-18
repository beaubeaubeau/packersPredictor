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


response = getData(280908009)
soup = parse(response)
title = soup.title.text

table = getTable(soup)
table_data = table.tbody.find_all("tr")

# Grabs data from table in a nice string format
for i in range(len(table_data)): #len(table_data)
    # Each row is a football statistic
    row = table_data[i].find_all("td")
    # Values are organized as [Category, Visitor Stat, Home Stat]
    for value in row:
        v = str(value.text).strip()
        print(v)
