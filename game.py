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
        self.explosion = False
        self.game_reactor = Reactor()

        self.name_font = name_font
        self.parametrs_font = parametrs_font

        self.image1 = self.engine.load_image('images/','1.jpg')

        self.suz_slider = Slider(50, 200, 50, 300,80,50, 0.0, 1.0, 0.5, "Положение СУЗ")
        self.turbine_slider = Slider(250, 200, 50, 300, 80, 50, 0.0, 1.0, 0.0, "Мощность Турбин")



    def draw_game_scene(self, cur_reactor):
        if not self.explosion:
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

    def draw_accident_scene(self, cur_reactor):
        accident = cur_reactor.explosion()
        if accident is not None:
            self.explosion = True
            self.engine.fill_game_surf((0, 0, 0))
            if accident == 'MAX_POWER_EXP':
                self.engine.render_text(self.parametrs_font,'Произошла авария на ЧАЭС. Реактор РБМК-1000 разрушен. Активной зоны больше нет.', 25,50)
                self.engine.render_text(self.parametrs_font, f'Мощность реактора: {cur_reactor.power:.2f} ||| Максимально допустимая мощность реактора: {cur_reactor.max_power:.2f}', 25, 100)
                self.engine.render_text(self.parametrs_font, f'Температура реактора: {cur_reactor.temperature:.2f} ||| Максимально допустимая температура реактора: {cur_reactor.max_temperature:.2f}', 25, 150)
                self.engine.render_text(self.parametrs_font,f'Колличество тиков: {cur_reactor.ticks}',25,200)
            if accident == 'MAX_TEMP_EXP':
                self.engine.render_text(self.parametrs_font,'Произошла авария на ЧАЭС. Реактор РБМК-1000 разрушен.', 25,50)
                self.engine.render_text(self.parametrs_font, 'Давление пара разорвало технологические каналы и сорвало крышку реактора!', 25, 100)
                self.engine.render_text(self.parametrs_font, f'Мощность реактора: {cur_reactor.power:.2f} ||| Максимально допустимая мощность реактора: {cur_reactor.max_power:.2f}', 25, 150)
                self.engine.render_text(self.parametrs_font, f'Температура реактора: {cur_reactor.temperature:.2f} ||| Максимально допустимая температура реактора: {cur_reactor.max_temperature:.2f}', 25, 200)
                self.engine.render_text(self.parametrs_font,f'Колличество тиков: {cur_reactor.ticks}',25,250)

    def math_thread(self):
        while self.game and not self.explosion:
            self.game_reactor.math_physics()
            time.sleep(self.tick_time)

    def start(self):
        math_thread = threading.Thread(target=self.math_thread, daemon=True)
        math_thread.start()


        while self.game:
            self.draw_game_scene(self.game_reactor)
            self.engine.render_screen()
            self.draw_accident_scene(self.game_reactor)
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