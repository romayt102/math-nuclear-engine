import pygame as pg
pg.init()

kernel_reactivity_koef=0.1

base_temperature = 284.0
fuel_temp_koef = 0.00002
void_steam_koef = 0.00005

tick=1
tick_time = 0.1
min_power = 0.1

heat_koef = 0.00825

environment_temp =20.0
turbine_koef = 0.2

start_power = 0.0
start_temperature = 0.0
start_height_kernel = 0.5
start_turbine_power = 0.0

max_temperature = 350.0
max_power=4000.0

WIDTH=1280
HEIGHT=720
name_font = pg.font.SysFont("Arial", 30)
parametrs_font = pg.font.SysFont("Arial", 25)