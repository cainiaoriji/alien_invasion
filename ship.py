import pygame


class Ship:
    '''管理飞船的类'''

    def __init__(self, ai_game):
        # 初始化飞船并设置其初始化位置
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外形给矩阵
        self.image = pygame.image.load(
            'E:\PythonProject\\alien_invasion\源代码文件\chapter_13\\building_alien_fleet\images\ship.bmp')
        self.rect = self.image.get_rect()

        # 对于每艘新飞船,都将其放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''根据移动标志调整飞船位置'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 根据self.x更新rect对象
        self.rect.x = self.x

    def blitem(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        '''让飞船在屏幕底部居中'''
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)