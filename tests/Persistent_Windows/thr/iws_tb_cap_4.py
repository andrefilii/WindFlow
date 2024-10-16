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
# 0 -> CB_INC_NORMAL , 1->CB_P_INC, 2->CB_NON_INC_NORMAL, 3->CB_P_NON_INC, 4 -> TB_INC_NORMAL , 5-> TB_P_INC, 6->TB_NONINC_NORMAL, 7->TB_P_NONINC ;;
# ABBIAMO = 4 / 5

axs[0][0].set_yscale("log")
axs[1][0].set_yscale("log")
axs[0][1].set_yscale("log")
axs[1][1].set_yscale("log")

fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"INCREMENTAL WINDOW SUM (IWS) TIME BASED THROUGHPUT MEMORYCAP 4GB\nLOG SCALE", ha = "center")
fig.supxlabel("KEYS")
fig.supylabel("Tuples/second")

# set width of bar
barWidth = 0.10


#PARALLELISM 1
normal1716 = [31143,30849,26210,28731,31032]
normalt3432 = [0,0,0,0,0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [5987,5161,5270,5738,5582]
persistentn34321m = [4757,4656,4915,5192,4873]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [3492,3654,2814,3298,3591]
persistentn34322m = [2887,3006,2942,3109,3094]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [5671,5203,5241,5575,5498]
persistents34321m = [4562,4426,4172,4398,4444]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [3492,3654,2814,3791,3550]
persistents34322m = [2887,3006,2942,3189,3018]
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
normal1716 = [83400,80411,90370,85434,83019]
normalt3432 = [0,0,0,0,0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [14156,13725,14228,15983,14417]
persistentn34321m = [11891,12340,11925,12251,12544]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [8319,8769,8372,8489,8178]
persistentn34322m = [7485,7317,7855,7514,7614]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [8302,8375,8840,8124,8419]
persistents34321m = [7642,7254,7697,7549,7711]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [8319,8769,8372,8423,8588]
persistents34322m = [7485,7317,7855,7631,7533]
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
normal1716 = [140214,126677,137042,145892,135783]
normalt3432 = [0,0,0,0,0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [21315,20884,22694,22149,20134]
persistentn34321m = [18755,19899,19381,20741,19478]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [14027,13876,13441,14278,13983]
persistentn34322m = [12672,12799,12449,13091,12765]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [14527,14101,13422,14382,14981]
persistents34321m = [12711,12540,12673,13254,12314]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [14027,13876,13441,13777,13255]
persistents34322m = [12672,12799,12449,12678,12135]
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
normal1716 = [272024,284424,220810,264900,245819]
normalt3432 = [0,0,0,0,0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [28236,28492,25871,26879,26814]
persistentn34321m = [18844,21687,20861,22930,19482]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [30992,31718,30023,30728,31847]
persistentn34322m = [24877,25283,26827,27498,26493]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [32290,33221,30403,31894,32407]
persistents34321m = [26460,24600,24319,25893,24899]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [30992,31718,30023,30908,31842]
persistents34322m = [24877,25283,25735,26783,25890]
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


fig.legend(labels=["IN-MEMORY", "PERSISTENT_PRIVATE(1)", "PERSISTENT_SHARED(1)", "PERSISTENT_PRIVATE(2)", "PERSISTENT_SHARED(2)"], loc='upper left')
plt.show()