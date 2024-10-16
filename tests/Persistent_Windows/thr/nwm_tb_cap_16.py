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
# 0 -> CB_INC_NORMAL , 1-> CB_P_INC, 2->CB_NON_INC_NORMAL, 3->CB_P_NON_INC, 4 ->TB_INC_NORMAL , 5->TB_P_INC, 6->TB_NONINC_NORMAL, 7->TB_P_NONINC ;;
# ABBIAMO = 6 / 7

#axs[0][0].set_yscale("log")
#axs[1][0].set_yscale("log")
#axs[0][1].set_yscale("log")
#axs[1][1].set_yscale("log")

fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"NON INCREMENTAL WINDOW MEAN (NWM) TIME BASED (TB) THROUGHPUT \nMEMORYCAP 16GB", ha = "center")
fig.supylabel("Tuples/second")
fig.supxlabel("KEYS")

# set width of bar
barWidth = 0.10


#PARALLELISM 1
normal1716 = [123491,122931,93813,103891,112941]
normalt3432 = [46481,50949,52913,48913,50727]
#normalt3432 = [0]
#normal1716 = [0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [12811,14842,13553,15902,14831]
persistentn34321m = [11122,13381,10124,11424,13727]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [25578,27361,25673,26471,25733]
persistentn34322m = [10217,12110,11531,12313,10362]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [17732,19941,18742,18372,17922]
persistents34321m = [17677,19148,17534,18637,19437]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [18728,20091,19304,21314,20489]
persistents34322m = [17440,20841,18524,21831,20381]
fpersistents2m = [np.mean(persistents17162m),np.mean(persistents34322m)]
fpersistents2merr = [np.std(persistents17162m),np.std(persistents34322m)]

# set height of bar

# Set position of bar on X axis
br1 = np.arange(len([1,2]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]
br6 = [x + barWidth for x in br5]

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
                  ['150K', '300K'])


#PARALLELISM 2
normal1716 = [239028,204924,218417,212389,223914]
normalt3432 = [138912,135821,142893,145931,143913]
#normalt3432 = [0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [28632,30783,29522,31923,31821]
persistentn34321m = [26869,28345,29435,27301,30717]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [33776,35051,34742,36821,34931]
persistentn34322m = [35686,37741,3887,36855,36357]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [42747,45841,44783,43831,45812]
persistents34321m = [37096,39626,38582,38721,37889]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [49958,52713,50973,51938,50831]
persistents34322m = [43901,45871,47913,48931,46399]
fpersistents2m = [np.mean(persistents17162m),np.mean(persistents34322m)]
fpersistents2merr = [np.std(persistents17162m),np.std(persistents34322m)]

# set height of bar

# Set position of bar on X axis
br1 = np.arange(len([1,2]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]
br6 = [x + barWidth for x in br5]

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
                  ['150K', '300K'])


#PARALLELISM 3 
normal1716 = [300134,312034,306273,315931,300919]
normalt3432 = [240318,247310,245313,244941,250132]
#normalt3432 = [0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [45144,47923,48918,46731,47391]
persistentn34321m = [42271,45631,46672,47831,45893]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [47647,50783,49783,48313,51928]
persistentn34322m = [72793,75723,74983,73992,73293]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [67443,70812,68831,69378,70162]
persistents34321m = [59730,60732,59544,61732,60821]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [80925,83381,82783,82314,81041]
persistents34322m = [130934,150525,140831,147813,139855]
fpersistents2m = [np.mean(persistents17162m),np.mean(persistents34322m)]
fpersistents2merr = [np.std(persistents17162m),np.std(persistents34322m)]

# set height of bar

# Set position of bar on X axis
br1 = np.arange(len([1,2]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]
br6 = [x + barWidth for x in br5]

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
                  ['150K', '300K'])

#PARALLELISM 5
normal1716 = [480319,509134,589313,535213,555222]
#normal1716 = [0]
normalt3432 = [525901,526122,575623,567313,566253]
#normalt3432 = [0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [113974,115832,113525,110313,111152]
persistentn34321m = [77283,79731,77831,78127,76313]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [84203,87371,85783,86731,85523]
persistentn34322m = [112980,115381,114918,113921,115256]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [119219,122391,121832,120319,121931]
persistents34321m = [106717,117312,109741,110329,112522]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [144673,157313,149631,153182,149257]
persistents34322m = [228598,235000,230783,234132,236523]
fpersistents2m = [np.mean(persistents17162m),np.mean(persistents34322m)]
fpersistents2merr = [np.std(persistents17162m),np.std(persistents34322m)]

# set height of bar

# Set position of bar on X axis
br1 = np.arange(len([1,2]))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]
br6 = [x + barWidth for x in br5]

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
                  ['150K', '300K'])


fig.legend(labels=["IN-MEMORY", "PERSISTENT_FRAG32(1)", "PERSISTENT_FRAG64(1)", "PERSISTENT_FRAG32(2)", "PERSISTENT_FRAG64(2)"], loc='upper left')
plt.show()