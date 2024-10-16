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
# 0 ->CB_INC_NORMAL , 1->CB_P_INC, 2->CB_NON_INC_NORMAL, 3->CB_P_NON_INC, 4 ->TB_INC_NORMAL , 5->TB_P_INC, 6->TB_NONINC_NORMAL, 7->TB_P_NONINC ;;
# 6/7
# NORMAL; FRAG32(1); FRAG32(2); FRAG64(1); FRAG64(2);
fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"NWM TIME-BASED LATENCY 150K KEYS\nLOG SCALE")
fig.supylabel("")

axs[0][0].set_xscale('log')
axs[0][1].set_xscale('log')
axs[1][0].set_xscale('log')
axs[1][1].set_xscale('log')

boxes = [
    {
        'whislo': np.mean([19421]),    # Bottom whisker position
        'q1'    : np.mean([1832980]),    # First quartile (25th percentile)
        'med'   : np.mean([2117843]),    # Median         (50th percentile)
        'q3'    : np.mean([2400512]),    # Third quartile (75th percentile)
        'whishi': np.mean([4007706]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([108484]),    # Bottom whisker position 
        'q1'    : np.mean([13979187]),    # First quartile (25th percentile)
        'med'   : np.mean([23321937]),    # Median         (50th percentile)
        'q3'    : np.mean([28905079]),    # Third quartile (75th percentile)
        'whishi': np.mean([52446985]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([932024]),    # Bottom whisker position
        'q1'    : np.mean([21320011]),    # First quartile (25th percentile)
        'med'   : np.mean([31810678]),    # Median         (50th percentile)
        'q3'    : np.mean([54867964]),    # Third quartile (75th percentile)
        'whishi': np.mean([96310061]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([70767]),    # Bottom whisker position
        'q1'    : np.mean([2146583]),    # First quartile (25th percentile)
        'med'   : np.mean([4158484]),    # Median         (50th percentile)
        'q3'    : np.mean([6981662]),    # Third quartile (75th percentile)
        'whishi': np.mean([61507556]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([94097]),    # Bottom whisker position
        'q1'    : np.mean([14196380]),    # First quartile (25th percentile)
        'med'   : np.mean([23290852]),    # Median         (50th percentile)
        'q3'    : np.mean([28882992]),    # Third quartile (75th percentile)
        'whishi': np.mean([49802714]),    # Top whisker position
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
        'whislo': np.mean([21002]),    # Bottom whisker position
        'q1'    : np.mean([1559186]),    # First quartile (25th percentile)
        'med'   : np.mean([1813280]),    # Median         (50th percentile)
        'q3'    : np.mean([2069583]),    # Third quartile (75th percentile)
        'whishi': np.mean([4024127]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([81849]),    # Bottom whisker position
        'q1'    : np.mean([3049228]),    # First quartile (25th percentile)
        'med'   : np.mean([7052300]),    # Median         (50th percentile)
        'q3'    : np.mean([11141086]),    # Third quartile (75th percentile)
        'whishi': np.mean([61704876]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([103989]),    # Bottom whisker position
        'q1'    : np.mean([7764219]),    # First quartile (25th percentile)
        'med'   : np.mean([14287213]),    # Median         (50th percentile)
        'q3'    : np.mean([19843921]),    # Third quartile (75th percentile)
        'whishi': np.mean([72655307]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([17677]),    # Bottom whisker position
        'q1'    : np.mean([2268527]),    # First quartile (25th percentile)
        'med'   : np.mean([4391884]),    # Median         (50th percentile)
        'q3'    : np.mean([6485860]),    # Third quartile (75th percentile)
        'whishi': np.mean([61711507]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([55173]),    # Bottom whisker position
        'q1'    : np.mean([14255455]),    # First quartile (25th percentile)
        'med'   : np.mean([22244642]),    # Median         (50th percentile)
        'q3'    : np.mean([27158254]),    # Third quartile (75th percentile)
        'whishi': np.mean([45523365]),    # Top whisker position
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
        'whislo': np.mean([20903]),    # Bottom whisker position
        'q1'    : np.mean([1459975]),    # First quartile (25th percentile)
        'med'   : np.mean([1687295]),    # Median         (50th percentile)
        'q3'    : np.mean([1919710]),    # Third quartile (75th percentile)
        'whishi': np.mean([3581967]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([52495]),    # Bottom whisker position
        'q1'    : np.mean([5587968]),    # First quartile (25th percentile)
        'med'   : np.mean([12441458]),    # Median         (50th percentile)
        'q3'    : np.mean([19744021]),    # Third quartile (75th percentile)
        'whishi': np.mean([62011291]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([69010]),    # Bottom whisker position
        'q1'    : np.mean([7312751]),    # First quartile (25th percentile)
        'med'   : np.mean([13187969]),    # Median         (50th percentile)
        'q3'    : np.mean([21943941]),    # Third quartile (75th percentile)
        'whishi': np.mean([67677138]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([38172]),    # Bottom whisker position
        'q1'    : np.mean([2781290]),    # First quartile (25th percentile)
        'med'   : np.mean([5427612]),    # Median         (50th percentile)
        'q3'    : np.mean([8058777]),    # Third quartile (75th percentile)
        'whishi': np.mean([61071760]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([32739]),    # Bottom whisker position
        'q1'    : np.mean([13461949]),    # First quartile (25th percentile)
        'med'   : np.mean([22066974]),    # Median         (50th percentile)
        'q3'    : np.mean([26881099]),    # Third quartile (75th percentile)
        'whishi': np.mean([51974597]),    # Top whisker position
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
        'whislo': np.mean([33750]),    # Bottom whisker position
        'q1'    : np.mean([1847911]),    # First quartile (25th percentile)
        'med'   : np.mean([2128775]),    # Median         (50th percentile)
        'q3'    : np.mean([2425012]),    # Third quartile (75th percentile)
        'whishi': np.mean([4858639]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([64160]),    # Bottom whisker position
        'q1'    : np.mean([19395992]),    # First quartile (25th percentile)
        'med'   : np.mean([37459088]),    # Median         (50th percentile)
        'q3'    : np.mean([49364602]),    # Third quartile (75th percentile)
        'whishi': np.mean([63021648]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([291991]),    # Bottom whisker position
        'q1'    : np.mean([7402486]),    # First quartile (25th percentile)
        'med'   : np.mean([13387869]),    # Median         (50th percentile)
        'q3'    : np.mean([18899964]),    # Third quartile (75th percentile)
        'whishi': np.mean([65777675]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([234042]),    # Bottom whisker position
        'q1'    : np.mean([3143142]),    # First quartile (25th percentile)
        'med'   : np.mean([5908056]),    # Median         (50th percentile)
        'q3'    : np.mean([8436086]),    # Third quartile (75th percentile)
        'whishi': np.mean([61114782]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([18939]),    # Bottom whisker position
        'q1'    : np.mean([7927227]),    # First quartile (25th percentile)
        'med'   : np.mean([22587831]),    # Median         (50th percentile)
        'q3'    : np.mean([39203307]),    # Third quartile (75th percentile)
        'whishi': np.mean([59708464]),    # Top whisker position
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

fig.legend(labels=["IN-MEMORY", "PERSISTENT_FRAG32(1)", "PERSISTENT_FRAG64(1)", "PERSISTENT_FRAG32(2)", "PERSISTENT_FRAG64(2)"], loc='upper left')
plt.show()