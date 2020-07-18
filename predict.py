import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv

def pullData(gameID:int):
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

response = pullData(280908009)
html = parse(response)
