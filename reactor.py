from physics import Physics
from settings import *

class Reactor():
    def __init__(self):
        self.phys = Physics()

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

    def math_physics(self):
        self.power, self.temperature = self.phys.step_rk4(self.power,self.temperature,self.height_kernel,self.turbine_power,self.tick_time)
        self.kernel_react = self.phys.kernel_reactivity(self.height_kernel)
        self.temp_react = self.phys.temp_reactivity(self.temperature)
        self.all_react = self.phys.all_reactivity(self.kernel_react, self.temp_react)
        self.new_heat = self.phys.new_heat(self.power)
        self.new_cooling = self.phys.new_cooling(self.temperature, self.turbine_power)

        self.ticks += 1

    def explosion(self):
        if self.power > max_power:
            return 'MAX_POWER_EXP'
        if self.temperature > max_temperature:
            return 'MAX_TEMP_EXP'