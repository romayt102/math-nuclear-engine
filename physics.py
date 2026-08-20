from settings import *

class Physics():
    def __init__(self):
        self.kernel_koef = kernel_reactivity_koef
        self.fuel_koef = fuel_temp_koef
        self.void_koef = void_steam_koef
        self.heat_koef = heat_koef
        self.t_env = environment_temp
        self.turbine_koef = turbine_koef
        self.base_temperature = base_temperature
        self.base_cooling = base_cooling
        self.tick = tick

    def kernel_reactivity(self,height):
        return (height-0.5) * self.kernel_koef

    def temp_reactivity(self, t_old):
        delta_t = t_old - self.base_temperature

        fuel_effect = - (delta_t * self.fuel_koef)
        if t_old < self.base_temperature:
            void_effect = 0
        else:
            void_effect = delta_t * self.void_koef

        return fuel_effect + void_effect

    def all_reactivity(self, kernel_react,temp_react):
        return kernel_react+temp_react

    def new_heat(self,new_p):
        return self.heat_koef*new_p

    def new_cooling(self, t_old, turbine_power):
        actual_cool_koef = self.base_cooling + (turbine_power * self.turbine_koef)
        return (t_old - self.t_env) * actual_cool_koef

    def derivatives(self,power, temperature, height, turbine):
        kernel_react = self.kernel_reactivity(height)
        temp_react = self.temp_reactivity(temperature)
        all_react = self.all_reactivity(kernel_react,temp_react)
        dP_dt = power * all_react

        heat = self.new_heat(power)
        cooling = self.new_cooling(temperature,turbine)
        dT_dt = heat - cooling

        return (dP_dt, dT_dt)

    def step_rk4(self,power, temperature, height, turbine, dt):
        k1_power, k1_temp = self.derivatives(power, temperature, height, turbine)
        k2_power, k2_temp = self.derivatives(power + k1_power * dt/2, temperature + k1_temp * dt/2, height, turbine)
        k3_power, k3_temp = self.derivatives(power + k2_power * dt / 2, temperature + k2_temp * dt / 2, height, turbine)
        k4_power, k4_temp = self.derivatives(power + k3_power * dt, temperature + k3_temp * dt, height, turbine)

        new_power = power + (dt / 6) * (k1_power + 2 * k2_power + 2 * k3_power + k4_power)
        new_temp = temperature + (dt / 6) * (k1_temp + 2 * k2_temp + 2 * k3_temp + k4_temp)

        return new_power, new_temp