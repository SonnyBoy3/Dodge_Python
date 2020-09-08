import pygame as pg
import random
from Settings import *
from sprites import *
from os import *
import time

def print_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        pg.mixer.music.load(path.join(snd_dir, "All of 0 Hitpoints Left.ogg"))
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play(loops=-1)
    def new(self):
        self.rand = 0
        self.health = 200
        # start a new game
        self.start = pg.time.get_ticks()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.ennemies = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.portal = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player = Player(self)
        for p in PORTAL_LIST:
            p = Portals(*p)
            self.all_sprites.add(p)
            self.portal.add(p)
        self.all_sprites.add(self.player)
        self.score = 0
        for i in range(3):
            ennemy = Ennemies()
            self.all_sprites.add(ennemy)
            self.ennemies.add(ennemy)
            if ennemy.rect.y > HEIGHT or ennemy.rect.x > WIDTH or ennemy.rect.x < 0:
                ennemy.kill()
                self.score += 10
        for p in PLATFORM_LIST:
            p = Plateforms(*p)
            self.platforms.add(p)
            self.all_sprites.add(p)
        for mob in MOB_LIST:
            mob = Mobs(*mob)
            self.all_sprites.add(mob)
            self.ennemies.add(mob)
        for p in PLAT_MOVE_LIST:
            p = Plateforms_Move(*p)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def update(self):
        self.now = pg.time.get_ticks()
        self.time = self.now - self.start
        if int(self.time) % 500 == 0:
            coin = Coins()
            self.coins.add(coin)
            self.all_sprites.add(coin)
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        hits = pg.sprite.spritecollide(self.player,self.portal, False)
        for hit in hits:
            self.rand += 1
            if self.rand % 2 == 0:
                self.player.pos = (WIDTH- P_width, HEIGHT/4)
            if self.rand % 2 == 1:
                self.player.pos = (P_width+1, HEIGHT/4)
        for ennemy in self.ennemies:
            if ennemy.rect.left > WIDTH or ennemy.rect.right < 0:
                self.score += 10
                ennemy.kill()
                n = Ennemies()
                self.all_sprites.add(n)
                self.ennemies.add(n)
        hits = pg.sprite.spritecollide(self.player, self.ennemies,False, pg.sprite.collide_circle)
        for hit in hits:
            player_dmg_snd = pg.mixer.Sound(path.join(snd_dir, "Hit_Hurt3.wav"))
            player_dmg_snd.play()
            hit.kill()
            h = Ennemies()
            self.all_sprites.add(h)
            self.ennemies.add(h)
            self.player.image = pg.transform.scale(pg.image.load(path.join(img_dir, "king_hurt.png")).convert(),(P_width,P_height))
            self.player.image.set_colorkey(WHITE)
            hit = Mobs(random.randrange(60,WIDTH-60),HEIGHT - 75)
            self.all_sprites.add(hit)
            self.ennemies.add(hit)
            self.health -= 30
            if self.health <= 0:
                self.player.image = pg.transform.scale(pg.image.load(path.join(img_dir, "king_dead.png")).convert(),(P_height,P_width))
                self.player.image.set_colorkey(WHITE)
                pg.display.flip()
                g.show_go_screen()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        hits = pg.sprite.groupcollide(self.platforms,self.ennemies, False, True)
        for hit in hits:
            self.score += 5
            n = Ennemies()
            self.all_sprites.add(n)
            self.ennemies.add(n)
        hits = pg.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            Coin = pg.mixer.Sound(path.join(snd_dir, "Pickup_Coin.wav"))
            Coin.play()
            self.score += 100
    def events(self):
        P_JUMP = pg.mixer.Sound(path.join(snd_dir,"Jump.wav"))
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    P_JUMP.play()
                    self.player.jump()
    def draw(self):
        backG = pg.transform.scale(pg.image.load(path.join(img_dir, "Background3.png")).convert(), (WIDTH,HEIGHT))
        backG_rect = backG.get_rect()
        self.now = pg.time.get_ticks()
        self.time = self.now - self.start
        # Game Loop - draw
        self.screen.blit(backG, backG_rect)
        self.all_sprites.draw(self.screen)
        print_text(self.screen, str(self.score), 22, WIDTH/2, 15)
        print_text(self.screen, str(int(self.time/1000)),22, WIDTH/2,40)
        draw_health(self.screen, 10, 10, self.health)
        # *after* drawing everything, flip the display
        pg.display.flip()
    def show_start_screen(self):
        # game splash/start screen
        backG = pg.transform.scale(pg.image.load(path.join(img_dir, "Background31.png")).convert(), (WIDTH,HEIGHT))
        backG_rect = backG.get_rect()
        self.screen.blit(backG, backG_rect)
        print_text(self.screen, "DODGE!",80, WIDTH/2, HEIGHT/4-100)
        print_text(self.screen, "Press a key to Start",30, WIDTH/2, HEIGHT*1.5/2)
        pg.display.flip()
        waiting = True
        while waiting == True:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYUP:
                    waiting = False
                    g.new()
    def show_go_screen(self):
        # game over/continue
        backG = pg.transform.scale(pg.image.load(path.join(img_dir, "Background3.png")).convert(), (WIDTH,HEIGHT))
        backG_rect = backG.get_rect()
        self.screen.blit(backG, backG_rect)
        pg.display.flip()
        time.sleep(1)
        backG = pg.transform.scale(pg.image.load(path.join(img_dir, "Background3.png")).convert(), (WIDTH,HEIGHT))
        backG_rect = backG.get_rect()
        self.screen.blit(backG, backG_rect)
        print_text(self.screen, "DODGE!",80, WIDTH/2, HEIGHT/4-100)
        print_text(self.screen, "YOUR SCORE WAS:",40, WIDTH/2, HEIGHT*3/4)
        print_text(self.screen, str(int(self.score)),22, WIDTH/2, HEIGHT* 3/4 + 60)
        pg.display.flip()
        time.sleep(2)
        waiting = True
        while waiting == True:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYUP:
                    waiting = False
                    g.new()


g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen

pg.quit()
