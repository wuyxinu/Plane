#HeroPlane.py

import flying
import bullet
import pygame

#英雄机类
class heroPlane(flying. Flying):
	'''
	英雄机类：
	1.包含一个__init__方法
		a)英雄级唯一，不需要记录数量
		b)x,y坐标是根据窗体的宽高计算得到的
		c)宽高根据image获取
		d)给英雄级添加double_file属性来描述英雄机的火力等级
		e)调用父类的__init__方法
	2.英雄级的碰撞检测
		def bmob(self, enemy)
	3.单倍火力
		def shoot(self, bullet_image)
		a)首先判断英雄机的火力值
		b)确定子弹的x,y的初始化坐标
		c)创建子弹实例

	'''
	def __init__(self, image):
	#每创造一个蜜蜂，就会调用一个__init__函数
		#随机产生的第一个参数到第二个参数中的随机整数
		x = 150
		y = 450
		width = image.width()
		height = image.height()
		
		self.double_fire = 0
		self.unique_skill = 3
		self.tag = 'heroPlane'
		super().__init__(x, y, width, height, image)

		# 英雄级的碰撞检测
	def bmob(self, enemy):
		# if self.x - enemy.width < enemy.x < self.x + self.width:
		# 	if self.y - enemy.height < enemy.y < self.y + self.height:
		# 		return True
		# return False
		if enemy.x - self.width < self.x < enemy.x + enemy.width:
			if enemy.y - self.height < self.y < enemy.y + enemy.height:
				return True
		return False

	def shoot(self, bullet_image):
		#如果double_fire <= 0 是单倍火力
		#否则是双倍
		if self.double_fire <= 0:
			#确定子弹的x坐标
			x = self.x + (self.width - bullet_image.width())/ 2 + 1
			#确定子弹的y坐标
			y = self.y - bullet_image.height()
			#创建子弹实例
			bul = bullet.Bullet(x, y, bullet_image)
			return bul

	def double_shoot(self, bullet_image):
		if self.double_fire > 0:
		#确定x坐标
			x1 = self.x + self.width / 4
			x2 = self.x + self.width / 4 * 3
		#确定y坐标
			y = self.y - bullet_image.height()
		#创建子弹对象
			bul1 = bullet.Bullet(x1, y, bullet_image)
			bul2 = bullet.Bullet(x2, y, bullet_image)
			self.double_fire -= 2
			return bul1, bul2

	  # 三倍火力
	def treble_shoot(self, bullet_image):
		if 20 < self.double_fire <=40:
			x1 = self.x
			x2 = self.x + self.width/5*2
			x3 = self.x + self.width/5*4

			y = self.y - bullet_image.height()

			bul1 = bullet.Bullet(x1, y, bullet_image)
			bul2 = bullet.Bullet(x2, y, bullet_image)
			bul3 = bullet.Bullet(x3, y, bullet_image)
			#    self.double_fire -= 2
			return bul1, bul2, bul3

    # 五倍火力
	def quadruple_shoot(self, bullet_image):
		if self.double_fire >40:
			x1 = self.x
			x2 = self.x + self.width/9*2
			x3 = self.x + self.width/9*4
			x4 = self.x + self.width/9*6
			x5 = self.x + self.width/9*8

			y = self.y - bullet_image.height()

			bul1 = bullet.Bullet(x1, y, bullet_image)
			bul2 = bullet.Bullet(x2, y, bullet_image)
			bul3 = bullet.Bullet(x3, y, bullet_image)
			bul4 = bullet.Bullet(x4, y, bullet_image)
			bul5 = bullet.Bullet(x5, y, bullet_image)
			#   self.double_fire -= 3
			return bul1, bul2, bul3, bul4, bul5




