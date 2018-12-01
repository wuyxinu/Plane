#bullet.py

import flying
import random
import config

class Bullet(flying.Flying):
	'''
		子弹类：
		1.包含一个__init__方法
		a)使用bullet_count来记录子弹的数量
		b)x,y的获取是根据英雄机的位置决定的，暂时获取不到
		c)width，height根据image获取到的
		d)设置tage属性，作为唯一标识
		e)调用父类的__init__方法
		2.子弹的移动
		def step(self, canvas)
			a)子弹只在Y方向移动，所以只考虑Y轴即可
		3.子弹的越界判断
		def out_of_bounds(self)
			a)子弹只在Y方向移动，所以只考虑Y轴即可
		4.碰撞检测
		def bmob(self, enemy)
		'''

	bullet_count = 0
	def __init__(self, x, y,image):
		#每创造一个子弹，就会调用一个__init__函数
		Bullet.bullet_count += 1
		#随机产生的第一个参数到第二个参数中的随机整数
		width = image.width()
		height = image.height()
		self.tag = 'Bullet_' + str(Bullet.bullet_count)
		super().__init__(x, y, width, height, image)

	#子弹的移动方式
	def step(self, canvas):
		#Y方向
		self.y -= 5

		canvas.move(self.tag, 0, -5)


	def step1(self, canvas):
		self.x -= 5
		self.y -= 5
		canvas.move(self.tag, -5, -5)

	def step2(self, canvas):
		self.x += 5
		self.y -= 5
		canvas.move(self.tag, 5, -5)

	def step3(self, canvas):
		self.x -= 2
		self.y -= 5
		canvas.move(self.tag, -2, -5)

	def step4(self, canvas):
		self.x +=2
		self.y -=5
		canvas.move(self.tag, +2, -5)

	#子弹的越界判断
	def out_of_bounds(self):
		if self.y < 0 - self.height:
			return True
		if self.x < 0 - self.width:
			return True
		if self.x > config.GAME_WIDTH:
			return True
		return False

	#子弹的碰撞检测
	def bmob(self, enemy):
		if enemy.x - self.width < self.x < enemy.x + enemy.width:
			if enemy.y - self.height < self.y < enemy.y + enemy.height:
				return True
		return False