#encoding=utf-8
import sys
from time import sleep

import pygame

import cv2
import numpy as np
import copy
import math


from bullet import Bullet
from alien import Alien

camera=cv2.VideoCapture(0)
firstframe=None
cap_region_x_begin = 0.5  # start point/total width
cap_region_y_end = 0.5  # start point/total width
cap_region_x_end = 0.5

key = cv2.waitKey(1)&0xFF
    
while (key!=ord("s")):
    key = cv2.waitKey(1)&0xFF
    ret,img = camera.read()
    img = cv2.flip(img, 1)  # flip the frame horizontally 图像水平翻转
    cv2.rectangle(img, (int(cap_region_x_begin * img.shape[1]), 0),(img.shape[1], int(cap_region_y_end * img.shape[0])), (255, 0, 0), 2) #画矩形 x=320 y=120
    frame=img
    
    #添加字体
    #font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体
    #imgzi = cv2.putText(frame, '欢迎来到保卫地球！请按"s"键初始化，将纯色背景置于红框中', (50, 50), font, 1.2, (255, 255, 255), 2)
    #图像，文字内容， 坐标 ，字体，大小，颜色，字体厚度
    im = cv2.imread("/usr/lib/earth_defense/images/first.png")#读取图像
    frame[0:im.shape[0],0:im.shape[1]]=im[0:im.shape[0],0:im.shape[1]]


    cv2.imshow("beginning", frame)
    cv2.moveWindow("beginning",0,0)
#print('sss')
cv2.destroyAllWindows()


def gesture():

    cnt = 0




    

    ret, img = camera.read()
    img = cv2.flip(img, 1)  # flip the frame horizontally 图像水平翻转
    cv2.rectangle(img, (int(cap_region_x_begin * img.shape[1]), 0),
                  (img.shape[1], int(cap_region_y_end * img.shape[0])), (255, 0, 0), 2)  # 画矩形 x=320 y=240
    cv2.rectangle(img, (320, 0),
                  (557, 160), (0, 255, 0), 2) #宽237 高160
    #cv2.imshow('img', img)
    frame = img
    frame = frame[0:int(cap_region_y_end * frame.shape[0]),
            int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI选取上述区域
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 颜色空间转换 灰
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # 高斯模糊
    global firstframe
    if firstframe is None:
        firstframe = gray

    frameDelta = cv2.absdiff(firstframe, gray)  # 将两幅图像相减获得边
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  # 二值化
    #cv2.imshow('er', thresh)
    # thresh = cv2.dilate(thresh, None, iterations=2)  #膨胀
    # cnts= cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # 手势识别模块
    thresh1 = copy.deepcopy(thresh)  # 复制
    imagee, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 查找检测物体的轮廓
    # 返回值contours为一个list，list中每个元素都是图像中的一个轮廓，每个轮廓为一些点的集合 可直线连接的点
    length = len(contours)
    maxArea = -1
    if length > 0:
        for i in range(length):  # find the biggest contour (according to area)1
            temp = contours[i]
            area = cv2.contourArea(temp)
            if area > maxArea:
                maxArea = area
                ci = i

        res = contours[ci]
        hull = cv2.convexHull(res)  # 凸包 最大包起来
        drawing = np.zeros(img.shape,
                           np.uint8)  # 返回来一个IndentationError: expected an indented block给定形状和类型的用0填充的数组 drawing还是图形 img.shape为图像尺寸
        cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)  # 进行轮廓的颜色填充   #绿色 轮廓 厚度为2
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)  # 红色 凸包 厚度为3
        # isFinishCal,cnt = calculateFingers(res,drawing)
        drawing = drawing[0:int(cap_region_y_end * drawing.shape[0]),0:int(cap_region_x_end * drawing.shape[1])]  # clip the ROI选取上述区域
        cv2.imshow('result', drawing)
        cv2.moveWindow("result",720,359)

        #cv2.imshow('dr', drawing)
        #  convexity defect
        hull = cv2.convexHull(res, returnPoints=False)
        # global cnt
        if len(hull) > 3:
            defects = cv2.convexityDefects(res, hull)
            if type(defects) != type(None):  # avoid crashing.   (BUG not found)
                cnt = 0
                for i in range(defects.shape[0]):  # calculate the angle
                    s, e, f, d = defects[i][0]
                    start = tuple(res[s][0])
                    end = tuple(res[e][0])
                    far = tuple(res[f][0])
                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                    if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                        cnt += 1
                        cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            # isFinishCal=True
        # isFinishCal=False,cnt=0

        '''
        if triggerSwitch is True:
            if isFinishCal is True and cnt <= 2:
                print cnt
        '''
    # if cnt>0 :
    # print("%d" %cnt)
    # 手势追踪模块
    x, y, w, h = cv2.boundingRect(thresh)  # 矩形边框   用一个最小的矩形，把找到的形状包起来
    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 画矩形
    cv2.imshow("camera", frame)
    cv2.moveWindow("camera",720,33)
    # cv2.imshow("img", img)
    # cv2.imshow("Thresh", thresh)
    # cv2.imshow("frame2", frameDelta)
    # key = cv2.waitKey(1)&0xFF

    #print ("%d,%d"  %(x,y)) #左上为原点
    #print(img.shape[0])
    # camera.release()
    # cv2.destroyAllWindows()
    if x==0 and y==0:
        x=120
        y=160
    if x%2==1:
        x+=1
    if y%2==1:
        y+=1
    return x, y, cnt

def check_ketdown_event(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_ketup_event(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False

        
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """相应手势控制"""
    x,y,cnt=gesture()

    if cnt == 4 or cnt==3 or cnt ==2 or cnt==1:
        if not (ai_settings.delay % 10):  # 每十帧发射一颗移动的子弹
            if len(bullets) < ai_settings.bullets_allowed:
                ai_settings.bullet_sound.play()
                new_bullet = Bullet(ai_settings, screen, ship)
                bullets.add(new_bullet)
    if 3*x-ship.rect.centerx < 0:
        ship.moving_left = True
        ship.moving_right = False
    if 3*x - ship.rect.centerx > 0:
        ship.moving_right = True
        ship.moving_left = False
    if 4.5*y - ship.rect.centery < 0:
        ship.moving_up = True
        ship.moving_down = False
    if 4.5*y - ship.rect.centery > 0:
        ship.moving_down = True
        ship.moving_up = False
    if 3*x - ship.rect.centerx == 0:
        ship.moving_right = False
        ship.moving_left = False
    if 4.5*y - ship.rect.centery == 0:
        ship.moving_down = False
        ship.moving_up = False

    #print(2.7*x-ship.rect.centerx)
    '''
    print(x)
    print(ship.rect.centerx)
    print(3*x-ship.rect.centerx)
    '''
    '''
    print(y)
    print(ship.rect.centery)
    print(4.5*x-ship.rect.centery)
    print('ssssssssss')
    '''

    #print(ship.rect.centerx-3.2 * x + 192,4.5 * y - ship.rect.centery,cnt)
    #print(x,y)
    #print(ship.rect.centerx,ship.rect.centery,cnt)
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_ketdown_event(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_ketup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
                              aliens, bullets, mouse_x, mouse_y)
    key = cv2.waitKey(1) & 0xFF

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮使开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                   play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.blit(ai_settings.background, (0, 0))

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检删除发生碰撞的外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        ai_settings.alien_down.play()
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) ==0:
        # 如果整群外星人都被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        ai_settings.bullet_sound.play()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number 
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -=1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放到屏幕低端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
