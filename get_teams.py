import requests
import json

API_key = '204720b278msh1c690d8a62476dcp11caa8jsn506e42ddb682'
API_url = 'https://api-nba-v1.p.rapidapi.com/teams/league/standard'
header = {
    "x-rapidapi-host": "api-nba-v1.p.rapidapi.com",
    "x-rapidapi-key": "204720b278msh1c690d8a62476dcp11caa8jsn506e42ddb682"
}

def get_all_teams():
    r = requests.get(API_url, headers=header)
    json_data = r.json()

    results = int(json_data['api']['results'])
    
    teamIDs = {}

    for i in range(results):
        teamIDs[json_data['api']['teams'][i]['nickname']] = int(json_data['api']['teams'][i]['teamId'])

    print(teamIDs)
    
get_all_teams()