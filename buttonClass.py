import pygame
import pygame.mouse as mouse

class button():
	def __init__(self,x,y,img,img_pressed,callback):
		self.x = x
		self.y = y
		self.img = img
		self.img_pressed = img_pressed
		self.callback = callback

		self.isHighlighted = False

	def testForMouse(self):
		mousePos = mouse.get_pos()
		selfSize = self.img.get_size()
		if((self.x <= mousePos[0] <= self.x + selfSize[0]) and (self.y <= mousePos[1] <= self.y + selfSize[1])):
			self.isHighlighted = True
			if(mouse.get_pressed()[0]):
				self.callback()

		else:
			self.isHighlighted = False

	def render(self,surface):
		surface.blit(self.img if not self.isHighlighted else self.img_pressed,[self.x,self.y])

	def cycle(self,surface):
		self.testForMouse()
		self.render(surface)

class settingsButton(button):
	def __init__(self,x,y,img_F,img_T,img2_F,img2_T,callback,boolean):
		self.x = x
		self.y = y
		self.img1 = img_F
		self.img1_T = img_T
		self.img2 = img2_F
		self.img2_T = img2_T
		self.callback = callback
		self.boolean = boolean

		self.isHighlighted = False

	def testForMouse(self):
		mousePos = mouse.get_pos()
		selfSize = self.img.get_size()
		if((self.x <= mousePos[0] <= self.x + selfSize[0]) and (self.y <= mousePos[1] <= self.y + selfSize[1])):
			self.isHighlighted = True
			self.boolean = not self.boolean
			if(mouse.get_pressed()[0]):
				self.callback()

		else:
			self.isHighlighted = False

	def render(self,surface):
		surface.blit(self.img if not self.isHighlighted else self.img_pressed,[self.x,self.y])

	def cycle(self,surface):
		self.testForMouse()
		self.render(surface)


