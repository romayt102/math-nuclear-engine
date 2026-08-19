import os
import threading
import time
import queue

from physics import Physics
from settings import *

phys = Physics()
ticks=0
step=0
game = True
input_queue = queue.Queue()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def initialization():
    global height_kernel; global temperature; global power; global turbine_power
    if ticks == 0:
        height_kernel = start_height_kernel
        turbine_power = start_turbine_power
        temperature = start_temperature
        power = start_power

def math_physics():
    global kernel_react; global temp_react; global all_react; global new_power; global new_heat; global new_cooling; global new_temp
    kernel_react = phys.kernel_reactivity(height_kernel)
    temp_react = phys.temp_reactivity(temperature, base_temperature)
    all_react = phys.all_reactivity(kernel_react, temp_react)
    new_power = phys.new_power(all_react, power, tick)
    new_heat = phys.new_heat(new_power)
    new_cooling = phys.new_cooling(temperature, environment_temp)
    new_temp = phys.new_temperature(temperature, new_heat, new_cooling, tick)

def update_values():
    global temperature; global power
    temperature = new_temp
    power = new_power

def draw_info():
    if step == 0:
        cls()
        print('=== АЭС СИМУЛЯТОР ===')
        print(f"Шаг симуляции (тик): {ticks}")
        print(f"Текущий уровень ТВЭЛ: {height_kernel}")
        print(f"Текущая мощность турбин: {turbine_power}")
        print('---------------------')
        print(f"Ядерная реактивность: {kernel_react:.2f}")
        print(f"Темп. реактивность:  {temp_react:.2f}")
        print(f"Общая реактивность:  {all_react:.2f}")
        print(f"Текущая мощность:    {new_power:.2f}")
        print(f"Выделение тепла:     {new_heat:.2f}")
        print(f"Охлаждение:          {new_cooling:.2f}")
        print(f"Новая температура:   {new_temp:.2f}")
        print('=====================')

        print('1 - уровень подъёма твелл (от 0 до 1)')
        print('2 - мощность турбины (от 0 до 1)')
        print('ВВЕДИТЕ НОМЕР ОПЕРАЦИИ: ')

def explosion():
    global game; global step
    if new_power > max_power:
        cls()
        step=-1
        print('Произошла авария на ЧАЭС. Реактор РБМК-1000 разрушен. Активной зоны больше нет.')
        print(f'Мощность реактора: {new_power:.2f} ||| Максимально допустимая мощность реактора: {max_power:.2f}')
        print(f'Температура реактора: {new_temp:.2f} ||| Максимально допустимая температура реактора: {max_temperature:.2f}')
        print(f'Колличество тиков: {ticks}')
        game = False
    elif new_temp > max_temperature:
        cls()
        step=-1
        print('Произошла авария на ЧАЭС. Реактор РБМК-1000 разрушен. Давление пара разорвало технологические каналы и сорвало крышку реактора!')
        print(f'Мощность реактора: {new_power:.2f} ||| Максимально допустимая мощность реактора: {max_power:.2f}')
        print(f'Температура реактора: {new_temp:.2f} ||| Максимально допустимая температура реактора: {max_temperature:.2f}')
        print(f'Колличество тиков: {ticks}')
        game = False


def math_tread():
    global ticks
    while game:
        if step == 0:
            math_physics()
            update_values()
            ticks+=1

        time.sleep(tick_time)

def input_sys():
    while game:
        user_string = input()
        input_queue.put(user_string)

initialization()

input_thread1 = threading.Thread(target=math_tread, daemon=True)
input_thread1.start()

time.sleep(0.2)
input_thread2 = threading.Thread(target=input_sys, daemon=True)
input_thread2.start()

while game:
    draw_info()
    explosion()

    if not input_queue.empty():
        data = input_queue.get()
        if step == 0:
            if data == '1':
                step = 1
                print('ВВЕДИТЕ ЗНАЧЕНИЕ (ОТ 0 ДО 1)')
            if data == '2':
                step = 2
                print('ВВЕДИТЕ ЗНАЧЕНИЕ (ОТ 0 ДО 1)')
        elif step == 1:
            height_kernel = float(data)
            step = 0
        elif step == 2:
            turbine_power = float(data)
            step = 0

    time.sleep(tick_time)