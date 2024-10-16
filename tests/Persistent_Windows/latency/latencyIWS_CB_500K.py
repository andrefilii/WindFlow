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
# 0/1
# NORMAL; PRIVATE(1); PRIVATE(2); SHARED(1); SHARED(2);
fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"IWS COUNT-BASED LATENCY 500K KEYS\nLOG SCALE")
fig.supylabel("")

axs[0][0].set_xscale('log')
axs[0][1].set_xscale('log')
axs[1][0].set_xscale('log')
axs[1][1].set_xscale('log')

boxes = [
    {
        'whislo': np.mean([57533]),    # Bottom whisker position
        'q1'    : np.mean([125792]),    # First quartile (25th percentile)
        'med'   : np.mean([187248]),    # Median         (50th percentile)
        'q3'    : np.mean([188075]),    # Third quartile (75th percentile)
        'whishi': np.mean([567977]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([751990]),    # Bottom whisker position 
        'q1'    : np.mean([1472002]),    # First quartile (25th percentile)
        'med'   : np.mean([2172005]),    # Median         (50th percentile)
        'q3'    : np.mean([26003989]),    # Third quartile (75th percentile)
        'whishi': np.mean([54543999]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([78960]),    # Bottom whisker position
        'q1'    : np.mean([134218]),    # First quartile (25th percentile)
        'med'   : np.mean([191051]),    # Median         (50th percentile)
        'q3'    : np.mean([248927]),    # Third quartile (75th percentile)
        'whishi': np.mean([8176951]),    # Top whisker position
        'fliers': []        # Outliers

    },{
        'whislo': np.mean([956075]),    # Bottom whisker position
        'q1'    : np.mean([1504018]),    # First quartile (25th percentile)
        'med'   : np.mean([2092024]),    # Median         (50th percentile)
        'q3'    : np.mean([7799994]),    # Third quartile (75th percentile)
        'whishi': np.mean([30188010]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([77475]),    # Bottom whisker position
        'q1'    : np.mean([126386]),    # First quartile (25th percentile)
        'med'   : np.mean([176988]),    # Median         (50th percentile)
        'q3'    : np.mean([226295]),    # Third quartile (75th percentile)
        'whishi': np.mean([7962468]),    # Top whisker position
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
        'whislo': np.mean([817]),    # Bottom whisker position
        'q1'    : np.mean([2739]),    # First quartile (25th percentile)
        'med'   : np.mean([5227]),    # Median         (50th percentile)
        'q3'    : np.mean([7247]),    # Third quartile (75th percentile)
        'whishi': np.mean([160753]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([39982]),    # Bottom whisker position 
        'q1'    : np.mean([540005]),    # First quartile (25th percentile)
        'med'   : np.mean([2679983]),    # Median         (50th percentile)
        'q3'    : np.mean([3847994]),    # Third quartile (75th percentile)
        'whishi': np.mean([24799980]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([946]),    # Bottom whisker position
        'q1'    : np.mean([104675]),    # First quartile (25th percentile)
        'med'   : np.mean([182231]),    # Median         (50th percentile)
        'q3'    : np.mean([274838]),    # Third quartile (75th percentile)
        'whishi': np.mean([4424243]),    # Top whisker position
        'fliers': []        # Outliers
    },{
                    'whislo': np.mean([44030]),    # Bottom whisker position
        'q1'    : np.mean([392028]),    # First quartile (25th percentile)
        'med'   : np.mean([2020011]),    # Median         (50th percentile)
        'q3'    : np.mean([2968015]),    # Third quartile (75th percentile)
        'whishi': np.mean([17328003]),    # Top whisker position
        'fliers': []        # Outliers

    },{
        'whislo': np.mean([36443]),    # Bottom whisker position
        'q1'    : np.mean([134783]),    # First quartile (25th percentile)
        'med'   : np.mean([188589]),    # Median         (50th percentile)
        'q3'    : np.mean([254745]),    # Third quartile (75th percentile)
        'whishi': np.mean([4125911]),    # Top whisker position
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
        'whislo': np.mean([673]),    # Bottom whisker position
        'q1'    : np.mean([2171]),    # First quartile (25th percentile)
        'med'   : np.mean([3484]),    # Median         (50th percentile)
        'q3'    : np.mean([7973]),    # Third quartile (75th percentile)
        'whishi': np.mean([111028]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([32283]),    # Bottom whisker position 
        'q1'    : np.mean([296133]),    # First quartile (25th percentile)
        'med'   : np.mean([580151]),    # Median         (50th percentile)
        'q3'    : np.mean([3261100]),    # Third quartile (75th percentile)
        'whishi': np.mean([14468174]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([842]),    # Bottom whisker position
        'q1'    : np.mean([138069]),    # First quartile (25th percentile)
        'med'   : np.mean([227301]),    # Median         (50th percentile)
        'q3'    : np.mean([305685]),    # Third quartile (75th percentile)
        'whishi': np.mean([2935080]),    # Top whisker position
        'fliers': []        # Outliers
    },{
                    'whislo': np.mean([43996]),    # Bottom whisker position
        'q1'    : np.mean([196077]),    # First quartile (25th percentile)
        'med'   : np.mean([383979]),    # Median         (50th percentile)
        'q3'    : np.mean([3091449]),    # Third quartile (75th percentile)
        'whishi': np.mean([13879996]),    # Top whisker position
        'fliers': []        # Outliers

    },{
        'whislo': np.mean([1204]),    # Bottom whisker position
        'q1'    : np.mean([147356]),    # First quartile (25th percentile)
        'med'   : np.mean([257717]),    # Median         (50th percentile)
        'q3'    : np.mean([332586]),    # Third quartile (75th percentile)
        'whishi': np.mean([2973300]),    # Top whisker position
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
        'whislo': np.mean([28]),    # Bottom whisker position
        'q1'    : np.mean([2433]),    # First quartile (25th percentile)
        'med'   : np.mean([3960]),    # Median         (50th percentile)
        'q3'    : np.mean([18436]),    # Third quartile (75th percentile)
        'whishi': np.mean([131586]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([183]),    # Bottom whisker position 
        'q1'    : np.mean([90694]),    # First quartile (25th percentile)
        'med'   : np.mean([219244]),    # Median         (50th percentile)
        'q3'    : np.mean([536078]),    # Third quartile (75th percentile)
        'whishi': np.mean([9332007]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([829]),    # Bottom whisker position
        'q1'    : np.mean([103517]),    # First quartile (25th percentile)
        'med'   : np.mean([186727]),    # Median         (50th percentile)
        'q3'    : np.mean([424177]),    # Third quartile (75th percentile)
        'whishi': np.mean([1958192]),    # Top whisker position
        'fliers': []        # Outliers
    },{
                    'whislo': np.mean([7995]),    # Bottom whisker position
        'q1'    : np.mean([224012]),    # First quartile (25th percentile)
        'med'   : np.mean([376152]),    # Median         (50th percentile)
        'q3'    : np.mean([767991]),    # Third quartile (75th percentile)
        'whishi': np.mean([10487996]),    # Top whisker position
        'fliers': []        # Outliers

    },{
        'whislo': np.mean([1144]),    # Bottom whisker position
        'q1'    : np.mean([75611]),    # First quartile (25th percentile)
        'med'   : np.mean([137966]),    # Median         (50th percentile)
        'q3'    : np.mean([204560]),    # Third quartile (75th percentile)
        'whishi': np.mean([1976891]),    # Top whisker position
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