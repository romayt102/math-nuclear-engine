from settings import *

class Physics():
    def __init__(self):
        self.kernel_koef = kernel_reactivity_koef
        self.fuel_koef = fuel_temp_koef
        self.void_koef = void_steam_koef
        self.heat_koef = heat_koef
        self.t_env = environment_temp
        self.turbine_koef = turbine_koef

    def kernel_reactivity(self,height):
        return (height-0.5) * self.kernel_koef

    def temp_reactivity(self, t_old, t_base):
        delta_t = t_old - t_base

        fuel_effect = - (delta_t * self.fuel_koef)
        void_effect = delta_t * self.void_koef

        return fuel_effect + void_effect

    def all_reactivity(self, kernel_react,temp_react):
        return kernel_react-temp_react

    def new_power(self,all_react,old_power,tick):
        new_p = old_power * (1+all_react*tick)
        return max(0.1, new_p)

    def new_heat(self,new_p):
        return self.heat_koef*new_p

    def new_cooling(self, t_old, turbine_power):
        actual_cool_koef = turbine_power * self.turbine_koef
        return (t_old - self.t_env) * actual_cool_koef

    def new_temperature(self, t_old, q_heat, q_cool, tick):
        return t_old + (q_heat - q_cool) * tick