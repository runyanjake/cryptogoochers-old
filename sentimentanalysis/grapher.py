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

fig = plt.figure()

ax1 = fig.add_subplot(1,1,1)

def animate(i):
    pullData = open("twitterout.txt","r").read()
    lines = pullData.split('\n')

    #original tutorial code
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

    #2 graph attempt
    #Gives counter-average sentments more power to bring things back to even
    #the idea here is that a lot of sequential sentiment one way would be recognized
    #Creates 2 graphs for comparisons
    xar = []
    x = 0
    yar = []
    y = 0
    yar2 = []
    y2 = 0
    for l in lines[-200:]:
        x += 1 #used for both
        if "pos" in l:
            #old
            y += 1
            #new
            if y2 >= 0:
                y2 += 1
            else:
                y2 += (1 + abs(y2)*0.1)
        elif "neg" in l:
            #old
            y -= 1 
            #new
            if y2 <= 0:
                y2 -= 1
            else:
                y2 -= (1 + abs(y2)*0.1)
        xar.append(x)
        yar.append(y)
        yar2.append(y2)
    ax1.clear()
    ax1.plot(xar,yar)
    ax1.plot(xar,yar2)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()