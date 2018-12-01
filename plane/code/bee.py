#bee.py

import flying
import random
import config
import pygame
#蜜蜂类
class Bee(flying.Flying):
	"""
	蜜蜂类：
	1.包含一个__init__
		a)使用bee_count(index)来记录蜜蜂的数量
		b)获取蜜蜂的x, y坐标，坐标的获取是根据游戏的窗口随机产生的
		c)width 和 height是根据图片的宽高获取的
		d)tag 属性，是用来删除图片的
	2.蜜蜂的移动方式
		def step(self, canvas)
		a)蜜蜂在x,y方向都可以移动，所以都要考虑
		 -X :要判断蜜蜂的速度和移动方向
		 -Y :只需要判断向下的移动速度即可
	3.判断蜜蜂是否越界
		def out_of_bound(self)
		a)只需要判断y轴是否越界
	"""
	bee_count = 0
	def __init__(self, image):
		#每创造一个蜜蜂，就会调用一个__init__函数
		self.direct = True
		Bee.bee_count += 1
		#随机产生的第一个参数到第二个参数中的随机整数
		x = random.randint(0, config.GAME_WIDTH - image.width())
		y = 0 - image.height()
		width = image.width()
		height = image.height()

		self.tag = 'Bee_' + str(Bee.bee_count)
		super().__init__(x, y, width, height, image)

	#蜜蜂的移动方式
	def step(self, canvas, score):
		#Y方向
		self.y += 3

		#X方向
		if self.direct: #规定向右为正方向
			self.x += 3
			#使用画布
			#canvas.move(tag, x, y):
			canvas.move(self.tag, 3, 3)
		else: #self.direct = False
			self.x -= 3
			canvas.move(self.tag, -3, 3)

		#判断蜜蜂的移动方向
		if self.x > config.GAME_WIDTH - self.width:
			self.direct = False
		elif self.x < 0:
			self.direct = True

	#判断蜜蜂是否越界
	def out_of_bounds(self):
		if(self.y > config.GAME_HEIGHT):
			return True
		return False