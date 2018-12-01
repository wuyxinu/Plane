import flying
import random
import config
import bullet
import enemy_bullet
import pygame
class BossPlane(flying.Flying):
	"""docstring for Boss"""
	boss_count=0
	def __init__(self,image):
		BossPlane.boss_count+=1
		self.X_direct=True
		self.Y_direct=True
		self.life = 5
		x=random.randint(0,config.GAME_WIDTH-image.width())
		y=0 - image.height()
		width=image.width()
		height=image.height()
		self.tag='Boss'+str(BossPlane.boss_count)
		super().__init__(x,y,width,height,image)
	def step(self,canvas, score):

		speed = score / 100
		#X方向
		if self.X_direct == True and self.Y_direct == True: #规定向右为正方向
			self.x += 2
			self.y += 2
			#使用画布
			#canvas.move(tag, x, y):
			canvas.move(self.tag, 2, 2)
		elif self.X_direct == False and self.Y_direct == True: #self.direct = False
			self.x -= 2
			self.y += 2
			canvas.move(self.tag, -2, 2)
		elif self.X_direct == True and self.Y_direct == False: #self.direct = False
			self.x += 2
			self.y -= 2
			canvas.move(self.tag, 2, -2)
		elif self.X_direct == False and self.Y_direct == False: #self.direct = False
			self.x -= 2
			self.y -= 2
			canvas.move(self.tag, -2, -2)


		#判断蜜蜂的移动方向
		if self.x > config.GAME_WIDTH - self.width:
			self.X_direct = False
		elif self.x < 0:
			self.X_direct = True
		if self.y > config.GAME_WIDTH / 2 + self.height:
			self.Y_direct = False
		elif self.y < 0:
			self.Y_direct = True

	def bmob(self,enemy):
		if enemy.x-self.width<self.x<enemy.x+enemy.width:
		#y方向必须检测，否则小蜜蜂会从英雄机穿过去不符合常理
			if enemy.y-self.height<self.y<enemy.y+enemy.height:
				return True
			return False
	def out_of_bounds(self):
		if self.y>config.GAME_HEIGHT:
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

	
