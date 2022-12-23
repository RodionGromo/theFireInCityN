class AI:
	def __init__(self):
		self.target = None
		self.lockTime = 0
		pass

	def doMovement(self,x,y):
		movement = [0,0]
		if(self.target != None):
			tgtPos = self.target.getCenter()
			if(tgtPos[0] < x):
				movement[0] = -1
			if(tgtPos[0] > x):
				movement[0] = 1
			if(tgtPos[1] > y):
				movement[1] = -1
			if(tgtPos[1] < y):
				movement[1] = 1
		return movement

	def selectTgt(self,fires,droneWater,x,y):
		for fire in fires:
			if(self.target == None):
				self.target = fire
			else:
				if(cDL(fire.getCenter(),[x,y]) < cDL(self.target.getCenter(),[x,y]) and self.lockTime == 0):
					self.target = fire
					self.lockTime = 50
				elif(self.lockTime > 0):
					self.lockTime -= 1;


	@staticmethod
	def countDistance(x1,y1,x2,y2):
		return math.sqrt((x2-x1)**2 + (y2-y1)**2)

	@staticmethod
	def cDL(pos1,pos2):
		return countDistance(pos1[0],pos1[1],pos2[0],pos2[1])