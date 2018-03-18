import pygame
import sys
import random

###################################精灵类#############################################
# 我方飞机类，继承自Sprite类
class Hero(pygame.sprite.Sprite):
    # 构造方法，参数分别是我方飞机图片和起始坐标
    def __init__(self, hero_surface, hero_init_pos):
        # 调用父类的构造方法
        pygame.sprite.Sprite.__init__(self)
        # 设置属性
        self.image = hero_surface  # image属性：我方飞机图片
        self.rect = self.image.get_rect()  # rect属性：矩形
        self.rect.topleft = hero_init_pos  # 矩形左上角坐标
        self.bullets = pygame.sprite.Group()  # bullets属性：子弹组，使用精灵组
        self.is_hit = False  # 玩家是否被击中
        self.explode_index = 0
        self.speed = 8  # speed属性：我方飞机移动速度，比上例调快了一倍

        # 移动方法，参数是offset列表
    def move(self, offset):
        # 计算新的x、y坐标
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        # 对rect属性赋值，调整我方飞机位置
        # 同时防止我方飞机越出边界
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y

            # 发射子弹方法，参数为子弹图片z

    def shoot(self, bullet_surface1,bullet_surface2,level):
        # 子弹初始位置在我方飞机的上方居中位置
        if level==1:
            bullet = Bullet(bullet_surface1, self.rect.midtop)
            self.bullets.add(bullet)
        if level==2:
            bullet1 = Bullet(bullet_surface2, self.rect.topleft)
            bullet2= Bullet(bullet_surface2, self.rect.topright)
            self.bullets.add(bullet1)
            self.bullets.add(bullet2)
        if level==3:
            bullet3 = Bullet(bullet_surface1, self.rect.midtop)
            bullet4 = Bullet(bullet_surface2, self.rect.topleft)
            bullet5 = Bullet(bullet_surface2, self.rect.topright)
            self.bullets.add(bullet3)
            self.bullets.add(bullet4)
            self.bullets.add(bullet5)

# 子弹类，继承自Sprite类
class Bullet(pygame.sprite.Sprite):
    # 构造方法，参数分别是子弹图片和起始位置
    def __init__(self, bullet_surface, bullet_init_pos):
        # 调用父类的构造方法
        pygame.sprite.Sprite.__init__(self)
        # 设置属性
        self.image = bullet_surface  # image属性：子弹图片
        self.rect = self.image.get_rect()  # rect属性：矩形
        self.rect.topleft = bullet_init_pos  # 矩形左上角坐标
        self.speed = 10  # speed属性：子弹移动速度

    # 移动方法
    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        # 如果子弹移出屏幕上方，则销毁子弹对象
        if self.rect.top < -self.rect.height:
            self.kill()

# 敌方飞机类，继承自Sprite类
class Enemy(pygame.sprite.Sprite):
    # 构造方法，参数分别是敌方飞机图片和起始坐标
    def __init__(self, surface, init_pos,level):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.explode_index = 0
        self.is_drop = False
        if level==1:
            self.speed = 1
        if level==2:
            self.speed = 3
        if level==3:
            self.speed = 5

    # 移动方法
    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.is_drop = True


################################################################################


# 击落敌方飞机得分
ENEMY_SCORE = 100

# 生命数
LIVE = 5

# 屏幕宽、高
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 游戏帧率
FRAME_RATE = 60

# 动画周期
ANIMATE_CYCLE = 30

# 创建游戏窗口
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('飞机大战v1.0')

#字体
game_font = pygame.font.SysFont('方正琥珀简体', 25, False)  # 字体


# 载入游戏音乐
bullet_sound = pygame.mixer.Sound('data/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('data/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('data/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('data/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


# 加载图片资源
bg = pygame.image.load('data/pic/background.png')  # 背景图片
shoot_img = pygame.image.load('data/pic/shoot.png')  # 游戏资源图片
game_over = pygame.image.load('data/pic/gameover.png')  # 背景图片
hero_surface = list()
hero_surface.append(shoot_img.subsurface(pygame.Rect(0, 99, 102, 126)))  # 我方飞机图片1
hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 360, 102, 126)))  # 我方飞机图片2

# 玩家爆炸精灵图片区域
hero_hit_group = pygame.sprite.Group()
hero_hit_surface = list()
hero_hit_surface.append(shoot_img.subsurface(pygame.Rect(165, 234, 102, 126)))
hero_hit_surface.append(shoot_img.subsurface(pygame.Rect(330, 624, 102, 126)))
hero_hit_surface.append(shoot_img.subsurface(pygame.Rect(330, 498, 102, 126)))
hero_hit_surface.append(shoot_img.subsurface(pygame.Rect(432, 624, 102, 126)))

#bullet_surface = shoot_img.subsurface(pygame.Rect(70, 80, 9, 21))  # 子弹图片
bullet_surface = pygame.image.load('data/pic/shoot1.png')  # 子弹图片1
bullet_surface1 = pygame.image.load('data/pic/shoot2.png')  # 子弹图片2
# 创建被击中的敌方飞机组
enemy_hit_group = pygame.sprite.Group()
enemy_hit_surface = list()
enemy_hit_surface.append(shoot_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_hit_surface.append(shoot_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_hit_surface.append(shoot_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_hit_surface.append(shoot_img.subsurface(pygame.Rect(930, 697, 57, 43)))

# 创建我方飞机对象
hero_pos = [200, 500]
hero = Hero(hero_surface[0], hero_pos)

# 创建敌方飞机组
enemy_group = pygame.sprite.Group()
enemy_surface = shoot_img.subsurface(pygame.Rect(534, 612, 57, 43))  # 敌方飞机图片

# 其它变量
ticks = 0  # 计数
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}  # 我方飞机移动值
clock = pygame.time.Clock()  # 时钟
score = 0  # 得分
hit_ed_times = 0 #被击中次数
level = 1 # 等级

# 被击中的敌方飞机字典
enemy_hit_dict = dict()

Play_sign = True


while Play_sign:
    # 控制游戏帧率
    clock.tick(FRAME_RATE)
    ticks += 1

    if score <= 2000:
        level = 1
    elif score >2000 and score <= 4000:
        level = 2
    elif score >4000:
        level = 3

    # 改变我方飞机图片，以产生动画效果
    if  ticks >= ANIMATE_CYCLE:
        ticks = 0
    hero.image = hero_surface[ ticks // (ANIMATE_CYCLE // 2)]

    #生成敌机
    if ticks % 60 == 0:
        enemy = Enemy(enemy_surface,[random.randint(0, SCREEN_WIDTH - enemy_surface.get_width()),-enemy_surface.get_height()],level)
        enemy_group.add(enemy)

    # 敌机是否逃脱
    if not hero.is_hit:
        for enemy in enemy_group:
            enemy.update()
            if enemy.is_drop:
                hit_ed_times += 1
                hero_hit_group.add(hero)
                enemy_group.remove(enemy)
            if hit_ed_times == LIVE:
                game_over_sound.play()
                hero.is_hit = True
                break

    # 检测我方子弹是否击中敌方飞机
    if not hero.is_hit:
        enemy_hit_dict = pygame.sprite.groupcollide(enemy_group, hero.bullets, True, True)
        score += len(enemy_hit_dict) * ENEMY_SCORE;  # 计算得分
        enemy_hit_group.add(enemy_hit_dict)

    #判断玩家是否被击中
    if not hero.is_hit:
        for enemy in enemy_group:
            enemy.update()
            if pygame.sprite.collide_rect(enemy, hero):
                score += ENEMY_SCORE
                enemy_hit_group.add(enemy)
                hero_hit_group.add(hero)
                enemy_group.remove(enemy)
                hit_ed_times += 1
                if hit_ed_times == LIVE:
                    game_over_sound.play()
                    hero.is_hit = True
                    break

    for event in pygame.event.get():
        # 退出事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            # 键盘按下事件
        if not hero.is_hit:
            if event.type == pygame.KEYDOWN:
                if event.key in offset:
                    offset[event.key] = hero.speed  # 我方飞机的移动值为speed属性值
            # 键盘松开事件
            if event.type == pygame.KEYUP:
                if event.key in offset:
                    offset[event.key] = 0
                    # 根据我方飞机的移动值，移动飞机
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        if ticks % 10 == 0:
            bullet_sound.play()
            hero.shoot(bullet_surface,bullet_surface1,level)

    # 子弹移动
    hero.bullets.update()  # 精灵组update时，会调用所有精灵的update方法
    # 绘制背景
    screen.blit(bg, [0, 0])
    # 绘制我方飞机
    if not hero.is_hit:
        hero.move(offset)
        screen.blit(hero.image, hero.rect)
    else:
        for hero_hit in hero_hit_group:
            screen.blit(hero_hit_surface[hero_hit.explode_index], hero_hit.rect)
            if ticks % (ANIMATE_CYCLE // 2) == 0:
                if hero_hit.explode_index < 3:
                    hero_hit.explode_index += 1
                else:
                    Play_sign = False

    # 绘制爆炸效果
    for enemy_hit in enemy_hit_group:
        screen.blit(enemy_hit_surface[enemy_hit.explode_index], enemy_hit.rect)
        if ticks % (ANIMATE_CYCLE // 10) == 0:
            if enemy_hit.explode_index < 3:
                enemy1_down_sound.play()
                enemy_hit.explode_index += 1
            else:
                enemy_hit_group.remove(enemy_hit)

    # 绘制子弹
    hero.bullets.draw(screen)  # 精灵组draw时，会将所有精灵绘制在surface上
    # 绘制敌方飞机
    enemy_group.draw(screen)
    # 绘制游戏得分
    screen.blit(game_font.render('当前得分：%d' % score, True, [105, 99, 104]), [20, 20])

    # 绘制生命数
    if not hero.is_hit:
        screen.blit(game_font.render('剩余生命：%d ' % (LIVE-hit_ed_times), True, [105, 99, 104]), [20, 60])
    else:
        screen.blit(game_font.render('剩余生命：0 ', True, [105, 99, 104]), [20, 60])

    # 绘制等级
    screen.blit(game_font.render('等级：%d ' % level, True, [105, 99, 104]), [20, 100])

    # 更新屏幕
    pygame.display.update()


screen.blit(game_over, (0, 0))
screen.blit(game_font.render('你的分数：%d' % score, True, [255, 0, 255]), [150, 420])
screen.blit(game_font.render('你的等级：%d' % level, True, [255, 0, 255]), [150, 450])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
