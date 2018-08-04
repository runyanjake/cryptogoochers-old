# @author Jake Runyan
# grapher.py
# Following along with sentdex's twitter sentiment analysis tutorial on youtube.

import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

style.use("ggplot")

fig = plt.figure("SENTIMENT ANALYSIS (Most recent tweets [X] versus Sentiment Aggregate +/- 1 [Y])")
fig2 = plt.figure("CURRENT PERCENT SENTIMENT ANALYSIS (Most recent tweets [X] versus Proportion of N recent tweet pos and neg ratios [Y])")

ax1 = fig.add_subplot(1,1,1)

ax2 = fig2.add_subplot(1,1,1)

def animate(i):
    pullData = open("twitterout.txt","r").read()
    lines = pullData.split('\n')

    #1 original tutorial code
    # xar = []
    # yar = []
    # x = 0
    # y = 0
    # for l in lines[-200:]:
    #     x += 1
    #     if "pos" in l:
    #         y += 1
    #     elif "neg" in l:
    #         y -= 1
    #     xar.append(x)
    #     yar.append(y)

    #2 graphs
    #Gives counter-average sentments more power to bring things back to even
    #the idea here is that a lot of sequential sentiment one way would be recognized
    #Creates 2 graphs for comparisons
    X_RANGE = 400
    xar = []
    x = 0-X_RANGE
    yar = []
    y = 0
    yar2 = []
    y2 = 0
    for l in lines[0-X_RANGE:]:
        x += 1 #used for both
        if "pos" in l:
            #old
            y += 1
            #new
            if y2 >= 0:
                y2 += 1
            else:
                y2 += (abs(y2)*0.1)
        elif "neg" in l:
            #old
            y -= 1 
            #new
            if y2 <= 0:
                y2 -= 1
            else:
                y2 -= (abs(y2)*0.1)
        xar.append(x)
        yar.append(y)
        yar2.append(y2)

    #3 percent vals (It's its own graph)
    # Plots the percent pos/neg values of the last PSI_POOL_SIZE reads
    # Graphs percents as between -1 and 1, where 1 is 100% positive, 0 is 50/50, and -1 is 100% negative
    # this might require 200+PSI_POOL_SIZE or more things in the array, so use make getdata for awhile
    PSI_POOL_SIZE = 200 #it tries to get this many, the actual amount that these are calculated from will vary
    NUM_XVALS = 400
    xvals = []
    pvals = []
    for i in range(0, NUM_XVALS):
        xvals.append(0-NUM_XVALS+i)
        numpos = 0
        numneg = 0
        for l in (lines[-((NUM_XVALS-i)+PSI_POOL_SIZE):])[:-(NUM_XVALS-i)]:
            if "pos" in l:
                numpos = numpos + 1
            elif "neg" in l:
                numneg = numneg + 1
        pval = 0
        if numneg+numpos>0:
            pval = (numpos - numneg) / (abs(numneg) + numpos)
            # if numneg > numpos:
            #     pval = (0.5 - abs(numneg)/(abs(numneg)+numpos)) * 2
            # else:
            #     pval = (-0.5 + numpos/(abs(numneg)+numpos)) * 2
        print(str(numpos) + " positives and " + str(numneg) + " negatives -> " + str(pval) + " for index " + str((200-i)) + " from the end.")
        pvals.append(pval)
        
    #CONTROL OF WHICH TO PLOT
    ax1.clear()
    # ax1.plot(xar,yar) #1
    ax1.plot(xar,yar2) #2


    #Plot 2
    ax2.clear()
    ax2.plot(xvals,pvals) #3

ani = animation.FuncAnimation(fig, animate, interval=1000)
ani2 = animation.FuncAnimation(fig2, animate, interval=1000)
plt.show()