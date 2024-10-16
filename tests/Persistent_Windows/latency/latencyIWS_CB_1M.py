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
fig.suptitle(f"IWS COUNT-BASED LATENCY 1M KEYS\nLOG SCALE")
fig.supylabel("")

axs[0][0].set_xscale('log')
axs[0][1].set_xscale('log')
axs[1][0].set_xscale('log')
axs[1][1].set_xscale('log')

boxes = [
    {
        'whislo': np.mean([3389]),    # Bottom whisker position
        'q1'    : np.mean([4610]),    # First quartile (25th percentile)
        'med'   : np.mean([5776]),    # Median         (50th percentile)
        'q3'    : np.mean([6934]),    # Third quartile (75th percentile)
        'whishi': np.mean([440471]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([80101]),    # Bottom whisker position
        'q1'    : np.mean([134131]),    # First quartile (25th percentile)
        'med'   : np.mean([189310]),    # Median         (50th percentile)
        'q3'    : np.mean([244238]),    # Third quartile (75th percentile)
        'whishi': np.mean([15299469]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([81302]),    # Bottom whisker position
        'q1'    : np.mean([138682]),    # First quartile (25th percentile)
        'med'   : np.mean([197465]),    # Median         (50th percentile)
        'q3'    : np.mean([255566]),    # Third quartile (75th percentile)
        'whishi': np.mean([16005210]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([77448]),    # Bottom whisker position
        'q1'    : np.mean([130580]),    # First quartile (25th percentile)
        'med'   : np.mean([184354]),    # Median         (50th percentile)
        'q3'    : np.mean([239056]),    # Third quartile (75th percentile)
        'whishi': np.mean([15039850]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([75799]),    # Bottom whisker position
        'q1'    : np.mean([127898]),    # First quartile (25th percentile)
        'med'   : np.mean([180333]),    # Median         (50th percentile)
        'q3'    : np.mean([232890]),    # Third quartile (75th percentile)
        'whishi': np.mean([14820756]),    # Top whisker position
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
        'whislo': np.mean([1318]),    # Bottom whisker position
        'q1'    : np.mean([3977]),    # First quartile (25th percentile)
        'med'   : np.mean([5874]),    # Median         (50th percentile)
        'q3'    : np.mean([7833]),    # Third quartile (75th percentile)
        'whishi': np.mean([240756]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([3940]),    # Bottom whisker position
        'q1'    : np.mean([112421]),    # First quartile (25th percentile)
        'med'   : np.mean([192305]),    # Median         (50th percentile)
        'q3'    : np.mean([296218]),    # Third quartile (75th percentile)
        'whishi': np.mean([8438994]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([5309]),    # Bottom whisker position
        'q1'    : np.mean([113128]),    # First quartile (25th percentile)
        'med'   : np.mean([189821]),    # Median         (50th percentile)
        'q3'    : np.mean([291091]),    # Third quartile (75th percentile)
        'whishi': np.mean([8395784]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([787]),    # Bottom whisker position
        'q1'    : np.mean([102158]),    # First quartile (25th percentile)
        'med'   : np.mean([180396]),    # Median         (50th percentile)
        'q3'    : np.mean([283928]),    # Third quartile (75th percentile)
        'whishi': np.mean([8143909]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([104483]),    # Bottom whisker position
        'q1'    : np.mean([181345]),    # First quartile (25th percentile)
        'med'   : np.mean([237781]),    # Median         (50th percentile)
        'q3'    : np.mean([292615]),    # Third quartile (75th percentile)
        'whishi': np.mean([7935399]),    # Top whisker position
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
        'whislo': np.mean([872]),    # Bottom whisker position
        'q1'    : np.mean([2928]),    # First quartile (25th percentile)
        'med'   : np.mean([4705]),    # Median         (50th percentile)
        'q3'    : np.mean([8145]),    # Third quartile (75th percentile)
        'whishi': np.mean([151026]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([1890]),    # Bottom whisker position
        'q1'    : np.mean([80383]),    # First quartile (25th percentile)
        'med'   : np.mean([161024]),    # Median         (50th percentile)
        'q3'    : np.mean([316758]),    # Third quartile (75th percentile)
        'whishi': np.mean([5652313]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([10360]),    # Bottom whisker position
        'q1'    : np.mean([96202]),    # First quartile (25th percentile)
        'med'   : np.mean([178229]),    # Median         (50th percentile)
        'q3'    : np.mean([315578]),    # Third quartile (75th percentile)
        'whishi': np.mean([5636097]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([4741]),    # Bottom whisker position
        'q1'    : np.mean([79538]),    # First quartile (25th percentile)
        'med'   : np.mean([152625]),    # Median         (50th percentile)
        'q3'    : np.mean([291550]),    # Third quartile (75th percentile)
        'whishi': np.mean([5458760]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([482]),    # Bottom whisker position
        'q1'    : np.mean([76978]),    # First quartile (25th percentile)
        'med'   : np.mean([150784]),    # Median         (50th percentile)
        'q3'    : np.mean([300976]),    # Third quartile (75th percentile)
        'whishi': np.mean([5737974]),    # Top whisker position
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
        'whislo': np.mean([21]),    # Bottom whisker position
        'q1'    : np.mean([2750]),    # First quartile (25th percentile)
        'med'   : np.mean([4885]),    # Median         (50th percentile)
        'q3'    : np.mean([17916]),    # Third quartile (75th percentile)
        'whishi': np.mean([161583]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([476]),    # Bottom whisker position
        'q1'    : np.mean([99660]),    # First quartile (25th percentile)
        'med'   : np.mean([181315]),    # Median         (50th percentile)
        'q3'    : np.mean([458722]),    # Third quartile (75th percentile)
        'whishi': np.mean([3664764]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([1961]),    # Bottom whisker position
        'q1'    : np.mean([105652]),    # First quartile (25th percentile)
        'med'   : np.mean([188211]),    # Median         (50th percentile)
        'q3'    : np.mean([402353]),    # Third quartile (75th percentile)
        'whishi': np.mean([3621250]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([1419]),    # Bottom whisker position
        'q1'    : np.mean([68463]),    # First quartile (25th percentile)
        'med'   : np.mean([127298]),    # Median         (50th percentile)
        'q3'    : np.mean([188929]),    # Third quartile (75th percentile)
        'whishi': np.mean([3514491]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([609]),    # Bottom whisker position
        'q1'    : np.mean([68934]),    # First quartile (25th percentile)
        'med'   : np.mean([128771]),    # Median         (50th percentile)
        'q3'    : np.mean([191983]),    # Third quartile (75th percentile)
        'whishi': np.mean([3580977]),    # Top whisker position
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