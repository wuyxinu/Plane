# bullet.py
import flying
import config
import pygame
class enemy_Bullet(flying.Flying):
    """
    子弹类
    1.包含一个__init__方法
        a)使用enemy_bullet_count来记录子弹的数量
        b)x,y坐标的获取是根据敌机的位置决定的，
            暂时获取不到
        c)w,h根据image获取到的
        d)设置tag属性，作为唯一标识
        e)调用父类的__init__方法
    2.子弹的移动
        def step(self, canvas)
        a)由于子弹只在Y方向移动，所以只需考虑Y轴即可
            - X：X的位置不变
            - Y：考虑Y轴的速度即可
    3.子弹的越界判断
        def out_of_bounds(self)
        a)只需判断Y方向是否越界即可
    4.碰撞检测
        def bmob(self, enemy)
        a)从X方向判断子弹与英雄机是否发生碰撞
        b)Y方向判断子弹与英雄机是否发生碰撞
    """
    enemy_bullet_count = 0
    def __init__(self, x, y, image):
        enemy_Bullet.enemy_bullet_count += 1
        width = image.width()
        height = image.height()
        self.tag = 'enemy_Bullet_' + str(enemy_Bullet.enemy_bullet_count)
        super().__init__(x, y, width, height, image)

    # 子弹的移动
    def step(self, canvas):
        self.y += 5
        canvas.move(self.tag, 0, 5)

    # 子弹的越界
    def out_of_bounds(self):
        if self.y > config.GAME_HEIGHT + self.height:
            return True
        return False

    # 子弹的碰撞检测
    def bmob(self, hero_plane):
        if hero_plane.x - self.width < self.x < hero_plane.x + hero_plane.width:
            if hero_plane.y - self.height < self.y < hero_plane.y+ hero_plane.height:
                return True
            return False
