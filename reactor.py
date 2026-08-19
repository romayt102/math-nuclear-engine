from physics import Physics
from settings import *
from engine import *

class Reactor():
    def __init__(self, game_controller):
        self.phys = Physics()
        self.engine = Engine()
        self.game_controller = game_controller

        self.kernel_react = 0
        self.temp_react = 0
        self.all_react = 0
        self.power = start_power
        self.new_heat = 0
        self.new_cooling = 0
        self.temperature = start_temperature
        self.height_kernel = start_height_kernel
        self.turbine_power = start_turbine_power

        self.max_power = max_power
        self.max_temperature = max_temperature

        self.ticks = tick
        self.tick_time = tick_time
        self.step = 0

    def math_physics(self):
        self.kernel_react = self.phys.kernel_reactivity(self.height_kernel)
        self.temp_react = self.phys.temp_reactivity(self.temperature)
        self.all_react = self.phys.all_reactivity(self.kernel_react, self.temp_react)
        self.power = self.phys.new_power(self.all_react, self.power)
        self.new_heat = self.phys.new_heat(self.power)
        self.new_cooling = self.phys.new_cooling(self.temperature, self.turbine_power)
        self.temperature = self.phys.new_temperature(self.temperature, self.new_heat, self.new_cooling)
        self.ticks += 1

    def explosion(self):
        if self.power > max_power:
            self.engine.cls()
            self.step = -1
            print('Произошла авария на ЧАЭС. Реактор РБМК-1000 разрушен. Активной зоны больше нет.')
            print(f'Мощность реактора: {self.power:.2f} ||| Максимально допустимая мощность реактора: {self.max_power:.2f}')
            print(
                f'Температура реактора: {self.temperature:.2f} ||| Максимально допустимая температура реактора: {self.max_temperature:.2f}')
            print(f'Колличество тиков: {self.ticks}')
            self.game_controller.set_game(False)
        elif self.temperature > max_temperature:
            self.engine.cls()
            self.step = -1
            print(
                'Произошла авария на ЧАЭС. Реактор РБМК-1000 разрушен. Давление пара разорвало технологические каналы и сорвало крышку реактора!')
            print(f'Мощность реактора: {self.power:.2f} ||| Максимально допустимая мощность реактора: {self.max_power:.2f}')
            print(
                f'Температура реактора: {self.temperature:.2f} ||| Максимально допустимая температура реактора: {self.max_temperature:.2f}')
            print(f'Колличество тиков: {self.ticks}')
            self.game_controller.set_game(False)