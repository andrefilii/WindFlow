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
# 2/3
# NORMAL; FRAG32(1); FRAG32(2); FRAG64(1); FRAG64(2);
fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"NWM COUNT-BASED LATENCY 300K KEYS\nLOG SCALE")
fig.supylabel("")

axs[0][0].set_xscale('log')
axs[0][1].set_xscale('log')
axs[1][0].set_xscale('log')
axs[1][1].set_xscale('log')

boxes = [
    {
        'whislo': np.mean([5125]),    # Bottom whisker position
        'q1'    : np.mean([12879]),    # First quartile (25th percentile)
        'med'   : np.mean([20669]),    # Median         (50th percentile)
        'q3'    : np.mean([28942]),    # Third quartile (75th percentile)
        'whishi': np.mean([710516]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([68326]),    # Bottom whisker position 
        'q1'    : np.mean([121694]),    # First quartile (25th percentile)
        'med'   : np.mean([175511]),    # Median         (50th percentile)
        'q3'    : np.mean([229956]),    # Third quartile (75th percentile)
        'whishi': np.mean([5195529]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([67843]),    # Bottom whisker position
        'q1'    : np.mean([119290]),    # First quartile (25th percentile)
        'med'   : np.mean([169914]),    # Median         (50th percentile)
        'q3'    : np.mean([222501]),    # Third quartile (75th percentile)
        'whishi': np.mean([5008000]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([68398]),    # Bottom whisker position
        'q1'    : np.mean([122207]),    # First quartile (25th percentile)
        'med'   : np.mean([176548]),    # Median         (50th percentile)
        'q3'    : np.mean([231701]),    # Third quartile (75th percentile)
        'whishi': np.mean([5235092]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([59782]),    # Bottom whisker position
        'q1'    : np.mean([106189]),    # First quartile (25th percentile)
        'med'   : np.mean([153082]),    # Median         (50th percentile)
        'q3'    : np.mean([199957]),    # Third quartile (75th percentile)
        'whishi': np.mean([4559334]),    # Top whisker position
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
        'whislo': np.mean([2304]),    # Bottom whisker position
        'q1'    : np.mean([10358]),    # First quartile (25th percentile)
        'med'   : np.mean([14869]),    # Median         (50th percentile)
        'q3'    : np.mean([19374]),    # Third quartile (75th percentile)
        'whishi': np.mean([920741]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([1178]),    # Bottom whisker position 
        'q1'    : np.mean([57713]),    # First quartile (25th percentile)
        'med'   : np.mean([147828]),    # Median         (50th percentile)
        'q3'    : np.mean([206872]),    # Third quartile (75th percentile)
        'whishi': np.mean([3230178]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([113950]),    # Bottom whisker position
        'q1'    : np.mean([155139]),    # First quartile (25th percentile)
        'med'   : np.mean([182922]),    # Median         (50th percentile)
        'q3'    : np.mean([211027]),    # Third quartile (75th percentile)
        'whishi': np.mean([3125150]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([143843]),    # Bottom whisker position
        'q1'    : np.mean([172409]),    # First quartile (25th percentile)
        'med'   : np.mean([200980]),    # Median         (50th percentile)
        'q3'    : np.mean([229639]),    # Third quartile (75th percentile)
        'whishi': np.mean([2995915]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([4188]),    # Bottom whisker position
        'q1'    : np.mean([50237]),    # First quartile (25th percentile)
        'med'   : np.mean([131484]),    # Median         (50th percentile)
        'q3'    : np.mean([180848]),    # Third quartile (75th percentile)
        'whishi': np.mean([2694739]),    # Top whisker position
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
        'whislo': np.mean([956]),    # Bottom whisker position
        'q1'    : np.mean([27402]),    # First quartile (25th percentile)
        'med'   : np.mean([47197]),    # Median         (50th percentile)
        'q3'    : np.mean([66434]),    # Third quartile (75th percentile)
        'whishi': np.mean([1051025]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([1854]),    # Bottom whisker position 
        'q1'    : np.mean([104771]),    # First quartile (25th percentile)
        'med'   : np.mean([214003]),    # Median         (50th percentile)
        'q3'    : np.mean([302550]),    # Third quartile (75th percentile)
        'whishi': np.mean([2882299]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([985]),    # Bottom whisker position
        'q1'    : np.mean([130468]),    # First quartile (25th percentile)
        'med'   : np.mean([228978]),    # Median         (50th percentile)
        'q3'    : np.mean([317240]),    # Third quartile (75th percentile)
        'whishi': np.mean([2855562]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([192068]),    # Bottom whisker position
        'q1'    : np.mean([251904]),    # First quartile (25th percentile)
        'med'   : np.mean([311349]),    # Median         (50th percentile)
        'q3'    : np.mean([369185]),    # Third quartile (75th percentile)
        'whishi': np.mean([2178070]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([8385]),    # Bottom whisker position
        'q1'    : np.mean([182302]),    # First quartile (25th percentile)
        'med'   : np.mean([266903]),    # Median         (50th percentile)
        'q3'    : np.mean([347580]),    # Third quartile (75th percentile)
        'whishi': np.mean([2097153]),    # Top whisker position
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
        'whislo': np.mean([83]),    # Bottom whisker position
        'q1'    : np.mean([22777]),    # First quartile (25th percentile)
        'med'   : np.mean([42575]),    # Median         (50th percentile)
        'q3'    : np.mean([62544]),    # Third quartile (75th percentile)
        'whishi': np.mean([1021610]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([1762]),    # Bottom whisker position 
        'q1'    : np.mean([163430]),    # First quartile (25th percentile)
        'med'   : np.mean([324643]),    # Median         (50th percentile)
        'q3'    : np.mean([477181]),    # Third quartile (75th percentile)
        'whishi': np.mean([2431207]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([311]),    # Bottom whisker position
        'q1'    : np.mean([242142]),    # First quartile (25th percentile)
        'med'   : np.mean([397359]),    # Median         (50th percentile)
        'q3'    : np.mean([562817]),    # Third quartile (75th percentile)
        'whishi': np.mean([2491192]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([4148]),    # Bottom whisker position
        'q1'    : np.mean([130872]),    # First quartile (25th percentile)
        'med'   : np.mean([264395]),    # Median         (50th percentile)
        'q3'    : np.mean([460756]),    # Third quartile (75th percentile)
        'whishi': np.mean([2090477]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([598]),    # Bottom whisker position
        'q1'    : np.mean([122464]),    # First quartile (25th percentile)
        'med'   : np.mean([258507]),    # Median         (50th percentile)
        'q3'    : np.mean([423382]),    # Third quartile (75th percentile)
        'whishi': np.mean([2090176]),    # Top whisker position
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