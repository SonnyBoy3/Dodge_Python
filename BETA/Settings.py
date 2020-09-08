#https://www.facebook.com/Segel.T
#http://blog-buch.rhcloud.com
#blossomblairr - Castle background
import random
import pygame as pg
from os import *

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")



TITLE = "PlateFormer"
WIDTH = 1200
HEIGHT = 600
FPS   = 60
font_name = pg.font.match_font('Times')
font_name1 = pg.font.match_font('Arial')
# Player properties
P_width = 37
P_height = 60
PLAYER_GRAV = 0.8
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12
PLAYER_JUMP = 14
#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED   = (255,0,0)
BLUE  = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

PLATFORM_LIST = [(0,HEIGHT - 40, WIDTH, 40,"Plateform.png"),
                (0,HEIGHT/3,100,27,"Plateform (2).png"),
                (WIDTH-300,HEIGHT-180,100,20,"Plateform (2).png"),
                (300,HEIGHT-180,100,20,"Plateform (2).png"),
                (WIDTH-100,HEIGHT/3,100,27,"Plateform (2).png")]
ENNEMY_LIST = [()]
PORTAL_LIST = [(0,HEIGHT-200),(WIDTH-5,HEIGHT-200)]
MOB_LIST = [(0,HEIGHT - 75),(WIDTH-150,HEIGHT - 75)]
PLAT_MOVE_LIST = [(400,300,100,20,"Plateform (2).png")]
SWORDS = ["SWORD.png","sword1.png"]
