class Fire:
	def __init__(self,x,y,img1,img2):
		self.x = x
		self.y = y
		self.img = img1
		self.img2 = img2
		self.alternate = True
		self.switchTicks = 0

	def render(self,surface):
		surface.blit(self.img if self.alternate else self.img2,[self.x,self.y])
		if(self.switchTicks >= 5):
			self.alternate = not self.alternate
			self.switchTicks = 0
		else:
			self.switchTicks += 1

	def getCenter(self):
		return [self.x + self.img.get_size()[0]/2,self.y + self.img.get_size()[1]/2]