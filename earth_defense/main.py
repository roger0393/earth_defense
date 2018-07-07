#encoding=utf-8
import pygame
from pygame.locals import *
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf



def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("保卫地球")

    # 加载背景音乐
    pygame.mixer.music.load('/usr/lib/earth_defense/sounds/game_music.wav')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(0, -1)

    # 创建play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建储存游戏统计信息的实例,并创建积分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:
        #设置帧数
        clock = pygame.time.Clock()
        clock.tick(60)

        if not ai_settings.delay % 3:
            ai_settings.switch_image = not ai_settings.switch_image

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens,
                             bullets)
            
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                          play_button)

        if ai_settings.delay == 0:
            ai_settings.delay = 60
        ai_settings.delay -= 1


run_game()
