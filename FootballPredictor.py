import requests
import json
from textblob import TextBlob
import numpy as np

# Define Football-Data.org API key
football_data_api_key = "datakey"

# Define News API key
news_api_key = "news key"

import requests

def get_league_data():
    """
    Retrieves data about the Premier League from the Football-Data API.
    """
    # Replace <API_KEY> with your API key
    api_key = football_data_api_key
    
    # Build the URL for the API request
    url = "http://api.football-data.org/v2/competitions/PL/matches?status=FINISHED"
    
    # Send the API request with the API key in the headers
    response = requests.get(url, headers={"X-Auth-Token": api_key})
    
    # Raise an exception if the API request was unsuccessful
    response.raise_for_status()
    
    # Return the JSON data from the API response
    return response.json()

def get_team_id(team):
    """
    Gets the ID of a team from the Football-Data API.
    """
    # Replace <API_KEY> with your API key
    api_key = football_data_api_key
    
    # Build the URL for the API request
    url = "http://api.football-data.org/v2/teams"
    
    # Send the API request with the API key in the headers
    response = requests.get(url, headers={"X-Auth-Token": api_key})
    
    # Raise an exception if the API request was unsuccessful
    response.raise_for_status()
    
    # Get the JSON data from the API response
    data = response.json()
    
    # Find the team with the given name and return its ID
    for team_data in data["teams"]:
        if team_data["name"] == team:
            return team_data["id"]
    
    # If no team with the given name was found, raise an exception
    raise ValueError(f"No team found with name '{team}'")
def get_team_data(team):
    """
    Gets data about a team, including their league position, recent form, and
    a list of missing players.
    """
    # Replace <API_KEY> with your API key
    api_key = football_data_api_key
    
    # Get the team ID
    team_id = get_team_id(team)
    
    # Build the URL for the API request to get the league table
    url = "http://api.football-data.org/v4/competitions/PL/standings?season=2022"
    
    # Send the API request with the API key in the headers
    response = requests.get(url, headers={"X-Auth-Token": api_key})
    
    # Raise an exception if the API request was unsuccessful
    response.raise_for_status()
    
    # Get the JSON data from the API response
    league_data = response.json()
    
    # Find the team in the league table and get its position
    for row in league_data["standings"][0]["table"]:
        if row["team"]["id"] == team_id:
            position = row["position"]
            break
    
    # If the team is not found in the league table, raise an exception
    else:
        raise ValueError(f"No position found for team '{team}'")
    
    # Build the URL for the API request to get the team data
    url = f"http://api.football-data.org/v2/teams/{team_id}"
    
    # Send the API request with the API key in the headers
    response = requests.get(url, headers={"X-Auth-Token": api_key})
    
    # Raise an exception if the API request was unsuccessful
    response.raise_for_status()
    
    # Get the JSON data from the API response
    team_data = response.json()
    print(f"team_data '{team_data}'")
    # Get the recent form of the team
    form = team_data["form"]
    
    # Get the list of missing players for the team
    squad = []
    for player in team_data["squad"]:
        if player["role"] == "PLAYER" and player["status"] == "INJURED":
            squad.append({
                "name": player["name"],
                "id": player["id"]
            })
    
    # Return the team data
    return {
        "position": position,
        "form": form,
        "squad": squad
    }


# Define a function to get data about a player
def get_player_stats(player_id):
    url = f"https://api.football-data.org/v2/players/{player_id}"
    headers = {"X-Auth-Token": football_data_api_key}
    response = requests.get(url, headers=headers)
    player_data = json.loads(response.text)
    return player_data

# Define a function to get data about head-to-head matches between two teams
def get_head_to_head_data(home_team, away_team):
    url = f"https://api.football-data.org/v2/teams"
    headers = {"X-Auth-Token": football_data_api_key}
    params = {"name": f"{home_team},{away_team}"}
    response = requests.get(url, headers=headers, params=params)
    team_data = json.loads(response.text)
    if "count" in team_data and team_data["count"] == 2:
        home_team_id = team_data["teams"][0]["id"]
        away_team_id = team_data["teams"][1]["id"]
        url = f"https://api.football-data.org/v2/head2head/{home_team_id}/{away_team_id}"
        response = requests.get(url, headers=headers)
        head_to_head_data = json.loads(response.text)
        home_wins = head_to_head_data["head2head"]["homeTeamWins"]
        away_wins = head_to_head_data["head2head"]["awayTeamWins"]
        draws = head_to_head_data["head2head"]["draws"]
        return home_wins, away_wins, draws
    else:
        raise ValueError(f"No data found for teams: {home_team}, {away_team}")

# Define a function to get news articles about a query
def get_news_articles(query):
    url = "https://newsapi.org/v2/everything"
    headers = {"Authorization": f"Bearer {news_api_key}"}
    params = {
        "q": query,
        "sortBy": "relevancy",
        "pageSize": 3
    }
    response = requests.get(url, headers=headers, params=params)
    news_data = json.loads(response.text)
    articles = news_data["articles"]
    return articles

# Define a function to perform sentiment analysis on news articles
def perform_sentiment_analysis(articles):
    sentiment_scores = []
    for article in articles:
        text = article["title"] + " " + article["description"]
        blob = TextBlob(text)
        sentiment_scores.append(blob.sentiment.polarity)
    return


# Define a function to predict the outcome of a match
def predict_match(home_team, away_team):
    # Get data about the home team
    home_team_data = get_team_data(home_team)
    home_team_form = home_team_data["form"]
    home_team_league_position = home_team_data["position"]
    
    # Get data about the away team
    away_team_data = get_team_data(away_team)
    away_team_form = away_team_data["form"]
    away_team_league_position = away_team_data["position"]
    
    # Calculate missing players and their stats
    home_team_missing_players = home_team_data["squad"]
    away_team_missing_players = away_team_data["squad"]
    home_team_missing_player_stats = []
    away_team_missing_player_stats = []
    for player in home_team_missing_players:
        player_stats = get_player_stats(player["id"])
        home_team_missing_player_stats.append(player_stats)
    for player in away_team_missing_players:
        player_stats = get_player_stats(player["id"])
        away_team_missing_player_stats.append(player_stats)
    
    # Get data about head-to-head matches between the two teams
    home_wins, away_wins, draws = get_head_to_head_data(home_team, away_team)
    
    # Get sentiment analysis of news articles about the upcoming fixture
    query = f"{home_team} vs {away_team}"
    articles = get_news_articles(query)
    sentiment_scores = perform_sentiment_analysis(articles)
    
    # Create input vector for model
    input_vector = np.array([
        home_team_form,
        home_team_league_position,
        len(home_team_missing_players),
        away_team_form,
        away_team_league_position,
        len(away_team_missing_players),
        home_wins,
        away_wins,
        draws,
        np.mean(sentiment_scores)
    ])
    
    # Load and use trained model to predict match outcome
    model = pickle.load(open("model.pkl", "rb"))
    outcome = model.predict(input_vector.reshape(1, -1))
    
    return outcome

# Example usage
home_team = "Manchester United FC"
away_team = "Liverpool FC"
prediction = predict_match(home_team, away_team)
print(f"{home_team} vs {away_team}: {prediction}")

