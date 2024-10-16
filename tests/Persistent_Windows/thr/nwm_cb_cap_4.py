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
# ABBIAMO = 2 / 3

#axs[0][0].set_yscale("log")
#axs[1][0].set_yscale("log")
#axs[0][1].set_yscale("log")
#axs[1][1].set_yscale("log")

fig.set_facecolor('white')
fig.align_labels()
fig.suptitle(f"NON INCREMENTAL WINDOW MEAN (NWM) COUNT BASED (CB) THROUGHPUT \nMEMORYCAP 4GB", ha = "center")
fig.supylabel("Tuples/second")
fig.supxlabel("KEYS")

# set width of bar
barWidth = 0.10


#PARALLELISM 1
normal1716 = [0,0,0,0,0]
normalt3432 = [0,0,0,0,0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [17725,18314,17531,17827,18123]
persistentn34321m = [17439,18981,17582,17931,18341]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [21360,22491,21481,22931,21754]
persistentn34322m = [17645,18984,19733,18643,17821]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [31180,33371,32361,32892,33901]
persistents34321m = [25788,27874,26602,26481,27491]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [27991,28529,26564,26781,28371]
persistents34322m = [27448,29609,27845,29741,26425]
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
normal1716 = [0,0,0,0,0]
normalt3432 = [0,0,0,0,0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [35926,37491,36571,37382,37192]
persistentn34321m = [41174,43747,42641,43819,42894]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [64146,66841,65894,66391,65894]
persistentn34322m = [36939,38231,37584,38541,37261]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [59907,61231,60876,62912,61839]
persistents34321m = [55788,57894,56189,58713,56731]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [66521,68894,67244,67381,67313]
persistents34322m = [59201,61721,60674,62913,61922]
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
normal1716 = [0,0,0,0,0]
normalt3432 = [0,0,0,0,0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [57107,54712,59786,56731,57841]
persistentn34321m = [56527,57255,58741,58019,57398]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [48461,50145,51714,52814,50192]
persistentn34322m = [60913,61917,62741,61894,60555]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [89901,90841,91813,88381,90551]
persistents34321m = [88577,89371,90569,89721,90876]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [89232,91894,90783,90894,91747]
persistents34322m = [101918,110741,100831,114819,107192]
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
normal1716 = [0,0,0,0,0]
normalt3432 = [0,0,0,0,0]
fnormal = [np.mean(normal1716),np.mean(normalt3432)]
fnormalerr = [np.std(normal1716),np.std(normalt3432)]

persistentn17161m = [156017,159831,155714,160313,158731]
persistentn34321m = [110479,112814,111841,122134,110248]
fpersistentn1m = [np.mean(persistentn17161m),np.mean(persistentn34321m)]
fpersistentn1merr = [np.std(persistentn17161m),np.std(persistentn34321m)]

persistentn17162m = [114406,115781,115552,116810,114984]
persistentn34322m = [139986,142414,143481,148194,159101]
fpersistentn2m = [np.mean(persistentn17162m),np.mean(persistentn34322m)]
fpersistentn2merr = [np.std(persistentn17162m),np.std(persistentn34322m)]

persistents17161m = [158158,157894,169482,165321,163144]
persistents34321m = [157345,159879,158894,164891,164089]
fpersistents1m = [np.mean(persistents17161m),np.mean(persistents34321m)]
fpersistents1merr = [np.std(persistents17161m),np.std(persistents34321m)]

persistents17162m = [154329,163094,165849,157382,158312]
persistents34322m = [168647,175705,171068,173480,173840]
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