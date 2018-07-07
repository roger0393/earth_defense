#encoding=utf-8
import pygame

class Settings():
    """储存《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏静态的设置"""

        # 屏幕设置
        self.screen_width = 711
        self.screen_height = 720
        self.bg_color = (195, 200, 201)
        self.background = pygame.image.load("/usr/lib/earth_defense/images/background.png")
        self.delay = 60

        # 飞船的设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        self.switch_image = False

        # 子弹设置
        self.bullet_speed_factor = 2
        self.bullets_allowed = 3
        self.bullet_sound = pygame.mixer.Sound("/usr/lib/earth_defense/sounds/bullet.wav")
        self.bullet_sound.set_volume(0.2)

        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        #子弹和外星人相撞
        self.alien_down = pygame.mixer.Sound("/usr/lib/earth_defense/sounds/alien_down.wav")
        self.alien_down.set_volume(0.4)

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 6
        self.bullet_speed_factor = 8
        self.alien_speed_factor = 8

        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1

        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高游戏速度和外星人点数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
        
