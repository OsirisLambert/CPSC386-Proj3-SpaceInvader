
class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.play_again = True
        self.game_over = False
        self.high_score_list = [0 for i in range(10)]
        self.pick_high_score()
        self.score = 0

    def pick_high_score(self):

        file = open("highscore.txt", "r")
        string = ''
        temp_score = 0
        sco = []
        while True:
            ch = file.read(1)
            if not ch:
                file.close()
                break
            else:
                if ch != ';':
                    string += ch
                if ch == ';':
                    temp_score = int(string)
                    string = ''
                    sco.append(temp_score)
                    temp_score = 0

                sco.sort(reverse=True)

                for x in range(0, len(sco)):
                    if x < 10:
                        self.high_score_list[x] = sco[x]

        self.high_score = self.high_score_list[0]

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

