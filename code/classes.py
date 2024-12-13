class game():
    def __init__(self, row : list, home, away, league_table : dict):
        self.date = row[0]
        self.season = row[1]
        self.home = home
        self.away = away
        #all stats are from perspective of home team
        self.gf = row[5]
        self.ga = row[6]
        self.result = row[4]
        self.home_yellows = row[7]
        self.away_yellows = row[8]
        self.home_reds = row[9]
        self.away_reds = row[10]
        self.significant = self.is_signif(league_table)
        self.odds = {
            "w" : row[11],
            "d" : row[12],
            "l" : row[13]
            }
    
    def overtake_possible(self, top, bottom):
        '''
        returns if bottom team can catch top team in the league table
        '''
        if int(top['points']) <= int(bottom['points']) + (38 - int(bottom['mp'])) * 3:
            return True
        return False

    def is_signif_helper(self, team_name, table):
        '''
        NOTE FOR PAPER: this algorithm is simplified to NOT consider matches between teams. 
        Consider the 4 team league where, with 2 matches left, the table is:
        A 5pts
        B 4pts
        C 0pts
        D 0pts
        and fixtures are:
        A vs B and D vs C
        A vs C and B vs E
        D would appear to still be in contention if they win against C and B and A loses both their games
        But A losing their games would mean B gets 3 points in that matchup.
        In reality, D is out of contention.
        Considering these edge cases makes the problem much more complicated and beyond the scope of this project
        '''
        position = table.index[table['team'] == team_name][0] + 1
        team = table.iloc[position-1]
        #might be a more efficient order to check these in but...
        #can go from 1st to 2nd (lose league title)
        if position == 1:
            second = table.iloc[1]
            if self.overtake_possible(team, second) == True:
                return True #if they cannot be passed, they have won the league and match is not significant
        #can go from top 4 to 5th place (lose UCL spot)
        if position <= 4:
            fifth = table.iloc[4]
            if self.overtake_possible(team, fifth) == True:
                return True
        #can go from 5th to 6th (lose european spot)
        if position == 5:
            sixth = table.iloc[5]
            if self.overtake_possible(team, sixth) == True:
                return True
        #can be relegated
        if position < 18:
            eighteenth = table.iloc[17]
            if self.overtake_possible(team, eighteenth) == True:
                return True
        #can escape relegation
        if position >= 18:
            seventeenth = table.iloc[16]
            if self.overtake_possible(seventeenth, team) == True:
                return True
        #can go to 4th
        fourth = table.iloc[3]
        if self.overtake_possible(fourth, team) == True:
            return True
        #can go to 1st
        first = table.iloc[0]
        if self.overtake_possible(first, team) == True:
            return True
        #can go to 5th
        fifth = table.iloc[4]
        if self.overtake_possible(fifth, team) == True:
            return True
        return False #if no if statement triggers

    def is_signif(self, league_tables : dict):
        '''
        Returns:
        H if the match is significant for only the home team
        A if the match is significant only for the away team
        N if the match is equally significant/insignificant
        '''
        if self.date not in league_tables: #too early in the season
            return 'N'
        h_sig = 0
        a_sig = 0
        #TODO: could be more accurate to use the previous day's/week's league table
        if self.is_signif_helper(self.home.getName(), league_tables[self.date]): 
            h_sig = 1
        if self.is_signif_helper(self.away.getName(), league_tables[self.date]):
            a_sig = 1
        if h_sig == a_sig:
            return 'N'
        if h_sig == 1:
            return 'H'
        if a_sig == 1:
            return 'A'

    def printInfo(self):
        '''
        mostly for debugging
        '''
        print(f'{self.date} {self.home.getName()} vs {self.away.getName()}, Final Score: {self.gf}-{self.ga}. Significant for: {self.significant}')


class team():
    def __init__(self, name : str):
        self.name = name
        self.games_list = []

    def getNumGames(self):
        return len(self.games_list)
    
    def getName(self):
        return self.name

    def getForm(self):
        '''
        returns team's goal differential across the last 5 matches
        '''
        goal_differential = 0
        for i in range(-6,-1):
            game_gd = int(self.games_list[i].gf) - int(self.games_list[i].ga)
            if self.games_list[i].home == self:
                goal_differential += game_gd
            else: #team is the away team so results needs to be reversed (in the game object they're from H team perspective)
                goal_differential -= game_gd
        return goal_differential

    def getPrevMatches(self):
        '''
        returns list of last 3 match results from oldest to newest
        ex: [W, D, D]
        '''
        results = []
        for i in range(-4,-1):
            result = self.games_list[i].result
            if result == "D":
                results.append("D")
            elif self.games_list[i].home == self:
                results.append(result)
            else: #team is the away team so results needs to be reversed (in the game object they're from H team perspective)
                if result == "W":
                    results.append("L")
                elif result == "L":
                    results.append("W")
        return results

    def getPrevMatchYellow(self):
        '''
        returns number of red cards for the team in last 5 matches
        5 chosen arbitrarily. Suspension rule is a single player getting 5 yellow cards in 19 matches
        Too much work to keep track of
        '''
        yellows = 0
        for i in range(-6,-1):
            if self.games_list[i].home == self:
                yellows += int(self.games_list[i].home_yellows)
            else:
                yellows += int(self.games_list[i].away_yellows)
        return yellows

    def getPrevMatchRed(self):
        '''
        returns number of red cards for the team in last 3 matches
        2 chosen b/c red cards mean the player is suspensed for at least 2 games
        '''
        reds = 0
        for i in range(-3,-1):
            if self.games_list[i].home == self:
                reds += int(self.games_list[i].home_reds)
            else:
                reds += int(self.games_list[i].away_reds)
        return reds

    def addGame(self, game):
        if len(self.games_list) > 5:
            self.games_list.pop(0)
            if self.games_list[-1].season != game.season:
                self.games_list = []
        self.games_list.append(game)

    def setNewSeason(self):
        self.games_list = []

    def printMatches(self):
        '''
        mostly to help with debugging
        '''
        for game_obj in self.games_list:
            game_obj.printInfo()
            