from mycroft import MycroftSkill, intent_file_handler
import requests
from datetime import datetime, timedelta
import json

API_key = '204720b278msh1c690d8a62476dcp11caa8jsn506e42ddb682'
API_url = 'https://api-nba-v1.p.rapidapi.com/games/teamId/'
header = {
    "x-rapidapi-host": "api-nba-v1.p.rapidapi.com",
    "x-rapidapi-key": "204720b278msh1c690d8a62476dcp11caa8jsn506e42ddb682"
}

# get today's date
# date = datetime.now()
# d = date.strftime('%Y-%m-%d')


def search_game(teamId):
    r = requests.get(API_url + str(teamId), headers=header)
    json_data = r.json()
    results = int(json_data['api']['results'])
    v_team = str(json_data['api']['games'][results - 1]['vTeam']['fullName'])
    v_score = str(json_data['api']['games'][results - 1]
                  ['vTeam']['score']['points'])
    h_team = str(json_data['api']['games'][results - 1]['hTeam']['fullName'])
    h_score = str(json_data['api']['games'][results - 1]
                  ['hTeam']['score']['points'])

    return v_team, v_score, h_team, h_score


class NbaScoreboard(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.register_entity_file('team.entity')
        
        # match team names to api team IDs, obtained from get_teams.py
        self.teamIDs = {'Hawks': 1, 'Celtics': 2, 'Bullets': 3, 'Nets': 4, 'Hornets': 5, 'Bulls': 6, 'Cavaliers': 7, 'Mavericks': 8, 'Nuggets': 9, 'Pistons': 10, 'Warriors': 11, 'Long-Lions': 12, 'Maccabi Haifa': 13, 'Rockets': 14, 'Pacers': 15, 'Clippers': 16, 'Lakers': 17, 'United': 18, 'Grizzlies': 19, 'Heat': 20, 'Bucks': 21, 'Timberwolves': 22, 'Pelicans': 23, 'Knicks': 24, 'Thunder': 25, 'Magic': 26, '76ers': 27, 'Suns': 28, 'Trail Blazers': 29, 'Kings': 33, 'Spurs': 31, 'Sharks': 32, 'Team Giannis': 34, 'Team LeBron': 35, 'Away': 36, 'Home':
                        37, 'Raptors': 38, 'USA': 39, 'Jazz': 40, 'Wizards': 41, 'World': 42, 'Paschoalotto/Bauru': 83, 'Fenerbahce Sports Club': 84, 'Olimpia Milano': 85, 'Real Madrid': 86, 'Flamengo': 87, 'FC Barcelona': 88, 'San Lorenzo': 89, '36ers': 90, 'Ducks': 91, 'Breakers': 92, 'Wildcats': 93, 'Franca': 99}

        # because our city's team has a weird name
        self.teamIDs['Sixers'] = 27
        self.teamIDs['Seventy Sixers'] = 27

    @intent_file_handler('scoreboard.nba.intent')
    def handle_scoreboard_nba(self, message):
        team = str(message.data.get('team'))

        if team is not None and team in self.teamIDs:
            teamId = int(self.teamIDs[team])

            # fill in score from api
            v_team, v_score, h_team, h_score = search_game(teamId)

            # loading score variables into dialog and speaking from that file
            self.speak_dialog('Score', {
                'team1': v_team,
                'score1': v_score,
                'team2': h_team,
                'score2': h_score})
        else:
            self.speak_dialog('NotFound')


def create_skill():
    return NbaScoreboard()
