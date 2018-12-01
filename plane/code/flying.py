#flying.py
#英雄机，敌机，小蜜蜂，子弹
#共同特点：x,y坐标，width， height
#根据共同特点抽象出的共同的父类Flying
class Flying(object):
	def __init__(self, x, y, width, height, image):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.image = image