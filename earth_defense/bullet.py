#encoding=utf-8
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """一个对飞船发射的子弹管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen


        # 在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.image = pygame.image.load('/usr/lib/earth_defense/images/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 储存用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.speed_factor = ai_settings.bullet_speed_factor

        self.delay = ai_settings.delay

    def update(self):
        """向上移动子弹"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)
        
