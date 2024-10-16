# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import random
BLUE = (76/255,114/255,176/255)
BLUE_LIGHT = (76/255,114/255,176/255)
PINK = (221/255,132/255,83/255)
ORANGE_LIGHT = (221/255,132/255,83/255)
GREEN = (85/255,168/255,104/255)
RED = (166/255,63/255,69/255)
PURPLE = (108/255,91/255,158/255)
KEYS = 150
sns.set_theme()
fig, axs = plt.subplots(ncols=2, nrows=2)
fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"NON INCREMENTAL WINDOW MEAN (NWM) COUNT-BASED 150K KEYS STATE RESIDENT MEMORY USAGE (RSS)", ha = "center")
fig.supxlabel("Time (seconds)")
fig.supylabel("MB Resident Memory")

_data = np.loadtxt(
    f"{KEYS}k/memory/0_{KEYS}000_1_mem.txt.dat", dtype="uint64")
__data = np.loadtxt(
    f"{KEYS}k/frag32(2)/0_{KEYS}000_1_mem.txt.dat", dtype="uint64")
___data = np.loadtxt(
    f"{KEYS}k/frag64(2)/0_{KEYS}000_1_mem.txt.dat", dtype="uint64")

_data = [(i/1024) for i in _data]
__data = [(i/1024) for i in __data]
___data = [(i/1024) for i in ___data]
_dataf = list(filter(lambda x: x > 0, _data))
__dataf = list(filter(lambda x: x > 0, __data))
___dataf = list(filter(lambda x: x > 0, ___data))
_datac = []
__datac = []
___datac = []

mymin = min(len(_dataf),len(__dataf),len(___dataf))
for i in range(0, mymin, 1):
    _datac.append(_dataf[i])
    __datac.append(__dataf[i])
    ___datac.append(___dataf[i])
xs = [*range(1, mymin + 1, 1)]
axs[0, 0].plot(xs, _datac, color=BLUE, linewidth=2)
axs[0, 0].plot(xs, __datac, color=PINK, linewidth=2)
axs[0, 0].plot(xs, ___datac, color=GREEN, linewidth=2)
axs[0, 0].set_title("PARALLELISM 1 1 1 1")

_data = np.loadtxt(
    f"{KEYS}k/memory/0_{KEYS}000_2_mem.txt.dat", dtype="uint64")
__data = np.loadtxt(
    f"{KEYS}k/frag32(2)/0_{KEYS}000_2_mem.txt.dat", dtype="uint64")
___data = np.loadtxt(
    f"{KEYS}k/frag64(2)/0_{KEYS}000_2_mem.txt.dat", dtype="uint64")
_data = [(i/1024) for i in _data]
__data = [(i/1024) for i in __data]
___data = [(i/1024) for i in ___data]
_dataf = list(filter(lambda x: x > 0, _data))
__dataf = list(filter(lambda x: x > 0, __data))
___dataf = list(filter(lambda x: x > 0, ___data))
_datac = []
__datac = []
___datac = []

mymin = min(len(_dataf),len(__dataf),len(___dataf))
for i in range(0, mymin, 1):
    _datac.append(_dataf[i])
    __datac.append(__dataf[i])
    ___datac.append(___dataf[i])
xs = [*range(1, mymin + 1, 1)]
axs[0, 1].plot(xs, _datac, color=BLUE, linewidth=2)
axs[0, 1].plot(xs, __datac, color=PINK, linewidth=2)
axs[0, 1].plot(xs, ___datac, color=GREEN, linewidth=2)
axs[0, 1].set_title("PARALLELISM 2 2 2 2")

_data = np.loadtxt(
    f"{KEYS}k/memory/0_{KEYS}000_3_mem.txt.dat", dtype="uint64")
__data = np.loadtxt(
    f"{KEYS}k/frag32(2)/0_{KEYS}000_3_mem.txt.dat", dtype="uint64")
___data = np.loadtxt(
    f"{KEYS}k/frag64(2)/0_{KEYS}000_3_mem.txt.dat", dtype="uint64")
_data = [(i/1024) for i in _data]
__data = [(i/1024) for i in __data]
___data = [(i/1024) for i in ___data]
_dataf = list(filter(lambda x: x > 0, _data))
__dataf = list(filter(lambda x: x > 0, __data))
___dataf = list(filter(lambda x: x > 0, ___data))
_datac = []
__datac = []
___datac = []

mymin = min(len(_dataf),len(__dataf),len(___dataf))
for i in range(0, mymin, 1):
    _datac.append(_dataf[i])
    __datac.append(__dataf[i])
    ___datac.append(___dataf[i])
xs = [*range(1, mymin + 1, 1)]
axs[1, 0].plot(xs, _datac, color=BLUE, linewidth=2)
axs[1, 0].plot(xs, __datac, color=PINK, linewidth=2)
axs[1, 0].plot(xs, ___datac, color=GREEN, linewidth=2)
axs[1, 0].set_title("PARALLELISM 3 3 3 3")

_data = np.loadtxt(
    f"{KEYS}k/memory/0_{KEYS}000_5_mem.txt.dat", dtype="uint64")
__data = np.loadtxt(
    f"{KEYS}k/frag32(2)/0_{KEYS}000_5_mem.txt.dat", dtype="uint64")
___data = np.loadtxt(
    f"{KEYS}k/frag64(2)/0_{KEYS}000_5_mem.txt.dat", dtype="uint64")
_data = [(i/1024) for i in _data]
__data = [(i/1024) for i in __data]
___data = [(i/1024) for i in ___data]
_dataf = list(filter(lambda x: x > 0, _data))
__dataf = list(filter(lambda x: x > 0, __data))
___dataf = list(filter(lambda x: x > 0, ___data))
_datac = []
__datac = []
___datac = []

mymin = min(len(_dataf),len(__dataf),len(___dataf))
for i in range(0, mymin, 1):
    _datac.append(_dataf[i])
    __datac.append(__dataf[i])
    ___datac.append(___dataf[i])
xs = [*range(1, mymin + 1, 1)]
axs[1, 1].plot(xs, _datac, color=BLUE, linewidth=2)
axs[1, 1].plot(xs, __datac, color=PINK, linewidth=2)
axs[1, 1].plot(xs, ___datac, color=GREEN, linewidth=2)
axs[1, 1].set_title("PARALLELISM 5 5 5 5")
fig.legend(labels=["IN-MEMORY", "PERSISTENT_FRAG32(2)", "PERSISTENT_FRAG64(2)"], loc='upper left')


plt.show()
