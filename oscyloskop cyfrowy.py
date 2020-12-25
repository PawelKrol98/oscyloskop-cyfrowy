#author Paweł Król

import numpy as np
import matplotlib.pyplot as plt

fs = 900
vref = 5
resolution = 1024

def txtToList(filepath):
    list = []
    file = open(filepath, "r")
    for line in file:
        list.append(str.strip(line))  # str.strip() usuwa enter z końcu znaku
    return list

def hexToVoltage(hex):
    dec = int(hex, 16)
    return dec * vref/resolution

data = txtToList("dane z przetwornika ADC.txt")
voltage = []
time = np.arange(0, len(data)/fs, 1/fs)
for d in data:
    voltage.append(hexToVoltage(d))
voltage = np.array(voltage)

plt.plot(voltage, time)
plt.show()
