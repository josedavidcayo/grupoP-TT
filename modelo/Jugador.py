class Jugador:
    def __init__(self):
        self._id = None
        self._nickName = None
        self._playedTime = None
        self._score = None
        self._difficulty = None 

    def getId(self):
        return self._id
    
    def getNickName(self):
        return self._nickName
    
    def getPlayedTime(self):
        return self._playedTime
    
    def getScore(self):
        return self._score

    def getDifficulty(self):
        return self._difficulty
    
    
    def setId(self, id):
        self._id = id
    
    def setNickName(self, nickName):
        self._nickName = nickName
    
    def setPlayedTime(self, playedTime):
        self._playedTime = playedTime
    
    def setScore(self, score):
        self._score = score
    
    def setDifficulty(self, difficulty):
        self._difficulty = difficulty
    
    




    