import time
import queue
import threading
import pygame as pg
from reactor import *
from engine import *
from slider import *
from settings import *

class Game():
    def __init__(self):
        self.game = True
        self.engine = Engine()
        self.tick_time = tick_time
        self.input_queue = queue.Queue()
        self.game_reactor = Reactor(game_controller=self)

        self.name_font = name_font
        self.parametrs_font = parametrs_font

        self.image1 = self.engine.load_image('images/','1.jpg')

        self.suz_slider = Slider(50, 200, 50, 300,80,50, 0.0, 1.0, 0.5, "Положение СУЗ")
        self.turbine_slider = Slider(250, 200, 50, 300, 80, 50, 0.0, 1.0, 0.0, "Мощность Турбин")

    def set_game(self, game):
        self.game = game

    def draw_game_scene(self, cur_reactor):
        self.engine.fill_game_surf((0, 0, 0))
        self.engine.render_text(self.name_font, 'РБМК-1000', 50, 25)
        self.engine.render_obj(self.image1, 595, 0)

        self.suz_slider.draw(self.engine.get_game_surf())
        self.turbine_slider.draw(self.engine.get_game_surf())

        self.engine.render_text(self.parametrs_font,f"Шаг симуляции (тик): {cur_reactor.ticks}", 400, 500)
        self.engine.render_text(self.parametrs_font,f"Ядерная реактивность: {cur_reactor.kernel_react:.2f} k",400,550)
        self.engine.render_text(self.parametrs_font,f"Темп. реактивность: {cur_reactor.temp_react:.2f} k",400,600)
        self.engine.render_text(self.parametrs_font,f"Общая реактивность: {cur_reactor.all_react:.2f} k",400,650)
        self.engine.render_text(self.parametrs_font,f"Выделение тепла: {cur_reactor.new_heat:.2f} МВт",800,500)
        self.engine.render_text(self.parametrs_font, f"Охлаждение: {cur_reactor.new_cooling:.2f} МВт", 800, 550)
        self.engine.render_text(self.parametrs_font, f"Мощность: {cur_reactor.power:.2f} МВт", 800, 600)
        self.engine.render_text(self.parametrs_font, f"Температура: {cur_reactor.temperature:.2f} °C ", 800, 650)

    def math_tread(self):
        while self.game:
            self.game_reactor.math_physics()
            time.sleep(self.tick_time)

    def start(self):
        math_thread = threading.Thread(target=self.math_tread, daemon=True)
        math_thread.start()

        while self.game:
            self.draw_game_scene(self.game_reactor)
            self.engine.render_screen()
            self.game_reactor.explosion()
            pg.display.flip()

            for event in pg.event.get():
                self.suz_slider.handle_event(event)
                self.turbine_slider.handle_event(event)

                if event.type == pg.QUIT:
                    self.game = False
                    pg.quit()
                if event.type == pg.VIDEORESIZE:
                    self.engine.change_size(event.size)

            if self.suz_slider.is_dragging:
                self.game_reactor.height_kernel = self.suz_slider.get_value()
            if self.turbine_slider.is_dragging:
                self.game_reactor.turbine_power = self.turbine_slider.get_value()