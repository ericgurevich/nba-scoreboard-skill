from mycroft import MycroftSkill, intent_file_handler
import requests
from datetime import datetime, timedelta
import json

API_key = '204720b278msh1c690d8a62476dcp11caa8jsn506e42ddb682'
API_url = 'https://api-nba-v1.p.rapidapi.com/games/date/'
header = {
	"x-rapidapi-host": "api-nba-v1.p.rapidapi.com",
	"x-rapidapi-key": "204720b278msh1c690d8a62476dcp11caa8jsn506e42ddb682"
}

#get today's date
date = datetime.now()
d = date.strftime('%Y-%m-%d')

def search_game(team):
    r = requests.get(API_url + '2019-11-30', headers=header)
    json_data = r.json()
    j = 0
    #finding the specific match
    for x in range(len(json_data['api']['games'])):
	    if team in json_data['api']['games'][j]['vTeam']['nickName'] or team in json_data['api']['games'][j]['hTeam']['nickName']:
                return json_data['api']['games'][j]['vTeam']['nickName'], json_data['api']['games'][j]['vTeam']['score']['points'], json_data['api']['games'][j]['hTeam']['nickName'], json_data['api']['games'][j]['hTeam']['score']['points']
	    j = j + 1
    return '', 0, '', 0

class NbaScoreboard(MycroftSkill):
    teamIDs = None

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.register_entity_file('team.entity')

        #match team names to api team IDs
        teamIDs = {
                'sixers': 1610612755,
                'seventy sixers': 1610612755,
		'lakers': 1610612747,
		'bulls':1610612741,
		'chicago bulls':1610612741,
		'celtics':1610612738,
		'rockets':1610612745,
		'mavericks':1610612742,
		'hawks':1610612737,
		'nets':1610612751,
		'hornets':1610612766,
		'cavaliers':1610612739,
		'nuggets':1610612742,
		'pistons':1610612765,
		'warriors':1610612744,
		'pacers':1610612754,
		'clippers':1610612746,
		'grizzlies':1610612763,
		'heat':1610612748,
		'bucks':1610612749,
		'timberwolves':1610612750,
		'pelicans':1610612740,
		'knicks':1610612752,
		'thunder':1610612760,
		'magic':1610612753,
		'suns':1610612756,
		'blazers':1610612757,
		'kings':1610612758,
		'spurs':1610612759,
		'raptors':1610612751,
		'jazz':1610612762,
		'wizards':1610612764
        }

    @intent_file_handler('scoreboard.nba.intent')
    def handle_scoreboard_nba(self, message):
        team = message.data.get('team')

        #fill in score from api
        v_team, v_score, h_team, h_score = search_game(team)

        if team is not None or v_score is not 0:
            #loading score variables into dialog and speaking from that file
            self.speak_dialog('Score', {
                'team1' : v_team,
                'score1': v_score,
                'team2' : h_team,
                'score2': h_score})
        else:
            self.speak_dialog('NotFound')

def create_skill():
    return NbaScoreboard()

