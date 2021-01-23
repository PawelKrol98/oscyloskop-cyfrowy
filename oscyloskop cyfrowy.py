#author Paweł Król

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button

fs = 900
vref = 5
resolution = 1024

def txtToList(filepath):
    list = []
    file = open(filepath, "r")
    for line in file:
        list.append(str.strip(line))  # str.strip() usuwa enter z końcu znaku
    file.close()
    return list

def hexToVoltage(hex):
    dec = int(hex, 16)
    return dec * vref/resolution

def setLimits():
    limits = input("Please enter the time range (in seconds) to display <t1 t2>,"
                   " 'close' to exit "
                   "or 'all' to display all data \n")
    if limits != "close" and limits !="all":
        try:
            limits = [float(limits.split()[0]), float(limits.split()[1])]
        except:
            print("Invalid input!")
            limits = "all"
    return limits

def click(event):
    x, y = event.xdata, event.ydata
    print(x,y)



data = txtToList("dane z przetwornika ADC.txt")
voltage = []
time = np.arange(0, len(data)/fs, 1/fs)
for d in data:
    voltage.append(hexToVoltage(d))
voltage = np.array(voltage)

frequency = np.linspace(0, fs - 1/len(time), len(time))
magnitude = np.absolute(np.fft.fft(voltage)) / len(voltage)

limits = setLimits()
while(limits != "close"):
    if limits == "all":
        fig = plt.figure(figsize=(8, 6))
        ax1 = fig.add_subplot(211)
        ax1.plot(time, voltage)
        ax2 = fig.add_subplot(212)
        ax2.plot(frequency, magnitude)
    else:
        startTime = limits[0]
        endTime = limits[1]
        startTimeIndex = np.absolute(time - startTime).argmin()
        endTimeIndex = np.absolute(time - endTime).argmin()
        voltageToDisplay = voltage[startTimeIndex : endTimeIndex + 1]
        timeToDisplay = time[startTimeIndex : endTimeIndex + 1]
        frequencyToDisplay = np.linspace(0, fs - 1/len(timeToDisplay), len(timeToDisplay))
        magnitudeToDisplay = np.absolute(np.fft.fft(voltageToDisplay)) / len(voltageToDisplay)
        fig = plt.figure(figsize=(8, 6))
        ax1 = fig.add_subplot(211)
        ax1.plot(timeToDisplay, voltageToDisplay)
        ax2 = fig.add_subplot(212)
        ax2.plot(frequencyToDisplay, magnitudeToDisplay)
    cursor1 = Cursor(ax1, useblit=True, color='red', linewidth=2)
    cursor2 = Cursor(ax2, useblit=True, color='red', linewidth=2)
    fig.canvas.mpl_connect('button_press_event', click)
    plt.show()
    voltage += 1
    limits = setLimits()
