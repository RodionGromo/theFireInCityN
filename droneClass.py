class drone:
	def __init__(self,x,y,imgSeq):
		self.x = x
		self.y = y
		self.imgSeq = imgSeq
		self.seqN = 0
		self.maxSeq = len(self.imgSeq)-1

	def render(self,surface):
		surface.blit(self.imgSeq[self.seqN],[self.x,self.y])
		if(self.seqN + 1 > self.maxSeq):
			self.seqN = 0
		else:
			self.seqN += 1

	def getCenter(self):
		return [self.x + self.imgSeq[0].get_size()[0]/2, self.y + self.imgSeq[0].get_size()[1]/2]