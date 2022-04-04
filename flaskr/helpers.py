import os
import requests
import urllib.parse
import json

from flask import redirect, render_template, request, session
from functools import wraps

def error_message(message, code=400):
    return render_template("error.html", message=message), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def find_game(name):
    """Find a game in RAWG database when specified"""
    try:
 
        # Authentication and api request for igdb data
        client_id = os.environ.get("CLIENT_ID")
        client_secrect = os.environ.get("CLIENT_SECRET")
        url_2 = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secrect}&grant_type=client_credentials"
        auth = requests.post(url_2)
        access_token = auth.json()['access_token']

        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {access_token}"
        }

        name = urllib.parse.quote_plus(name)
        data = f"search \"{name}\"; fields name, slug, cover.url, screenshots.url, release_dates.y, genres.name; limit 500;"
        r = requests.post("https://api.igdb.com/v4/games/", data=data , headers=headers)        

    
    except requests.RequestException:
        return None
    
    #try:
        #return a dict of games
    games_list = []
    for game in r.json():
        try:
            cover = game['cover']['url'].replace("t_thumb", "t_cover_big")
            title = game['name']
            genre = game['genres'][0]['name']
            release_date = game['release_dates'][0]['y']
            slug = game['slug']
        
        except (KeyError, TypeError, ValueError):
            continue


        game_list = {
            'cover': cover,
            'title': title,
            'genre': genre,
            'release_date': release_date,
            'slug': slug
        }

        games_list.append(game_list)
     
        
    return games_list

def game_details(name):
    
    try:
 
        # Authentication and api request for igdb data
        client_id = os.environ.get("CLIENT_ID")
        client_secrect = os.environ.get("CLIENT_SECRET")
        url_2 = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secrect}&grant_type=client_credentials"
        auth = requests.post(url_2)
        access_token = auth.json()['access_token']

        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {access_token}"
        }

        #name = urllib.parse.quote_plus(name)
        # Create dictionary to store all the data needed for a game's description page
        data = f"fields name, screenshots.url, cover.url, genres.name, websites.url, involved_companies.company.name, release_dates.human, \
                slug, platforms.name, similar_games.name, similar_games.cover.url, videos.video_id, summary; where slug = \"{name}\";"
        r = requests.post("https://api.igdb.com/v4/games/", data=data , headers=headers)       

        return r.json() 

    
    except requests.RequestException:
        return None

def find_prices(slug):
    """Uses the IsThereAnyDeal API to find prices for games across various sites"""
    
    api_key = os.environ.get("API_KEY")
    price_client_id = os.environ.get("PRICE_CLIENT_ID")
    price_client_secret = os.environ.get("PRICE_CLIENT_SECRET")

    headers = {
        "Client ID": price_client_id,
        "Client Secret": price_client_secret
    }

    url = f"https://api.isthereanydeal.com/v01/game/prices/?key={api_key}&plains={slug}"
    r = requests.get(url, headers=headers)

    return r.json()

def int_to_roman(number):
    """Converts an integer to a roman numeral to match plain data from ITAD api"""
    """Function provided by Aristide on stackoverflow"""

    ROMAN =[
        (9, "ix"),
        (5, "v"),
        (4, "iv"),
        (1, "i"),
    ]

    result = ""

    for (arabic, roman) in ROMAN:
        (factor, number) = divmod(number, arabic)
        result += roman * factor
    return result      

         
        
    