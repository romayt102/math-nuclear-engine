import time
import queue
import threading
from reactor import *
from engine import *
from settings import *

class Game():
    def __init__(self):
        self.game = True
        self.engine = Engine()
        self.tick_time = tick_time
        self.input_queue = queue.Queue()
        self.game_reactor = Reactor(game_controller=self)

    def set_game(self, game):
        self.game = game

    def draw_info(self, cur_reactor):
        if cur_reactor.step == 0:
            self.engine.cls()
            print('=== АЭС СИМУЛЯТОР ===')
            print(f"Шаг симуляции (тик): {cur_reactor.ticks}")
            print(f"Текущий уровень ТВЭЛ: {cur_reactor.height_kernel}")
            print(f"Текущая мощность турбин: {cur_reactor.turbine_power}")
            print('---------------------')
            print(f"Ядерная реактивность: {cur_reactor.kernel_react:.2f}")
            print(f"Темп. реактивность:  {cur_reactor.temp_react:.2f}")
            print(f"Общая реактивность:  {cur_reactor.all_react:.2f}")
            print(f"Текущая мощность:    {cur_reactor.power:.2f}")
            print(f"Выделение тепла:     {cur_reactor.new_heat:.2f}")
            print(f"Охлаждение:          {cur_reactor.new_cooling:.2f}")
            print(f"Новая температура:   {cur_reactor.temperature:.2f}")
            print('=====================')

            print('1 - уровень подъёма твелл (от 0 до 1)')
            print('2 - мощность турбины (от 0 до 1)')
            print('ВВЕДИТЕ НОМЕР ОПЕРАЦИИ: ')

            time.sleep(self.tick_time)

    def input_thread(self):
        while self.game:
            user_string = input()
            self.input_queue.put(user_string)

    def math_tread(self):
        while self.game:
            if self.game_reactor.step == 0:
                self.game_reactor.math_physics()
            time.sleep(self.tick_time)

    def start(self):
        math_thread = threading.Thread(target=self.math_tread, daemon=True)
        math_thread.start()

        time.sleep(0.2)
        input_thread = threading.Thread(target=self.input_thread, daemon=True)
        input_thread.start()

        while self.game:
            #self.engine.cls()
            self.draw_info(self.game_reactor)
            self.game_reactor.explosion()

            if not self.input_queue.empty():
                data = self.input_queue.get()
                if self.game_reactor.step == 0:
                    if data == '1':
                        self.game_reactor.step = 1
                        print('ВВЕДИТЕ ЗНАЧЕНИЕ (ОТ 0 ДО 1)')
                    if data == '2':
                        self.game_reactor.step = 2
                        print('ВВЕДИТЕ ЗНАЧЕНИЕ (ОТ 0 ДО 1)')
                elif self.game_reactor.step == 1:
                    self.game_reactor.height_kernel = float(data)
                    self.game_reactor.step = 0
                elif self.game_reactor.step == 2:
                    self.game_reactor.turbine_power = float(data)
                    self.game_reactor.step = 0

            time.sleep(tick_time)
