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
# ABBIAMO = 0 / 1

#axs[0][0].set_yscale("log")
#axs[1][0].set_yscale("log")
#axs[0][1].set_yscale("log")
#axs[1][1].set_yscale("log")

fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"INCREMENTAL WINDOW SUM (IWS) COUNT BASED (CB)\nMEMORYCAP 8GB")
fig.supylabel("Tuples/second")

# set width of bar
barWidth = 0.10


#PARALLELISM 1
normal1716 = [123013,150412,130291,137921,144821]
normalt3432 = [60123,58288,62118,59823,60816]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [16551,19241,17121,18761,17264]
persistentn34321m = [11848,13075,12522,12983,12762]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [20687,22521,21213,20935,21373]
persistentn34322m = [9208,10177,9504,9781,9682]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [15782,17621,18721,16731,17932]
persistents34321m = [12831,13721,11982,12864,13291]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [21632,22381,20341,22614,21126]
persistents34322m = [9121,10212,9371,9721,9571]
fpersistents2m = [np.mean(persistents17162m),np.mean(persistents34322m)]
fpersistents2merr = [np.std(persistents17162m),np.std(persistents34322m)]

# set height of bar

# Set position of bar on X axis
br1 = np.arange(len([1,2]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]

# Make the plot
axs[0][0].bar(br1, fnormal, yerr=fnormalerr,width=barWidth,
           edgecolor='grey', label='Normal', error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(67/255,91/255,154/255))
axs[0][0].bar(br2, fpersistentn1m, yerr=fpersistentn1merr,width=barWidth,
           edgecolor='grey', label='Persistent_256MB_EACH_MAP', error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(196/255,116/255,74/255))
axs[0][0].bar(br4, fpersistents1m, yerr=fpersistents1merr,width=barWidth,
           edgecolor='grey', label='Persistent_256MB_SHARED',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(166/255,63/255,69/255))
axs[0][0].bar(br3, fpersistentn2m, yerr=fpersistentn2merr,width=barWidth,
           edgecolor='grey', label='Persistent_512MB_EACH_MAP',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(89/255,151/255,91/255))
axs[0][0].bar(br5, fpersistents2m, yerr=fpersistents2merr,width=barWidth,
           edgecolor='grey', label='Persistent_512MB_SHARED',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(108/255,91/255,158/255))

axs[0][0].set_title("PARALLELISM 1,1,1,1")
axs[0][0].set_xticks([r + barWidth for r in range(len([1,2]))],
                  ['500K', '1M'])


#PARALLELISM 2
normal1716 = [137921,141234,139382,140762,138721]
normalt3432 = [120312,135212,137121,133920,127919]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [42422,44872,43184,43521,42975]
persistentn34321m = [30262,32712,31832,31947,30931]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [60119,62581,61531,61255,60816]
persistentn34322m = [31190,32143,33419,32597,32522]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [7323,7578,7591,7492,7529]
persistents34321m = [6134,6689,6357,6584,6582]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [8881,9147,9037,8973,9081]
persistents34322m = [7572,8542,7625,7972,7767]
fpersistents2m = [np.mean(persistents17162m),np.mean(persistents34322m)]
fpersistents2merr = [np.std(persistents17162m),np.std(persistents34322m)]

# set height of bar

# Set position of bar on X axis
br1 = np.arange(len([1,2]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]

# Make the plot
axs[0][1].bar(br1, fnormal, yerr=fnormalerr,width=barWidth,
           edgecolor='grey', label='Normal', error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(67/255,91/255,154/255))
axs[0][1].bar(br2, fpersistentn1m, yerr=fpersistentn1merr,width=barWidth,
           edgecolor='grey', label='Persistent_256MB_EACH_MAP', error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(196/255,116/255,74/255))
axs[0][1].bar(br4, fpersistents1m, yerr=fpersistents1merr,width=barWidth,
           edgecolor='grey', label='Persistent_256MB_SHARED',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(166/255,63/255,69/255))
axs[0][1].bar(br3, fpersistentn2m, yerr=fpersistentn2merr,width=barWidth,
           edgecolor='grey', label='Persistent_512MB_EACH_MAP',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(89/255,151/255,91/255))
axs[0][1].bar(br5, fpersistents2m, yerr=fpersistents2merr,width=barWidth,
           edgecolor='grey', label='Persistent_512MB_SHARED',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(108/255,91/255,158/255))

axs[0][1].set_title("PARALLELISM 2,2,2,2")
axs[0][1].set_xticks([r + barWidth for r in range(len([1,2]))],
                  ['500K', '1M'])


#PARALLELISM 3 
normal1716 = [182391,173302,167581,177862,175977]
normalt3432 = [203913,189173,187361,197421,188279]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [56692,58731,57631,59833,55918]
persistentn34321m = [49989,52897,51428,50381,51539]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [110230,112125,123716,117631,115783]
persistentn34322m = [52209,55871,62121,58712,57899]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [12141,11932,12781,11761,12620]
persistents34321m = [12654,11782,12631,12683,11585]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [14834,14792,14532,15873,14699]
persistents34322m = [13736,13277,12988,12765,13475]
fpersistents2m = [np.mean(persistents17162m),np.mean(persistents34322m)]
fpersistents2merr = [np.std(persistents17162m),np.std(persistents34322m)]

# set height of bar

# Set position of bar on X axis
br1 = np.arange(len([1,2]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]

# Make the plot
axs[1][0].bar(br1, fnormal, yerr=fnormalerr,width=barWidth,
           edgecolor='grey', label='Normal', error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(67/255,91/255,154/255))
axs[1][0].bar(br2, fpersistentn1m, yerr=fpersistentn1merr,width=barWidth,
           edgecolor='grey', label='Persistent_256MB_EACH_MAP', error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(196/255,116/255,74/255))
axs[1][0].bar(br4, fpersistents1m, yerr=fpersistents1merr,width=barWidth,
           edgecolor='grey', label='Persistent_256MB_SHARED',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(166/255,63/255,69/255))
axs[1][0].bar(br3, fpersistentn2m, yerr=fpersistentn2merr,width=barWidth,
           edgecolor='grey', label='Persistent_512MB_EACH_MAP',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(89/255,151/255,91/255))
axs[1][0].bar(br5, fpersistents2m, yerr=fpersistents2merr,width=barWidth,
           edgecolor='grey', label='Persistent_512MB_SHARED',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(108/255,91/255,158/255))

axs[1][0].set_title("PARALLELISM 3,3,3,3")
axs[1][0].set_xticks([r + barWidth for r in range(len([1,2]))],
                  ['500K', '1M'])

#PARALLELISM 5
normal1716 = [214237,233182,216372,228272,230827]
normalt3432 = [238391,225718,237481,242738,236681]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [101445,105417,113718,109233]
persistentn34321m = [94159,97356,95873,96371,98317]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [118583,120381,121874,121471,122355]
persistentn34322m = [116123,121873,117788,118731,119388]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [29463,26984,23173,25901,27913]
persistents34321m = [33763,40817,44762,42879,38371]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [26157,31105,34583,29418,30487]
persistents34322m = [37742,41482,40347,39174,38137]
fpersistents2m = [np.mean(persistents17162m),np.mean(persistents34322m)]
fpersistents2merr = [np.std(persistents17162m),np.std(persistents34322m)]

# set height of bar

# Set position of bar on X axis
br1 = np.arange(len([1,2]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]

# Make the plot
axs[1][1].bar(br1, fnormal, yerr=fnormalerr,width=barWidth,
           edgecolor='grey', label='Normal', error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(67/255,91/255,154/255))
axs[1][1].bar(br2, fpersistentn1m, yerr=fpersistentn1merr,width=barWidth,
           edgecolor='grey', label='Persistent_256MB_EACH_MAP', error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(196/255,116/255,74/255))
axs[1][1].bar(br4, fpersistents1m, yerr=fpersistents1merr,width=barWidth,
           edgecolor='grey', label='Persistent_256MB_SHARED',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(166/255,63/255,69/255))
axs[1][1].bar(br3, fpersistentn2m, yerr=fpersistentn2merr,width=barWidth,
           edgecolor='grey', label='Persistent_512MB_EACH_MAP',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(89/255,151/255,91/255))
axs[1][1].bar(br5, fpersistents2m, yerr=fpersistents2merr,width=barWidth,
           edgecolor='grey', label='Persistent_512MB_SHARED',error_kw=dict(ecolor='black', lw=1, capsize=3, capthick=1, alpha = 0.5), color=(108/255,91/255,158/255))

axs[1][1].set_title("PARALLELISM 5,5,5,5")
axs[1][1].set_xticks([r + barWidth for r in range(len([1,2]))],
                  ['500K', '1M'])

fig.supxlabel("KEYS")
fig.legend(labels=["IN-MEMORY", "PERSISTENT_PRIVATE(1)", "PERSISTENT_SHARED(1)", "PERSISTENT_PRIVATE(2)", "PERSISTENT_SHARED(2)"], loc='upper left')
plt.show()