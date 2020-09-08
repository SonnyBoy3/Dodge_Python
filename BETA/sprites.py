# Sprite classes for platform game
from Settings import *
import pygame as pg

vec = pg.math.Vector2
def draw_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_WIDTH  = 10
    fill = (pct /100) *BAR_LENGHT
    outline_rect = pg.Rect(x,y, BAR_LENGHT, BAR_WIDTH)
    fill_rect = pg.Rect(x,y,fill,BAR_WIDTH)
    pg.draw.rect(surf, WHITE, outline_rect, 3)
    pg.draw.rect(surf, GREEN, fill_rect)
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        Player_img = pg.transform.scale(pg.image.load(path.join(img_dir, "king_right.png")).convert(),(P_width,P_height))
        self.image = Player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH/2),(HEIGHT/2))
        self.pos = vec(WIDTH/2,HEIGHT-50)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            Player_img = pg.transform.scale(pg.image.load(path.join(img_dir, "king_left.png")).convert(),(P_width,P_height))
            self.image = Player_img
            self.image.set_colorkey(WHITE)
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            Player_img = pg.transform.scale(pg.image.load(path.join(img_dir, "king_right.png")).convert(),(P_width,P_height))
            self.image = Player_img
            self.image.set_colorkey(WHITE)
        if keys[pg.K_DOWN]:
            self.acc.y += 10
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 *self.acc
        if self.rect.right >= WIDTH :
            self.pos.x = WIDTH-(P_width/2)-1
        elif self.rect.left <= 0:
            self.pos.x = (P_width/2)+1
        self.rect.midbottom  = self.pos
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y += -PLAYER_JUMP
class Plateforms(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, name):
        pg.sprite.Sprite.__init__(self)
        Plateform_img = pg.transform.scale(pg.image.load(path.join(img_dir, name)).convert(), (w,h))
        Plat_rect = Plateform_img.get_rect()
        self.image = pg.transform.scale(Plateform_img,(w,h))
        self.image.set_colorkey(BLACK)
        self.rect = Plat_rect
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0,0)
class Plateforms_Move(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, name):
        pg.sprite.Sprite.__init__(self)
        Plateform_img = pg.transform.scale(pg.image.load(path.join(img_dir, name)).convert(), (w,h))
        Plat_rect = Plateform_img.get_rect()
        self.image = pg.transform.scale(Plateform_img,(w,h))
        self.image.set_colorkey(BLACK)
        self.rect = Plat_rect
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0,0)
        self.vel.x = 3
    def update(self):
        self.rect.x += self.vel.x
        if self.rect.right >= WIDTH+1 or self.rect.left <= 0:
            self.vel = -self.vel
class Ennemies(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        Ennemies_img = pg.image.load(path.join(img_dir, random.choice(SWORDS))).convert()
        self.imageF = Ennemies_img
        self.imageF.set_colorkey(BLACK)
        self.image = self.imageF.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width  / 3
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-20,-10)
        self.speedy = random.randrange(3,16)
        self.speedx = random.randint(-1,1)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last = pg.time.get_ticks()
    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last > 50:
            self.last = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pg.transform.rotate(self.imageF, self.rot)
            #Helps to manipulate the rotation and makes it look natural
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
class Mobs(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        Mob_img = pg.transform.scale(pg.image.load(path.join(img_dir, "snake.png")).convert(),(55,35))
        self.image = Mob_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width  -60
        self.rect.x = x
        self.rect.y = y
        self.vel = 5
    def update(self):
        self.now = pg.time.get_ticks()
        self.rect.x += self.vel
        if self.rect.right >= WIDTH+1 or self.rect.left <= 0:
            self.vel = -self.vel
            if self.vel < 0:
                Mob_img = pg.transform.scale(pg.image.load(path.join(img_dir, "snake_re.png")).convert(),(55,35))
                self.image = Mob_img
                self.image.set_colorkey(WHITE)
                self.radius = self.rect.width  -60
            if self.vel > 0:
                Mob_img = pg.transform.scale(pg.image.load(path.join(img_dir, "snake.png")).convert(),(55,35))
                self.image = Mob_img
                self.image.set_colorkey(WHITE)
                self.radius = self.rect.width  -60
class Portals(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5,60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Coins(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        Mob_img = pg.transform.scale(pg.image.load(path.join(img_dir, "coin0.png")).convert(),(20,20))
        self.image = Mob_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(21,WIDTH-21)
        self.rect.y = random.randrange(100,HEIGHT-80)
