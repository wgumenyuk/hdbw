import pygame as pg
from game import Game

pg.init()
pg.font.init()
pg.mixer.init()

game = Game()
game.run()

pg.quit()
exit(0)