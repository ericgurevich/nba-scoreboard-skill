from mycroft import MycroftSkill, intent_file_handler


class NbaScoreboard(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('scoreboard.nba.intent')
    def handle_scoreboard_nba(self, message):
        self.speak_dialog('scoreboard.nba')


def create_skill():
    return NbaScoreboard()

