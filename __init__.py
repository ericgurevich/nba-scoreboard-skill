from mycroft import MycroftSkill, intent_file_handler


class NbaScoreboard(MycroftSkill):
    teamIDs = None

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.register_entity_file('team.entity')

        #match team names to api team IDs
        teamIDs = {
                'sixers': 0,
                'seventy sixers': 0
        }

    @intent_file_handler('scoreboard.nba.intent')
    def handle_scoreboard_nba(self, message):
        team = message.data.get('team')

        #fill in score from api
        score = 50
        
        if team is not None and team in teamIDs:
            #loading score variables into dialog and speaking from that file
            self.speak_dialog('Score', {
                'team': team,
                'score1': score,
                'score2': score})
        else:
            self.speak_dialog('NotFound')


def create_skill():
    return NbaScoreboard()

