#enemy_plane.py

import flying
import random
import config
import enemy_bullet
import pygame

class EnemyPlane(flying.Flying):
	'''
		敌机类
		1.包含一个__init__方法
			a)使用enemy_count(index)来记录敌机的数量
			b)获取敌机的x, y坐标，坐标的获取是根据游戏的窗口随机产生的
			c)width 和 height是根据图片的宽高获取的
			d)设置tag 属性，作为唯一标识，是用来删除图片的
		2.敌机的移动方式
		def step(self, canvas)
		a)敌机仅在y方向都可以移动
		 -Y :只需要判断向下的移动速度即可
	'''
	enemy_count = 0
	def __init__(self, image):
		#每创造一个蜜蜂，就会调用一个__init__函数
		EnemyPlane.enemy_count += 1
		#随机产生的第一个参数到第二个参数中的随机整数
		x = random.randint(0, config.GAME_WIDTH - image.width())
		y = 0 - image.height()
		width = image.width()
		height = image.height()
		self.tag = 'EnemyPlane_' + str(EnemyPlane.enemy_count)
		super().__init__(x, y, width, height, image)

	#敌机的移动方式
	def step(self, canvas, score):
		#Y方向
		speed = 3 + score / 1000
		self.y += speed

		canvas.move(self.tag, 0, speed)

	#敌机的越界判断
	def out_of_bounds(self):
		if(self.y > config.GAME_HEIGHT):
			return True
		return False

	def shoot(self, enemy_bullet_image):
		# 确定子弹的x坐标
		x = self.x + (self.width - enemy_bullet_image.width())/2 + 1
		# 确定子弹的y坐标
		y = self.y +self.height+ enemy_bullet_image.height()
		# 创建子弹实例(对象)
		enemy_bul = enemy_bullet.enemy_Bullet(x, y, enemy_bullet_image)
		return enemy_bul