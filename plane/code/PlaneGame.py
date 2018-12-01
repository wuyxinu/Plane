# PlaneGame.py

import config
import tkinter
import image
import HeroPlane
import bee
import bullet
import enemy_plane
import time
import random
import threading
import winsound
import pygame
import boss_plane
import enemy_bullet

#定义一个敌机的列表
enemys = []
#定义一个子弹的列表
bullets = []
bullets1 = []
bullets2 = []
bullets3 = []
bullets4 = []
all_bullets = [bullets, bullets1, bullets2, bullets3, bullets4]
# 定义一个敌机子弹的列表
enemy_bullets = []
#定义一个英雄机，保存hp对象
hp = ''
new_hp = ''
#获取初始生命值以及初始的分数
life = 3
score = 0
Skill_bomb = False
delay = 100
protection = 0
protection_active = False
protection_sev = False
state = True

#音乐文件读入
pygame.mixer.init()
First_music = pygame.mixer.Sound(config.MUSIC_1)
First_music.set_volume(0.2)
Once_shoot_music = pygame.mixer.Sound(config.MUSIC_2)
Once_shoot_music.set_volume(0.2)
double_shoot_music = pygame.mixer.Sound(config.MUSIC_3)
double_shoot_music.set_volume(0.2)
smallPlane_down = pygame.mixer.Sound(config.MUSIC_4)
smallPlane_down.set_volume(0.2)
bee_down = pygame.mixer.Sound(config.MUSIC_5)
bee_down.set_volume(0.2)
bigPlane_down = pygame.mixer.Sound(config.MUSIC_6)
bigPlane_down.set_volume(0.2)

#初始化游戏状态
game_state = config.GAME_START
#创建窗体
game_window = tkinter.Tk()
#设置标题
game_window.title('星球大战')


#设置窗体的大小
#获取屏幕的分辨率
screenwidth = game_window.winfo_screenwidth()
screenheight = game_window.winfo_screenheight()
#窗口的摆放位置
size = '%dx%d+%d+%d' % (config.GAME_WIDTH, config.GAME_HEIGHT, (screenwidth - config.GAME_WIDTH) / 2, 100)
game_window.geometry(size)

#获取图片
back_image, bee_image, bullet_image, hero_image, hero0_image, smallPlane_image, skill_image, bomb_image, protection_image, bigPlane_image = image.load_image(tkinter)
start_image, stop_image, pause_image = image.load_state_image(tkinter)
#获取画布
window_canvas = tkinter.Canvas(game_window)
#包装画布,fill 填充， expand可扩展
window_canvas.pack(fill = tkinter.BOTH, expand = tkinter.YES)


#定义颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


#用来控制敌机的入场频率
count = 0

def game_start():
	#获取初始的分数和生命值
	global life
	global score
	global hp
	life = 3
	score = 0
	#画背景，在窗口上面
	window_canvas.create_image(0, 0,anchor = tkinter.NW, image = back_image, tag = 'BACK')
	#画开始界面
	window_canvas.create_image(0, 0, anchor = tkinter.NW, image = start_image, tag = 'START')
	#得到英雄机的实例
	hp = HeroPlane.heroPlane(hero_image)
	#画英雄机
	window_canvas.create_image(hp.x, hp.y, anchor = tkinter.NW, image = hp.image, tag = 'HP')

def call_back_click(event):
	#event 事件，在这里代表鼠标
	#如果游戏状态为开始状态，则改为运行状态
	global life
	global game_state
	if game_state == config.GAME_START:
		game_state = config.GAME_RUNNING
		#画分数和生命值
		window_canvas.create_text(10, 10, anchor = tkinter.NW, text = '分数：%d' % (score), fill = 'red', font = 'time 24 bold', tag = 'SCORE')
		window_canvas.create_text(10, 50, anchor = tkinter.NW, text = '生命：%d' %(life), fill = 'red', font = 'time 24 bold', tag = 'LIFE')
		#删除开始界面
		window_canvas.delete('START')
		#删除暂停界面
		window_canvas.delete('PAUSE')
	if game_state == config.GAME_STOP:
		game_state = config.GAME_START
		window_canvas.delete('STOP')
		window_canvas.delete('HP')
		game_start()
def call_back_pause(event):
	#判断游戏暂停，点击中键
	#暂停状态再次点击左键继续进行游戏
	global game_state
	if game_state==config.GAME_RUNNING:
		game_state=config.GAME_START
		window_canvas.create_image(0,0,anchor=tkinter.NW,image=pause_image,tag='PAUSE')
def call_back_move(event):
	#event 事件，在这里代表鼠标
	#游戏状态应该为 GAME_RUNNNIG
	global game_state
	global protection_sev
	global protection_active
	global hp
	if game_state == config.GAME_RUNNING:	
		old_x = hp.x
		old_y = hp.y
		hp.x = event.x - hp.width/2
		hp.y = event.y - hp.height/2
		window_canvas.move('HP', hp.x - old_x, hp.y - old_y)
			

				
#开大招
def big_bomb(event):
	global game_state
	global score
	global life
	global Skill_bomb
	global protection
	global protection_active
	global protection_sev
	global state
	if game_state == config.GAME_RUNNING:
		if hp.unique_skill > 0:
			hp.unique_skill -= 1
			Skill_bomb = True
			for bul in bullets:
			#在画布中删除子弹和敌机
				window_canvas.delete(bul.tag)
			#将列表中的子弹全部删除
			bullets.clear()		
			for enemy in enemys:
				if isinstance(enemy, bee.Bee):
					play_music(5)#播放蜜蜂被摧毁声音
					a = random.randint(0, 10)
					if a == 0:
						life += 1
					elif a < 5:
						if protection <= 0:
							protection_sev = True
							state = True
						protection_active = True
						protection = 3
					else:
						hp.double_fire += 20
				if isinstance(enemy, enemy_plane.EnemyPlane):
					play_music(4)#播放敌机被摧毁声音
					score += 5
				if isinstance(enemy, boss_plane.BossPlane):
					play_music(4)#播放敌机被摧毁声音
					score += 100
			#在画布中删除敌机
				window_canvas.delete(enemy.tag)
			#将列表中的敌机全部删除
			enemys.clear()
			for enemy_bullet in enemy_bullets:
				window_canvas.delete(enemy_bullet.tag)
			enemy_bullets.clear() # 返回值为空列表[]，不是None

			window_canvas.create_image(0, 0, anchor = tkinter.NW, image = skill_image, tag = 'SKILL')
			window_canvas.create_image(0, 0, anchor = tkinter.NW, image = bomb_image, tag = 'BOMB')
			window_canvas.create_image(hp.x, hp.y, anchor = tkinter.NW, image = hp.image, tag = 'HP')
		

#产生敌机或者小蜜蜂
def next_one():
	#1, 20 1->5 bee 6->20 enemy
	a = random.randint(1, 100)
	enemy = ''
	if a <= 10:
		#产生小蜜蜂,创建小蜜蜂实例
		enemy = bee.Bee(bee_image)
	elif a <= 96 :
		enemy = enemy_plane.EnemyPlane(smallPlane_image)
	else :
		enemy = boss_plane.BossPlane(bigPlane_image)
	return enemy


def enter_action():
	#enter_action per 10ms 执行一次
	global count
	global hp
	global Skill_bomb
	if Skill_bomb == False:
		count += 1
		#让敌机每40ms 出现一架
		if count % 40 == 0:
			# 随机产生一架敌机
			enemy = next_one()
			# 将敌机放入敌机列表进行保存
			enemys.append(enemy)
			#测试
			window_canvas.create_image(enemy.x, enemy.y, anchor = tkinter.NW, image = enemy.image, tag = enemy.tag)

		if count % 40 == 0:
		#画子弹
			for enemy in enemys:
				if isinstance(enemy,enemy_plane.EnemyPlane):
					a = random.randint(1, 40)
					if a <= 5:
						# 画敌机子弹
						enemy_bul = enemy.shoot(bullet_image)
						# 将子弹添加到bullets中
						enemy_bullets.append(enemy_bul)
						window_canvas.create_image(enemy_bul.x, enemy_bul.y, anchor=tkinter.NW, image=enemy_bul.image, tag=enemy_bul.tag)
				if isinstance(enemy,boss_plane.BossPlane):
					# 画敌机子弹
					enemy_bul = enemy.shoot(bullet_image)
					# 将子弹添加到bullets中
					enemy_bullets.append(enemy_bul)
					window_canvas.create_image(enemy_bul.x, enemy_bul.y, anchor=tkinter.NW, image=enemy_bul.image, tag=enemy_bul.tag)

		#当英雄级为双倍火力时
			
			if hp.double_fire > 40:
				bul1, bul2, bul3, bul4, bul5= hp.quadruple_shoot(bullet_image)
				# 将子弹添加到bullets中
				bullets1.append(bul1)
				bullets3.append(bul2)
				bullets.append(bul3)
				bullets4.append(bul4)
				bullets2.append(bul5)
				window_canvas.create_image(bul1.x, bul1.y, anchor=tkinter.NW, image=bul1.image, tag=bul1.tag)
				window_canvas.create_image(bul2.x, bul2.y, anchor=tkinter.NW, image=bul2.image, tag=bul2.tag)
				window_canvas.create_image(bul3.x, bul3.y, anchor=tkinter.NW, image=bul3.image, tag=bul3.tag)
				window_canvas.create_image(bul4.x, bul4.y, anchor=tkinter.NW, image=bul4.image, tag=bul4.tag)
				window_canvas.create_image(bul5.x, bul5.y, anchor=tkinter.NW, image=bul5.image, tag=bul5.tag)
				play_music(3)
			elif 20 < hp.double_fire <= 40:
				bul1, bul2, bul3 = hp.treble_shoot(bullet_image)
				# 将子弹添加到bullets中
				bullets3.append(bul1)
				bullets.append(bul2)
				bullets4.append(bul3)
				window_canvas.create_image(bul1.x, bul1.y, anchor=tkinter.NW, image=bul1.image, tag=bul1.tag)
				window_canvas.create_image(bul2.x, bul2.y, anchor=tkinter.NW, image=bul2.image, tag=bul2.tag)
				window_canvas.create_image(bul3.x, bul3.y, anchor=tkinter.NW, image=bul3.image, tag=bul3.tag)
				play_music(3)
			elif 0 < hp.double_fire <= 20:
				bul1, bul2 = hp.double_shoot(bullet_image)
				# 将子弹添加到bullets中
				bullets.append(bul1)
				bullets.append(bul2)
				window_canvas.create_image(bul1.x, bul1.y, anchor=tkinter.NW, image=bul1.image, tag=bul1.tag)
				window_canvas.create_image(bul2.x, bul2.y, anchor=tkinter.NW, image=bul2.image, tag=bul2.tag)
				play_music(2)
			if hp.double_fire <=0:
				bul = hp.shoot(bullet_image)
				# 将子弹添加到bullets中
				bullets.append(bul)
				window_canvas.create_image(bul.x, bul.y, anchor=tkinter.NW, image=bul.image, tag=bul.tag)
				play_music(2)

			


def step_action():
	#遍历所有的敌机，调用敌机的step方法
	global score
	for enemy in enemys:
		enemy.step(window_canvas, score)
	#遍历所有的子弹，调用子弹的step
	for bullet in bullets:
		bullet.step(window_canvas)
	for bullet in bullets1:
		bullet.step1(window_canvas)
	for bullet in bullets2:
		bullet.step2(window_canvas)
	for bullet in bullets3:
		bullet.step3(window_canvas)
	for bullet in bullets4:
		bullet.step4(window_canvas)
	for enemy_bullet in enemy_bullets:
		enemy_bullet.step(window_canvas)

#子弹和敌机的越界判断
def out_of_bounds_action():
	for enemy in enemys:
		if enemy.out_of_bounds():
			enemys.remove(enemy)
			window_canvas.delete(enemy.tag)
	for bul in all_bullets:
		for bullet in bul:
			if bullet.out_of_bounds(): # 越界
				bul.remove(bullet)
				window_canvas.delete(bullet.tag)
	for enemy_bullet in enemy_bullets:
		if enemy_bullet.out_of_bounds(): # 越界
			enemy_bullets.remove(enemy_bullet)
			window_canvas.delete(enemy_bullet.tag)


def bmob_action():
	global hp
	global life
	global score
	global protection
	global protection_active
	global protection_sev
	global state
	#1。子弹同敌机的碰撞检测
	for bul in all_bullets:
		for bullet in bul:
			for enemy in enemys:
				#进行碰撞检测
				if bullet.bmob(enemy):
					if isinstance(enemy, boss_plane.BossPlane):
						if enemy.life > 0:
							enemy.life -= 1
							bul.remove(bullet)
							window_canvas.delete(bullet.tag)	
						else :
							#从列表中删除子弹和敌机
							bul.remove(bullet)
							enemys.remove(enemy)
							#在画布中删除子弹和敌机
							window_canvas.delete(bullet.tag)
							window_canvas.delete(enemy.tag)
							window_canvas.delete('Plane_bomb')
							play_music(4)#播放敌机被摧毁声音
							score += 100
							#如果击中蜜蜂
					else:
						#从列表中删除子弹和敌机
						bul.remove(bullet)
						enemys.remove(enemy)
						#在画布中删除子弹和敌机
						window_canvas.delete(bullet.tag)
						window_canvas.delete(enemy.tag)
						window_canvas.delete('SmallPlane_bomb')
						#如果击中蜜蜂
						if isinstance(enemy, bee.Bee):
							play_music(5)#播放蜜蜂被摧毁声音
							a = random.randint(0, 10)
							if a == 0:
								life += 1
							elif a < 5:
								if protection <= 0:
									protection_sev = True
									state = True
								protection_active = True
								protection = 3
							else:
								hp.double_fire += 20
						if isinstance(enemy, enemy_plane.EnemyPlane):
							play_music(4)#播放敌机被摧毁声音
							score += 5
						

	#2.英雄机同敌机的碰撞检测
	for enemy in enemys:
		#进行碰撞检测
		if hp.bmob(enemy):
			enemys.remove(enemy)
			window_canvas.delete(enemy.tag)
			if protection > 0:
				protection -= 1
			elif(protection == 0):
				protection_active = False
				protection_sev = True
				state = True
				protection-=1
			else:
				life -= 1
				hp.double_fire = 0
				hp.unique_skill = 3
			window_canvas.delete('LIFE')
			window_canvas.create_text(10, 50, anchor = tkinter.NW, text = '生命：%d' %(life), fill = 'red', font = 'time 24 bold', tag = 'LIFE')
			if life < 0:
				#游戏结束
				gameover()

	# 3.敌机子弹和英雄机的碰撞
	for enemy_bullet in enemy_bullets:
		if hp.bmob(enemy_bullet):
			# 1.让生命-1
			if protection > 0:
				protection -= 1
			elif(protection == 0):
				protection_active = False
				protection_sev = True
				state = True
				protection -= 1
			else:
				life -= 1  
				hp.double_fire = 0
				hp.unique_skill = 3
			# 2.在列表中删除该敌机子弹
			enemy_bullets.remove(enemy_bullet)
			# 3.在画布中删除敌机子弹
			window_canvas.delete(enemy_bullet.tag)
		elif life < 0: # GG
			gameover()




def gameover():
	global life
	global game_state
	global hp
	global protection
	global protection_sev
	global protection_active
	game_state = config.GAME_STOP

	for bul in bullets:
		#在画布中删除子弹和敌机
		window_canvas.delete(bul.tag)
	#将列表中的子弹全部删除
	bullets.clear()
	for enemy in enemys:
		#在画布中删除敌机
		window_canvas.delete(enemy.tag)
	#将列表中的敌机全部删除
	enemys.clear()

	for enemy_bullet in enemy_bullets:
		window_canvas.delete(enemy_bullet.tag)
	enemy_bullets.clear() # 返回值为空列表[]，不是None

	#将防护罩相关全部清零
	protection = 0
	protection_sev = False
	protection_active = False

	#播放英雄机被摧毁声音
	pygame.mixer.init()
	track = pygame.mixer.music.load(config.MUSIC_6)
	pygame.mixer.music.play()

	#画背景，在窗口上面
	window_canvas.create_image(0, 0,anchor = tkinter.NW, image = back_image, tag = 'BACK')
	hp = HeroPlane.heroPlane(hero_image)
	#画英雄机
	window_canvas.create_image(hp.x, hp.y, anchor = tkinter.NW, image = hp.image, tag = 'HP')

	window_canvas.create_image(0, 0, anchor = tkinter.NW, image = stop_image, tag = 'STOP')

def game_continue(event):
	global game_state
	if game_state == config.GAME_RUNNING:
		if event.x > config.GAME_WIDTH or event.x < 0:
			if event.y > config.GAME_HEIGHT or event.y < 0:
				print(event.x, event.y)
				game_state == config.GAME_PAUSE
				window_canvas.create_image(0, 0, anchor = tkinter.NW, image = pause_image, tag = 'PAUSE')

def draw_action():
	global hp
	#1.在画布上删除原本的分数和生命值
	window_canvas.delete('LIFE')
	window_canvas.delete('SCORE')
	window_canvas.delete('SKILL_NUM')
	#2.在画布上重画分数和生命值	
	window_canvas.create_text(10, 10, anchor = tkinter.NW, text = '分数：%d' %(score), fill = 'red', font = 'time 24 bold', tag = 'SCORE')
	window_canvas.create_text(10, 50, anchor = tkinter.NW, text = '生命：%d' %(life), fill = 'red', font = 'time 24 bold', tag = 'LIFE')
	window_canvas.create_text(10, 90, anchor = tkinter.NW, text = '大招：%d' %(hp.unique_skill), fill = 'red', font = 'time 24 bold', tag = 'SKILL_NUM')
					
def play_music(n):

	if(n == 1):
		First_music.play()
	elif n == 2:
		Once_shoot_music.play()
	elif n == 3:
		double_shoot_music.play()
	elif n == 4:
		smallPlane_down.play()
	elif n == 5:	
		bee_down.play()
	elif n == 6:
		bigPlane_down.play()


def game_play():
	global game_state
	pygame.mixer.init()
	track = pygame.mixer.music.load(config.MUSIC_BACK)
	if pygame.mixer.music.get_busy() == False:
		pygame.mixer.music.play(-1)

#背景音乐线程
def new_thread():
	#创建一个线程
	t1 = threading.Thread(target = game_play)
	#线程开始
	t1.setDaemon(True)
	t1.start()


def get_newplane():
	global life
	global new_hp
	global protection_active
	global protection_sev
	global state
	global hp
	if protection_active == True:
		if state == True:
			print(1)
			double_fire = hp.double_fire
			hp = HeroPlane.heroPlane(protection_image)
			window_canvas.delete("HP")
			window_canvas.create_image(hp.x, hp.y, anchor=tkinter.NW, image=hp.image, tag='HP')
			hp.double_fire = double_fire
			protection_sev = False
			state = False

# 从带有防护罩的英雄机变成原来的样子
def change_plane():
    global life
    global hp
    global protection_active
    global protection_sev
    global state
    if protection_active == False:
    	print(protection_sev)
    	if state == True:
	        print(2)
	        double_fire = hp.double_fire
	        window_canvas.delete("HP")
	        hp = HeroPlane.heroPlane(hero_image)
	        window_canvas.create_image(hp.x, hp.y, anchor=tkinter.NW, image=hp.image, tag='HP')
	        hp.double_fire = double_fire
	        state = False
	        protection_sev = False


def game():
	global life
	global Skill_bomb
	global delay
	global protection_active
	global protection
	if game_state == config.GAME_START:
		#游戏开始界面
		game_start()
		#添加鼠标监听
		window_canvas.bind('<Button-1>', call_back_click)
		window_canvas.bind('<Button-3>',  big_bomb)
		window_canvas.bind('<Motion>', call_back_move)
		window_canvas.bind('<Button-2>',call_back_pause)
		#敌机进场
		while True:
			if game_state == config.GAME_RUNNING:
				#让敌机和子弹进场
				enter_action()
				#让子弹和敌机动起来
				step_action()
				#子弹和敌机的越界判断
				out_of_bounds_action()

				#碰撞检测
				bmob_action()
				
				if life >= 0:
					#画分数和生命值
					draw_action()
				
				if(Skill_bomb == True):
					delay -= 1
					if(delay == 40):
						window_canvas.delete('BOMB')
					if(delay == 0):
						window_canvas.delete('SKILL')
						Skill_bomb = False
						delay = 100

				if protection_sev == True:
					print(protection)
					if protection_active == True:
						get_newplane()
					else:
						change_plane()
				
			#更新显示
			game_window.update()
			#设置单位时间间隔
			time.sleep(0.01)

#锁定模块窗口执行，让代码只能在这个文件下执行
if __name__ == '__main__':

	new_thread()
	game()
	
	game_window.mainloop()