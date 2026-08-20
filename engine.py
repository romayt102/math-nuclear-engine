import os
from settings import *


class Engine:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        self.game_surface = pg.Surface((WIDTH, HEIGHT))
        self.current_size = self.screen.get_size()

    def load_image(self, path,name_image):
        loading_image = pg.image.load(os.path.join(path,name_image)).convert_alpha()
        return loading_image

    def render_obj(self, obj,x_pos,y_pos):
        self.game_surface.blit(obj,(x_pos,y_pos))

    def render_screen(self):
        self.screen.blit(pg.transform.scale(self.game_surface, self.current_size),(0,0))

    def render_text(self, font,text,x_pos,y_pos, color=None):
        if color is not None:
            text = font.render(text, 1, color)
        else:
            text = font.render(text,1, (80,80,80))
        self.game_surface.blit(text,(x_pos,y_pos))

    def fill_game_surf(self, color):
        self.game_surface.fill(color)

    def get_game_surf(self):
        return self.game_surface

    def change_size(self, new_size):
        self.current_size = new_size

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
