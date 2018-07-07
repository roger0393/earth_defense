#!/usr/bin/env python
# coding=utf-8
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('/usr/lib/earth_defense/images/ship.png')
        self.image1 = pygame.image.load('/usr/lib/earth_defense/images/ship1.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        '''
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        '''

        self.rect.centerx = 318
        self.rect.centery = 684
        #print(self.screen_rect.centerx)  #320
        #print(self.screen_rect.bottom)   #720
 
        
        # 在飞船的属性center中储存小数值
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor * 1.5
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor * 1.5

        # 根据self.center更新rect对象
        '''
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        '''

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        #print(self.ai_settings.ship_speed_factor)
        '''
        print(self.moving_right)
        print(self.rect.right)
        print(self.screen_rect.right)
        print(self.moving_left)
        print(self.moving_up)
        print(self.moving_down)
        print('ssssssssssssss')
        '''
        


    def blitme(self):
        """在指定位置绘制飞船"""

        # 绘制飞机的两种不同的形式
        if self.ai_settings.switch_image:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.image1, self.rect)



    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
