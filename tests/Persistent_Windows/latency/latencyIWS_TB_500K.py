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
# 0 -> CB_INC_NORMAL , 1-> CB_P_INC, 2->CB_NON_INC_NORMAL, 3->CB_P_NON_INC, 4 ->TB_INC_NORMAL , 5-> TB_P_INC, 6->TB_NONINC_NORMAL, 7->TB_P_NONINC ;;
# 4/5
# NORMAL; PRIVATE(1); PRIVATE(2); SHARED(1); SHARED(2);
fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"IWS TIME-BASED LATENCY 500K KEYS\nLOG SCALE")
fig.supylabel("")

axs[0][0].set_xscale('log')
axs[0][1].set_xscale('log')
axs[1][0].set_xscale('log')
axs[1][1].set_xscale('log')

boxes = [
    {
        'whislo': np.mean([24066]),    # Bottom whisker position
        'q1'    : np.mean([1159563]),    # First quartile (25th percentile)
        'med'   : np.mean([2961250]),    # Median         (50th percentile)
        'q3'    : np.mean([5986338]),    # Third quartile (75th percentile)
        'whishi': np.mean([17987103]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([751990]),    # Bottom whisker position 
        'q1'    : np.mean([2590013]),    # First quartile (25th percentile)
        'med'   : np.mean([6738010]),    # Median         (50th percentile)
        'q3'    : np.mean([26003989]),    # Third quartile (75th percentile)
        'whishi': np.mean([54543999]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([404066]),    # Bottom whisker position
        'q1'    : np.mean([2770928]),    # First quartile (25th percentile)
        'med'   : np.mean([5130815]),    # Median         (50th percentile)
        'q3'    : np.mean([25939958]),    # Third quartile (75th percentile)
        'whishi': np.mean([78604811]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([309301]),    # Bottom whisker position
        'q1'    : np.mean([2125645]),    # First quartile (25th percentile)
        'med'   : np.mean([4745125]),    # Median         (50th percentile)
        'q3'    : np.mean([9414207]),    # Third quartile (75th percentile)
        'whishi': np.mean([62597893]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([310310]),    # Bottom whisker position
        'q1'    : np.mean([3782131]),    # First quartile (25th percentile)
        'med'   : np.mean([4381902]),    # Median         (50th percentile)
        'q3'    : np.mean([9414207]),    # Third quartile (75th percentile)
        'whishi': np.mean([62597893]),    # Top whisker position
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
        'whislo': np.mean([57201]),    # Bottom whisker position
        'q1'    : np.mean([1894184]),    # First quartile (25th percentile)
        'med'   : np.mean([3799636]),    # Median         (50th percentile)
        'q3'    : np.mean([5930923]),    # Third quartile (75th percentile)
        'whishi': np.mean([8319451]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([113819]),    # Bottom whisker position 
        'q1'    : np.mean([3347831]),    # First quartile (25th percentile)
        'med'   : np.mean([6281741]),    # Median         (50th percentile)
        'q3'    : np.mean([9873818]),    # Third quartile (75th percentile)
        'whishi': np.mean([69813881]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([107994]),    # Bottom whisker position
        'q1'    : np.mean([3599971]),    # First quartile (25th percentile)
        'med'   : np.mean([6438648]),    # Median         (50th percentile)
        'q3'    : np.mean([9303885]),    # Third quartile (75th percentile)
        'whishi': np.mean([70486330]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([192327]),    # Bottom whisker position
        'q1'    : np.mean([3495935]),    # First quartile (25th percentile)
        'med'   : np.mean([6910451]),    # Median         (50th percentile)
        'q3'    : np.mean([10621927]),    # Third quartile (75th percentile)
        'whishi': np.mean([70823835]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([203190]),    # Bottom whisker position
        'q1'    : np.mean([3458010]),    # First quartile (25th percentile)
        'med'   : np.mean([7875610]),    # Median         (50th percentile)
        'q3'    : np.mean([11238395]),    # Third quartile (75th percentile)
        'whishi': np.mean([74381919]),    # Top whisker position
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
        'whislo': np.mean([1980]),    # Bottom whisker position
        'q1'    : np.mean([625818]),    # First quartile (25th percentile)
        'med'   : np.mean([1161075]),    # Median         (50th percentile)
        'q3'    : np.mean([1682421]),    # Third quartile (75th percentile)
        'whishi': np.mean([5212769]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([34283]),    # Bottom whisker position 
        'q1'    : np.mean([3792100]),    # First quartile (25th percentile)
        'med'   : np.mean([7683199]),    # Median         (50th percentile)
        'q3'    : np.mean([15931003]),    # Third quartile (75th percentile)
        'whishi': np.mean([74910021]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([26305]),    # Bottom whisker position
        'q1'    : np.mean([3960032]),    # First quartile (25th percentile)
        'med'   : np.mean([7614465]),    # Median         (50th percentile)
        'q3'    : np.mean([11354222]),    # Third quartile (75th percentile)
        'whishi': np.mean([69768146]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([131934]),    # Bottom whisker position
        'q1'    : np.mean([6489290]),    # First quartile (25th percentile)
        'med'   : np.mean([9918319]),    # Median         (50th percentile)
        'q3'    : np.mean([15848031]),    # Third quartile (75th percentile)
        'whishi': np.mean([79182301]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([198312]),    # Bottom whisker position
        'q1'    : np.mean([7318913]),    # First quartile (25th percentile)
        'med'   : np.mean([10391002]),    # Median         (50th percentile)
        'q3'    : np.mean([19849102]),    # Third quartile (75th percentile)
        'whishi': np.mean([839123013]),    # Top whisker position
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
        'whislo': np.mean([1521]),    # Bottom whisker position
        'q1'    : np.mean([868370]),    # First quartile (25th percentile)
        'med'   : np.mean([1692856]),    # Median         (50th percentile)
        'q3'    : np.mean([2529161]),    # Third quartile (75th percentile)
        'whishi': np.mean([3468048]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([83120]),    # Bottom whisker position 
        'q1'    : np.mean([6319022]),    # First quartile (25th percentile)
        'med'   : np.mean([17419930]),    # Median         (50th percentile)
        'q3'    : np.mean([41838199]),    # Third quartile (75th percentile)
        'whishi': np.mean([933200722]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([74575]),    # Bottom whisker position
        'q1'    : np.mean([4815887]),    # First quartile (25th percentile)
        'med'   : np.mean([13320013]),    # Median         (50th percentile)
        'q3'    : np.mean([31273386]),    # Third quartile (75th percentile)
        'whishi': np.mean([62725726]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([163278]),    # Bottom whisker position
        'q1'    : np.mean([9516086]),    # First quartile (25th percentile)
        'med'   : np.mean([20459321]),    # Median         (50th percentile)
        'q3'    : np.mean([39498262]),    # Third quartile (75th percentile)
        'whishi': np.mean([64158717]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([173180]),    # Bottom whisker position
        'q1'    : np.mean([10391932]),    # First quartile (25th percentile)
        'med'   : np.mean([26310302]),    # Median         (50th percentile)
        'q3'    : np.mean([48301203]),    # Third quartile (75th percentile)
        'whishi': np.mean([1276891371]),    # Top whisker position
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