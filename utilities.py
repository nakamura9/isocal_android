'''
Created on Apr 20, 2016

@author: caleb kandoro
'''


def calculate_pressure_psi(weight):
    weight = float(weight)
    return (weight/45.19)+5.0150254481


def calculate_pressure_bar(weight):
    weight = float(weight)
    return calculate_pressure_psi(weight) / 14.4038
    

        
def calculate_pressure_kpa(weight):
    weight = float(weight)
    return calculate_pressure_bar(weight) * 100
    
def calculate_pressure_mpa(weight):
    val = calculate_pressure_bar(weight) / 10
    return val
    
def calculate_pressure_pa(weight):
    return calculate_pressure_bar(weight) / 100000

