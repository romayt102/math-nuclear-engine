class Physics():
    def __init__(self):
        pass

    def kernel_reactivity(self,height, koef):
        return (height-0.5) * koef

    def temp_reactivity(self, t_old, t_base, fuel_koef, void_koef):
        delta_t = t_old - t_base

        fuel_effect = - (delta_t * fuel_koef)
        void_effect = delta_t * void_koef

        return fuel_effect + void_effect

    def all_reactivity(self, kernel_react,temp_react):
        return kernel_react-temp_react

    def new_power(self,all_react,old_power,tick):
        new_p = old_power * (1+all_react*tick)
        return max(0.1, new_p)

    def new_heat(self,new_p,heat_koef):
        return heat_koef*new_p

    def new_cooling(self, t_old, t_env, turbine_power, turbine_koef):
        actual_cool_koef = turbine_power * turbine_koef
        return (t_old - t_env) * actual_cool_koef

    def new_temperature(self, t_old, q_heat, q_cool, tick):
        return t_old + (q_heat - q_cool) * tick