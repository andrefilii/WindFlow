# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
BLUE = "#3D85F7"
BLUE_LIGHT = "#5490FF"
PINK = "#C32E5A"
PINK_LIGHT = "#D34068"
GREY40 = "#666666"
GREY25 = "#404040"
GREY20 = "#333333"
BACKGROUND = "#F5F4EF"
sns.set_theme()
fig, axs = plt.subplots(ncols=2,nrows=2,sharey=False,sharex=False)
# 0 -> CB_INC_NORMAL , 1-> CB_P_INC, 2->CB_NON_INC_NORMAL, 3->CB_P_NON_INC, 4 -> TB_INC_NORMAL , 5-> TB_P_INC, 6->TB_NONINC_NORMAL, 7->TB_P_NONINC ;;
# 4/5
# NORMAL; PRIVATE(1); PRIVATE(2); SHARED(1); SHARED(2);
fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"IWS TIME-BASED LATENCY 1M KEYS\nLOG SCALE")
fig.supylabel("")

axs[0][0].set_xscale('log')
axs[0][1].set_xscale('log')
axs[1][0].set_xscale('log')
axs[1][1].set_xscale('log')

boxes = [
    {
        'whislo': np.mean([3156]),    # Bottom whisker position
        'q1'    : np.mean([93544]),    # First quartile (25th percentile)
        'med'   : np.mean([363730]),    # Median         (50th percentile)
        'q3'    : np.mean([956120]),    # Third quartile (75th percentile)
        'whishi': np.mean([8407679]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([412919]),    # Bottom whisker position
        'q1'    : np.mean([1453865]),    # First quartile (25th percentile)
        'med'   : np.mean([2426016]),    # Median         (50th percentile)
        'q3'    : np.mean([9008079]),    # Third quartile (75th percentile)
        'whishi': np.mean([75039985]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([763177]),    # Bottom whisker position
        'q1'    : np.mean([1738192]),    # First quartile (25th percentile)
        'med'   : np.mean([3812913]),    # Median         (50th percentile)
        'q3'    : np.mean([10319380]),    # Third quartile (75th percentile)
        'whishi': np.mean([791823718]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([423918]),    # Bottom whisker position
        'q1'    : np.mean([1584910]),    # First quartile (25th percentile)
        'med'   : np.mean([2531783]),    # Median         (50th percentile)
        'q3'    : np.mean([10823193]),    # Third quartile (75th percentile)
        'whishi': np.mean([66491743]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([594819]),    # Bottom whisker position
        'q1'    : np.mean([1482138]),    # First quartile (25th percentile)
        'med'   : np.mean([2498310]),    # Median         (50th percentile)
        'q3'    : np.mean([12371828]),    # Third quartile (75th percentile)
        'whishi': np.mean([723719382]),    # Top whisker position
        'fliers': []        # Outliers
    }

]
bx = axs[0][0].bxp(boxes,patch_artist=True,vert=False)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bx[element], color='black', alpha = 0.5)

axs[0][0].set_title("PARALLELISM 1,1,1,1")
axs[0][0].set_yticks([r for r in range(len([1,2,3,4,5]))],
                  ['', '', '', '', ''])

bx['boxes'][0].set(facecolor = (76/255,114/255,176/255), alpha = 1)
bx['boxes'][1].set(facecolor = (221/255,132/255,83/255),alpha = 1)
bx['boxes'][2].set(facecolor = (85/255,168/255,104/255),alpha = 1)
bx['boxes'][3].set(facecolor = (196/255,77/255,82/255), alpha = 1)
bx['boxes'][4].set(facecolor = (130/255,113/255,178/255), alpha = 1)


boxes = [
    {
        'whislo': np.mean([4627]),    # Bottom whisker position
        'q1'    : np.mean([694858]),    # First quartile (25th percentile)
        'med'   : np.mean([972833]),    # Median         (50th percentile)
        'q3'    : np.mean([1579991]),    # Third quartile (75th percentile)
        'whishi': np.mean([8183071]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([291687]),    # Bottom whisker position
        'q1'    : np.mean([1207846]),    # First quartile (25th percentile)
        'med'   : np.mean([2067416]),    # Median         (50th percentile)
        'q3'    : np.mean([3008484]),    # Third quartile (75th percentile)
        'whishi': np.mean([65683989]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([391030]),    # Bottom whisker position
        'q1'    : np.mean([1438192]),    # First quartile (25th percentile)
        'med'   : np.mean([2319300]),    # Median         (50th percentile)
        'q3'    : np.mean([3182399]),    # Third quartile (75th percentile)
        'whishi': np.mean([73182739]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([291687]),    # Bottom whisker position
        'q1'    : np.mean([1207846]),    # First quartile (25th percentile)
        'med'   : np.mean([2067416]),    # Median         (50th percentile)
        'q3'    : np.mean([3008484]),    # Third quartile (75th percentile)
        'whishi': np.mean([69213899]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([352819]),    # Bottom whisker position
        'q1'    : np.mean([1983919]),    # First quartile (25th percentile)
        'med'   : np.mean([2837188]),    # Median         (50th percentile)
        'q3'    : np.mean([3781238]),    # Third quartile (75th percentile)
        'whishi': np.mean([71839139]),    # Top whisker position
        'fliers': []        # Outliers
    }

]
bx = axs[0][1].bxp(boxes,patch_artist=True,vert=False)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bx[element], color='black', alpha = 0.5)

axs[0][1].set_title("PARALLELISM 2,2,2,2")
axs[0][1].set_yticks([r for r in range(len([1,2,3,4,5]))],
                  ['', '', '', '', ''])

bx['boxes'][0].set(facecolor = (76/255,114/255,176/255), alpha = 1)
bx['boxes'][1].set(facecolor = (221/255,132/255,83/255),alpha = 1)
bx['boxes'][2].set(facecolor = (85/255,168/255,104/255),alpha = 1)
bx['boxes'][3].set(facecolor = (196/255,77/255,82/255), alpha = 1)
bx['boxes'][4].set(facecolor = (130/255,113/255,178/255), alpha = 1)


boxes = [
    {
        'whislo': np.mean([17627]),    # Bottom whisker position
        'q1'    : np.mean([259141]),    # First quartile (25th percentile)
        'med'   : np.mean([485753]),    # Median         (50th percentile)
        'q3'    : np.mean([960218]),    # Third quartile (75th percentile)
        'whishi': np.mean([6022690]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([40787]),    # Bottom whisker position
        'q1'    : np.mean([2206722]),    # First quartile (25th percentile)
        'med'   : np.mean([4092640]),    # Median         (50th percentile)
        'q3'    : np.mean([6040087]),    # Third quartile (75th percentile)
        'whishi': np.mean([65534039]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([58391]),    # Bottom whisker position
        'q1'    : np.mean([2583190]),    # First quartile (25th percentile)
        'med'   : np.mean([4283919]),    # Median         (50th percentile)
        'q3'    : np.mean([7291901]),    # Third quartile (75th percentile)
        'whishi': np.mean([69182381]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([79123]),    # Bottom whisker position
        'q1'    : np.mean([4931901]),    # First quartile (25th percentile)
        'med'   : np.mean([7921010]),    # Median         (50th percentile)
        'q3'    : np.mean([9182381]),    # Third quartile (75th percentile)
        'whishi': np.mean([81827389]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([78183]),    # Bottom whisker position
        'q1'    : np.mean([4589219]),    # First quartile (25th percentile)
        'med'   : np.mean([6981923]),    # Median         (50th percentile)
        'q3'    : np.mean([8321838]),    # Third quartile (75th percentile)
        'whishi': np.mean([75617318]),    # Top whisker position
        'fliers': []        # Outliers
    }

]
bx = axs[1][0].bxp(boxes,patch_artist=True,vert=False)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bx[element], color='black', alpha = 0.5)

axs[1][0].set_title("PARALLELISM 3,3,3,3")
axs[1][0].set_yticks([r for r in range(len([1,2,3,4,5]))],
                  ['', '', '', '', ''])

bx['boxes'][0].set(facecolor = (76/255,114/255,176/255), alpha = 1)
bx['boxes'][1].set(facecolor = (221/255,132/255,83/255),alpha = 1)
bx['boxes'][2].set(facecolor = (85/255,168/255,104/255),alpha = 1)
bx['boxes'][3].set(facecolor = (196/255,77/255,82/255), alpha = 1)
bx['boxes'][4].set(facecolor = (130/255,113/255,178/255), alpha = 1)


boxes = [
    {
        'whislo': np.mean([6091]),    # Bottom whisker position
        'q1'    : np.mean([183175]),    # First quartile (25th percentile)
        'med'   : np.mean([376106]),    # Median         (50th percentile)
        'q3'    : np.mean([792947]),    # Third quartile (75th percentile)
        'whishi': np.mean([5479008]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([34390]),    # Bottom whisker position
        'q1'    : np.mean([2407352]),    # First quartile (25th percentile)
        'med'   : np.mean([4661315]),    # Median         (50th percentile)
        'q3'    : np.mean([6995220]),    # Third quartile (75th percentile)
        'whishi': np.mean([63034752]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([31930]),    # Bottom whisker position
        'q1'    : np.mean([2283912]),    # First quartile (25th percentile)
        'med'   : np.mean([4391839]),    # Median         (50th percentile)
        'q3'    : np.mean([6589410]),    # Third quartile (75th percentile)
        'whishi': np.mean([60910393]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([69381]),    # Bottom whisker position
        'q1'    : np.mean([3743194]),    # First quartile (25th percentile)
        'med'   : np.mean([8319037]),    # Median         (50th percentile)
        'q3'    : np.mean([10931092]),    # Third quartile (75th percentile)
        'whishi': np.mean([783193991]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([67312]),    # Bottom whisker position
        'q1'    : np.mean([3583912]),    # First quartile (25th percentile)
        'med'   : np.mean([8391020]),    # Median         (50th percentile)
        'q3'    : np.mean([9823883]),    # Third quartile (75th percentile)
        'whishi': np.mean([76923189]),    # Top whisker position
        'fliers': []        # Outliers
    }

]
bx = axs[1][1].bxp(boxes,patch_artist=True,vert=False)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bx[element], color='black', alpha = 0.5)

axs[1][1].set_title("PARALLELISM 5,5,5,5")
axs[1][1].set_yticks([r for r in range(len([1,2,3,4,5]))],
                  ['', '', '', '', ''])

bx['boxes'][0].set(facecolor = (76/255,114/255,176/255), alpha = 1)
bx['boxes'][1].set(facecolor = (221/255,132/255,83/255),alpha = 1)
bx['boxes'][2].set(facecolor = (85/255,168/255,104/255),alpha = 1)
bx['boxes'][3].set(facecolor = (196/255,77/255,82/255), alpha = 1)
bx['boxes'][4].set(facecolor = (130/255,113/255,178/255), alpha = 1)

fig.align_labels()
fig.supxlabel("Latency (microseconds)")

fig.legend(labels=["IN-MEMORY", "PERSISTENT_PRIVATE(1)", "PERSISTENT_PRIVATE(2)", "PERSISTENT_SHARED(1)", "PERSISTENT_SHARED(2)"], loc='upper left')
plt.show()