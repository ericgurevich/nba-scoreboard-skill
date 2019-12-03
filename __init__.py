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
    
    i = results - 1

    # iterate through results backwards until get to most recent non-zero game
    while True:
        v_score = str(json_data['api']['games'][i]
                      ['vTeam']['score']['points'])
        h_score = str(json_data['api']['games'][i]
                      ['hTeam']['score']['points'])

        if v_score != '' or h_score != '':
            if v_score != '0' or h_score != '0':
                break

        i -= 1

    v_team = str(json_data['api']['games'][i]['vTeam']['fullName'])
    
    h_team = str(json_data['api']['games'][i]['hTeam']['fullName'])
    
    return v_team, v_score, h_team, h_score


class NbaScoreboard(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.register_entity_file('team.entity')

        # match team names to api team IDs, obtained from get_teams.py
        self.teamIDs = {'hawks': 1, 'celtics': 2, 'bullets': 3, 'nets': 4, 'hornets': 5, 'bulls': 6, 'cavaliers': 7, 'mavericks': 8, 'nuggets': 9, 'pistons': 10, 'warriors': 11, 'long-lions': 12, 'maccabi haifa': 13, 'rockets': 14, 'pacers': 15, 'clippers': 16, 'lakers': 17, 'united': 18, 'grizzlies': 19, 'heat': 20, 'bucks': 21, 'timberwolves': 22, 'pelicans': 23, 'knicks': 24, 'thunder': 25, 'magic': 26, '76ers': 27, 'suns': 28, 'trail blazers': 29, 'kings': 33, 'spurs': 31, 'sharks': 32, 'team giannis': 34, 'team lebron': 35, 'away': 36, 'home':
                        37, 'raptors': 38, 'usa': 39, 'jazz': 40, 'wizards': 41, 'world': 42, 'paschoalotto/bauru': 83, 'fenerbahce sports club': 84, 'olimpia milano': 85, 'real madrid': 86, 'flamengo': 87, 'fc barcelona': 88, 'san lorenzo': 89, '36ers': 90, 'ducks': 91, 'breakers': 92, 'wildcats': 93, 'franca': 99}

        # because our city's team has a weird name
        self.teamIDs['sixers'] = 27
        self.teamIDs['seventy sixers'] = 27

	#to offer flexible parsing
	self.teamIDs['atlanta hawks'] = 1
	self.teamIDs['boston celtics'] = 2
	self.teamIDs['brooklyn nets'] = 4
	self.teamIDs['charlotte hornets'] = 5
	self.teamIDs['chicago bulls'] = 6
	self.teamIDs['cleveland cavaliers'] = 7
	self.teamIDs['dallas mavericks'] = 8
	self.teamIDs['denver nuggets'] = 9
	self.teamIDs['detroit pistons'] = 10
	self.teamIDs['golden state warriors'] = 11
	self.teamIDs['houston rockets'] = 14
	self.teamIDs['indiana pacers'] = 15
	self.teamIDs['los angeles clippers'] = 16
	self.teamIDs['los angeles lakers'] = 17
	self.teamIDs['memphis grizzlies'] = 19
	self.teamIDs['miami heat'] = 20
	self.teamIDs['milwaukee bucks'] = 21
	self.teamIDs['minnesota timberwolves'] = 22
	self.teamIDs['new orleans pelicans'] = 23
	self.teamIDs['new york knicks'] = 24
	self.teamIDs['oklahoma city thunder'] = 25
	self.teamIDs['orlando magic'] = 26
	self.teamIDs['Philadelphia seventy-sixers'] = 27
	self.teamIDs['phoenix suns'] = 28
	self.teamIDs['portland trail blazers'] = 29
	self.teamIDs['sacremento kings'] = 30
	self.teamIDs['san antonio spurs'] = 31
	self.teamIDs['torronto raptors'] = 38
	self.teamIDs['utah jazz'] = 40
	self.teamIDs['washington wizards'] = 41

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
