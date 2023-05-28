import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from alien import Alien
from bullet import Bullet


class AlienInvasion:
    '''初始化游戏并创建游戏资源'''

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        # self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width=self.screen.get_rect().width
        # self.settings.screen_heigtht=self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.stats=GameStats(self)
        self.ship = Ship(self)
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self._create_fleet()
        self.play_button=Button(self,"Play")

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        '''响应案件和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    def _check_play_button(self,mouse_pose):
        '''在玩家点击Play的按钮时开始新游戏'''
        if self.play_button.rect.collidepoint(mouse_pose):
            #重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active=True
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
    def _check_keydown_events(self, event):
        '''响应按键'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''响应松开'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''创建一个子弹,并将其加入编组'''
        if len(self.bullets) < self.settings.bullets_allowed:
            # 满足self.bullets内的的长度小于settings内的设置
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''更新子弹位置并删除消失的子弹'''
        '''更新子弹位置'''
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查是否有子弹几种了外星人
        # 如果是就删除子弹和外星人
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹几种了外星人
        # 如果是就删除子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if not self.aliens:
            # 删除现有的子弹并创建一群外星人
            self.bullets.empty()
            self._create_fleet()

    def _update_screen(self):
        '''更新屏幕上的图像,并切换到新屏幕'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitem()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _create_fleet(self):
        '''创建外星人群'''
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人宽度
        alien = Alien(self)
        alien_width ,alien_height= alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # 计算可以容纳多少行外星人
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
        number_rows=available_space_y//(2*alien_height)
        #       创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        alien = Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height+ 2 * (alien_height * row_number)
        self.aliens.add(alien)




    def _update_aliens(self):
        '''更新外星人群中所有外星人的位置'''
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
           self._ship_hit()
        self._check_fleet_edges()
        self._check_alien_bottom()




    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''整体外星人下移,并改变他们的方向'''
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _ship_hit(self):
        '''响应飞船被外星人撞到'''
        if self.stats.ships_left>0:
            # 将ships_left-1
            self.stats.ships_left -= 1
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人,并将飞船放到屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停0.5s
            sleep(0.5)
        else:
            self.stats.game_active=False
    def _check_alien_bottom(self):
        '''检查是否有外星人到达了屏幕底部'''
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                #像飞船被撞到一样处理
                self._ship_hit()
                break
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
