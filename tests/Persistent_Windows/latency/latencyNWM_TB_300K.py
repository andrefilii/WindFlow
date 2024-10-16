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

fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"NWM TIME-BASED LATENCY 300K KEYS\nLOG SCALE")
fig.supylabel("")

axs[0][0].set_xscale('log')
axs[0][1].set_xscale('log')
axs[1][0].set_xscale('log')
axs[1][1].set_xscale('log')

boxes = [
    {
        'whislo': np.mean([6349]),    # Bottom whisker position
        'q1'    : np.mean([1986029]),    # First quartile (25th percentile)
        'med'   : np.mean([2481273]),    # Median         (50th percentile)
        'q3'    : np.mean([2973562]),    # Third quartile (75th percentile)
        'whishi': np.mean([6896198]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([114397]),    # Bottom whisker position
        'q1'    : np.mean([13407847]),    # First quartile (25th percentile)
        'med'   : np.mean([22436198]),    # Median         (50th percentile)
        'q3'    : np.mean([30098639]),    # Third quartile (75th percentile)
        'whishi': np.mean([61190127]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([528168]),    # Bottom whisker position
        'q1'    : np.mean([2012067]),    # First quartile (25th percentile)
        'med'   : np.mean([24820017]),    # Median         (50th percentile)
        'q3'    : np.mean([36500013]),    # Third quartile (75th percentile)
        'whishi': np.mean([70754839]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([900173]),    # Bottom whisker position
        'q1'    : np.mean([9332040]),    # First quartile (25th percentile)
        'med'   : np.mean([14716949]),    # Median         (50th percentile)
        'q3'    : np.mean([50308115]),    # Third quartile (75th percentile)
        'whishi': np.mean([94960156]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([429066]),    # Bottom whisker position
        'q1'    : np.mean([4145654]),    # First quartile (25th percentile)
        'med'   : np.mean([7996882]),    # Median         (50th percentile)
        'q3'    : np.mean([11808126]),    # Third quartile (75th percentile)
        'whishi': np.mean([76120757]),    # Top whisker position
        'fliers': []        # Outliers
    }

]
bx = axs[0][0].bxp(boxes,patch_artist=True,vert=False)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bx[element], color='black', alpha = 0.5)

axs[0][0].set_title("PARALLELISM 1,1,1")
axs[0][0].set_yticks([r for r in range(len([1,2,3,4,5]))],
                  ['', '', '', '', ''])

bx['boxes'][0].set(facecolor = (76/255,114/255,176/255), alpha = 1)
bx['boxes'][1].set(facecolor = (221/255,132/255,83/255),alpha = 1)
bx['boxes'][2].set(facecolor = (85/255,168/255,104/255),alpha = 1)
bx['boxes'][3].set(facecolor = (196/255,77/255,82/255), alpha = 1)
bx['boxes'][4].set(facecolor = (130/255,113/255,178/255), alpha = 1)


boxes = [
    {
        'whislo': np.mean([946]),    # Bottom whisker position
        'q1'    : np.mean([1442106]),    # First quartile (25th percentile)
        'med'   : np.mean([1819759]),    # Median         (50th percentile)
        'q3'    : np.mean([2192417]),    # Third quartile (75th percentile)
        'whishi': np.mean([5646298]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([297441]),    # Bottom whisker position
        'q1'    : np.mean([13265146]),    # First quartile (25th percentile)
        'med'   : np.mean([21335593]),    # Median         (50th percentile)
        'q3'    : np.mean([27293960]),    # Third quartile (75th percentile)
        'whishi': np.mean([63696360]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([358017]),    # Bottom whisker position
        'q1'    : np.mean([1367929]),    # First quartile (25th percentile)
        'med'   : np.mean([2008049]),    # Median         (50th percentile)
        'q3'    : np.mean([2704058]),    # Third quartile (75th percentile)
        'whishi': np.mean([64347149]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([85432]),    # Bottom whisker position
        'q1'    : np.mean([2198857]),    # First quartile (25th percentile)
        'med'   : np.mean([3620168]),    # Median         (50th percentile)
        'q3'    : np.mean([5852091]),    # Third quartile (75th percentile)
        'whishi': np.mean([76058035]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([38031]),    # Bottom whisker position
        'q1'    : np.mean([1364237]),    # First quartile (25th percentile)
        'med'   : np.mean([2308387]),    # Median         (50th percentile)
        'q3'    : np.mean([3344188]),    # Third quartile (75th percentile)
        'whishi': np.mean([67526353]),    # Top whisker position
        'fliers': []        # Outliers
    }

]
bx = axs[0][1].bxp(boxes,patch_artist=True,vert=False)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bx[element], color='black', alpha = 0.5)

axs[0][1].set_title("PARALLELISM 2,2,2")
axs[0][1].set_yticks([r for r in range(len([1,2,3,4,5]))],
                  ['', '', '', '', ''])

bx['boxes'][0].set(facecolor = (76/255,114/255,176/255), alpha = 1)
bx['boxes'][1].set(facecolor = (221/255,132/255,83/255),alpha = 1)
bx['boxes'][2].set(facecolor = (85/255,168/255,104/255),alpha = 1)
bx['boxes'][3].set(facecolor = (196/255,77/255,82/255), alpha = 1)
bx['boxes'][4].set(facecolor = (130/255,113/255,178/255), alpha = 1)


boxes = [
    {
        'whislo': np.mean([2006]),    # Bottom whisker position
        'q1'    : np.mean([1504333]),    # First quartile (25th percentile)
        'med'   : np.mean([1880174]),    # Median         (50th percentile)
        'q3'    : np.mean([2250293]),    # Third quartile (75th percentile)
        'whishi': np.mean([6605957]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([32811]),    # Bottom whisker position
        'q1'    : np.mean([1787322]),    # First quartile (25th percentile)
        'med'   : np.mean([3268923]),    # Median         (50th percentile)
        'q3'    : np.mean([4702385]),    # Third quartile (75th percentile)
        'whishi': np.mean([63235850]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([344985]),    # Bottom whisker position
        'q1'    : np.mean([2921907]),    # First quartile (25th percentile)
        'med'   : np.mean([4974320]),    # Median         (50th percentile)
        'q3'    : np.mean([7116421]),    # Third quartile (75th percentile)
        'whishi': np.mean([68231306]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([156442]),    # Bottom whisker position
        'q1'    : np.mean([3487990]),    # First quartile (25th percentile)
        'med'   : np.mean([5868053]),    # Median         (50th percentile)
        'q3'    : np.mean([8376210]),    # Third quartile (75th percentile)
        'whishi': np.mean([67914264]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([15999]),    # Bottom whisker position
        'q1'    : np.mean([1901614]),    # First quartile (25th percentile)
        'med'   : np.mean([3402266]),    # Median         (50th percentile)
        'q3'    : np.mean([4982629]),    # Third quartile (75th percentile)
        'whishi': np.mean([64107031]),    # Top whisker position
        'fliers': []        # Outliers
    }

]
bx = axs[1][0].bxp(boxes,patch_artist=True,vert=False)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bx[element], color='black', alpha = 0.5)

axs[1][0].set_title("PARALLELISM 3,3,3")
axs[1][0].set_yticks([r for r in range(len([1,2,3,4,5]))],
                  ['', '', '', '', ''])

bx['boxes'][0].set(facecolor = (76/255,114/255,176/255), alpha = 1)
bx['boxes'][1].set(facecolor = (221/255,132/255,83/255),alpha = 1)
bx['boxes'][2].set(facecolor = (85/255,168/255,104/255),alpha = 1)
bx['boxes'][3].set(facecolor = (196/255,77/255,82/255), alpha = 1)
bx['boxes'][4].set(facecolor = (130/255,113/255,178/255), alpha = 1)


boxes = [
    {
        'whislo': np.mean([3311]),    # Bottom whisker position
        'q1'    : np.mean([1713145]),    # First quartile (25th percentile)
        'med'   : np.mean([2145716]),    # Median         (50th percentile)
        'q3'    : np.mean([2559798]),    # Third quartile (75th percentile)
        'whishi': np.mean([6991693]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([73666]),    # Bottom whisker position
        'q1'    : np.mean([21952094]),    # First quartile (25th percentile)
        'med'   : np.mean([35009359]),    # Median         (50th percentile)
        'q3'    : np.mean([41403985]),    # Third quartile (75th percentile)
        'whishi': np.mean([63245782]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([13088]),    # Bottom whisker position
        'q1'    : np.mean([1826791]),    # First quartile (25th percentile)
        'med'   : np.mean([3364216]),    # Median         (50th percentile)
        'q3'    : np.mean([4579929]),    # Third quartile (75th percentile)
        'whishi': np.mean([64464435]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([230418]),    # Bottom whisker position
        'q1'    : np.mean([2859943]),    # First quartile (25th percentile)
        'med'   : np.mean([4960073]),    # Median         (50th percentile)
        'q3'    : np.mean([7031422]),    # Third quartile (75th percentile)
        'whishi': np.mean([66422249]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([75911]),    # Bottom whisker position
        'q1'    : np.mean([1723560]),    # First quartile (25th percentile)
        'med'   : np.mean([3412804]),    # Median         (50th percentile)
        'q3'    : np.mean([5188820]),    # Third quartile (75th percentile)
        'whishi': np.mean([59855262]),    # Top whisker position
        'fliers': []        # Outliers
    }

]
bx = axs[1][1].bxp(boxes,patch_artist=True,vert=False)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bx[element], color='black', alpha = 0.5)

axs[1][1].set_title("PARALLELISM 5,5,5")
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