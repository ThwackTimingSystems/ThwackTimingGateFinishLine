import copy

class Leaderboard:
    def __init__(self):
        self.leaderboard = []
        

    def addTime(self, time):
        self.leaderboard.append(time)

    def getLeaderboard(self):
        leaderboard = copy.deepcopy(self.leaderboard)
        sortedList = []
        while len(leaderboard)>0:
            index = 0
            maxTime = 0
            for i in range(len(leaderboard)):
                if leaderboard[i]>maxTime:
                    maxTime = leaderboard[i]
                    index = i
                    
            sortedList.append((index, maxTime))
            leaderboard.pop(index)
        
        return sortedList

    def getRacersTime(self, index):
        return self.leaderboard[index]