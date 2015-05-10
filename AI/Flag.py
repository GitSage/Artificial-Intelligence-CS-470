class Flag:
    def __init__(self, team_color, possessing_team_color, x, y):
        self.team_color = team_color
        self.possessing_team_color = possessing_team_color
        self.x = x
        self.y = y

    def __str__(self):
        return "Flag team color: %s, possessing_team_color: %s, x: %f, y:  %f" %(self.team_color,
                                                                                 self.possessing_team_color, self.x,
                                                                                 self.y)