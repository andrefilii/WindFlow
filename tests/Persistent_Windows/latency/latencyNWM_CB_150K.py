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
fig.suptitle(f"NWM COUNT-BASED LATENCY 150K KEYS\nLOG SCALE")
fig.supylabel("")

axs[0][0].set_xscale('log')
axs[0][1].set_xscale('log')
axs[1][0].set_xscale('log')
axs[1][1].set_xscale('log')

boxes = [
    {
        'whislo': np.mean([5536]),    # Bottom whisker position
        'q1'    : np.mean([22340]),    # First quartile (25th percentile)
        'med'   : np.mean([38040]),    # Median         (50th percentile)
        'q3'    : np.mean([53589]),    # Third quartile (75th percentile)
        'whishi': np.mean([770419]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([688003]),    # Bottom whisker position 
        'q1'    : np.mean([1264068]),    # First quartile (25th percentile)
        'med'   : np.mean([1840068]),    # Median         (50th percentile)
        'q3'    : np.mean([2416016]),    # Third quartile (75th percentile)
        'whishi': np.mean([22280108]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([872004]),    # Bottom whisker position
        'q1'    : np.mean([1628000]),    # First quartile (25th percentile)
        'med'   : np.mean([2352020]),    # Median         (50th percentile)
        'q3'    : np.mean([6419998]),    # Third quartile (75th percentile)
        'whishi': np.mean([28428900]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([71144]),    # Bottom whisker position
        'q1'    : np.mean([126532]),    # First quartile (25th percentile)
        'med'   : np.mean([184770]),    # Median         (50th percentile)
        'q3'    : np.mean([242341]),    # Third quartile (75th percentile)
        'whishi': np.mean([2964292]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([283992]),    # Bottom whisker position
        'q1'    : np.mean([544032]),    # First quartile (25th percentile)
        'med'   : np.mean([796003]),    # Median         (50th percentile)
        'q3'    : np.mean([1052017]),    # Third quartile (75th percentile)
        'whishi': np.mean([12499993]),    # Top whisker position
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
        'whislo': np.mean([2850]),    # Bottom whisker position
        'q1'    : np.mean([19287]),    # First quartile (25th percentile)
        'med'   : np.mean([31801]),    # Median         (50th percentile)
        'q3'    : np.mean([44001]),    # Third quartile (75th percentile)
        'whishi': np.mean([1050746]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([20569]),    # Bottom whisker position
        'q1'    : np.mean([244608]),    # First quartile (25th percentile)
        'med'   : np.mean([1348590]),    # Median         (50th percentile)
        'q3'    : np.mean([1892620]),    # Third quartile (75th percentile)
        'whishi': np.mean([14516566]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([95949]),    # Bottom whisker position
        'q1'    : np.mean([423973]),    # First quartile (25th percentile)
        'med'   : np.mean([1699970]),    # Median         (50th percentile)
        'q3'    : np.mean([2263960]),    # Third quartile (75th percentile)
        'whishi': np.mean([13019957]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([672]),    # Bottom whisker position
        'q1'    : np.mean([64889]),    # First quartile (25th percentile)
        'med'   : np.mean([151159]),    # Median         (50th percentile)
        'q3'    : np.mean([218166]),    # Third quartile (75th percentile)
        'whishi': np.mean([1811031]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([32028]),    # Bottom whisker position
        'q1'    : np.mean([200041]),    # First quartile (25th percentile)
        'med'   : np.mean([640025]),    # Median         (50th percentile)
        'q3'    : np.mean([880000]),    # Third quartile (75th percentile)
        'whishi': np.mean([6252001]),    # Top whisker position
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
        'whislo': np.mean([200]),    # Bottom whisker position
        'q1'    : np.mean([39658]),    # First quartile (25th percentile)
        'med'   : np.mean([71144]),    # Median         (50th percentile)
        'q3'    : np.mean([101115]),    # Third quartile (75th percentile)
        'whishi': np.mean([1211014]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([30375]),    # Bottom whisker position
        'q1'    : np.mean([257619]),    # First quartile (25th percentile)
        'med'   : np.mean([375190]),    # Median         (50th percentile)
        'q3'    : np.mean([501612]),    # Third quartile (75th percentile)
        'whishi': np.mean([2219320]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([40014]),    # Bottom whisker position
        'q1'    : np.mean([428595]),    # First quartile (25th percentile)
        'med'   : np.mean([1074420]),    # Median         (50th percentile)
        'q3'    : np.mean([2876014]),    # Third quartile (75th percentile)
        'whishi': np.mean([10580001]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([1370]),    # Bottom whisker position
        'q1'    : np.mean([223197]),    # First quartile (25th percentile)
        'med'   : np.mean([323055]),    # Median         (50th percentile)
        'q3'    : np.mean([446324]),    # Third quartile (75th percentile)
        'whishi': np.mean([2028016]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([36581]),    # Bottom whisker position
        'q1'    : np.mean([266654]),    # First quartile (25th percentile)
        'med'   : np.mean([480363]),    # Median         (50th percentile)
        'q3'    : np.mean([768016]),    # Third quartile (75th percentile)
        'whishi': np.mean([3151307]),    # Top whisker position
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
        'whislo': np.mean([33]),    # Bottom whisker position
        'q1'    : np.mean([16648]),    # First quartile (25th percentile)
        'med'   : np.mean([37280]),    # Median         (50th percentile)
        'q3'    : np.mean([56587]),    # Third quartile (75th percentile)
        'whishi': np.mean([1031642]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([4898]),    # Bottom whisker position
        'q1'    : np.mean([278107]),    # First quartile (25th percentile)
        'med'   : np.mean([459054]),    # Median         (50th percentile)
        'q3'    : np.mean([622728]),    # Third quartile (75th percentile)
        'whishi': np.mean([1963063]),    # Top whisker position
        'fliers': []        # Outliers
    }, {
        'whislo': np.mean([31995]),    # Bottom whisker position
        'q1'    : np.mean([296006]),    # First quartile (25th percentile)
        'med'   : np.mean([524043]),    # Median         (50th percentile)
        'q3'    : np.mean([792030]),    # Third quartile (75th percentile)
        'whishi': np.mean([6139997]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([450]),    # Bottom whisker position
        'q1'    : np.mean([241155]),    # First quartile (25th percentile)
        'med'   : np.mean([414230]),    # Median         (50th percentile)
        'q3'    : np.mean([561998]),    # Third quartile (75th percentile)
        'whishi': np.mean([1818132]),    # Top whisker position
        'fliers': []        # Outliers
    },{
        'whislo': np.mean([927]),    # Bottom whisker position
        'q1'    : np.mean([261557]),    # First quartile (25th percentile)
        'med'   : np.mean([400620]),    # Median         (50th percentile)
        'q3'    : np.mean([555746]),    # Third quartile (75th percentile)
        'whishi': np.mean([1506728]),    # Top whisker position
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