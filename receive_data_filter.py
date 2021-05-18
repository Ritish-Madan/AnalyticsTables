class MatchFilter:
    def __init__(self,
                 data,
                 match_no,
                 main_player,
                 right_shot=None,
                 other_player=None,
                 shot=2,
                 rec='Y'):

        self.PrimaryData = data
        self.match_no = match_no
        self.main_player = main_player
        self.right_shot = right_shot
        self.other_player = other_player
        self.shot = shot
        self.rec = rec

    def normal(self):
        match = self.PrimaryData['Match_No'] == self.match_no
        service = self.PrimaryData['RECEIVE'] == self.rec
        main_played = self.PrimaryData['Played_by'] == self.main_player
        shot = self.PrimaryData['Shot_no'] == self.shot
        required = self.PrimaryData[match & service & main_played & shot]
        return required

    def rshot(self):
        norm = self.normal()
        right = norm['Placement'].str[-1] == self.right_shot
        right_condition = norm[right]
        return right_condition




class MatchWon:
    def __init__(self,
                 data,
                 match_no,
                 winning_main,
                 winning_other=None,
                 left_shot=None,
                 left_shot2=None):
        self.PrimaryData = data
        self.match_no = match_no
        self.winning_main = winning_main
        self.winning_other = winning_other
        self.left_shot = left_shot
        self.left_shot2 = left_shot2

    def normal(self):
        match = self.PrimaryData['Match_No'] == self.match_no
        main_win = self.PrimaryData['WON_BY'] == self.winning_main
        win_data = self.PrimaryData[match & main_win]
        return win_data
    def bothWin(self):
        match = self.PrimaryData['Match_No'] == self.match_no
        main_win = self.PrimaryData['WON_BY'] == self.winning_main
        other_win = self.PrimaryData['WON_BY'] == self.winning_other
        bothWin_data = self.PrimaryData[match & (main_win | other_win)]
        return bothWin_data
    def leftShot(self):
        norm = self.normal()
        left_two_shots = norm['Shot'].str[:2] == self.left_shot
        leftFilter = norm[left_two_shots]
        return leftFilter
    def bothWinLeft(self):
        bothData = self.bothWin()
        leftCondition = bothData['Shot'].str[:2] == self.left_shot
        leftBoth = bothData[leftCondition]
        return  leftBoth
    def leftOtherShot(self):
        norm = self.normal()
        left_other_shots1 = norm['Shot'].str[:2] != self.left_shot
        left_other_shots2 = norm['Shot'].str[:2] != self.left_shot2
        otherLeftFilter = norm[(left_other_shots1 & left_other_shots2)]
        return otherLeftFilter
    def bothWinleftOther(self):
        bothData = self.bothWin()
        left_other_shots1 = bothData['Shot'].str[:2] != self.left_shot
        left_other_shots2 = bothData['Shot'].str[:2] != self.left_shot2
        leftBoth = bothData[(left_other_shots1 & left_other_shots2)]
        return leftBoth






