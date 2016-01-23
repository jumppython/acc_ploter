import numpy as np
import csv
import matplotlib.pyplot as plt

def pause_plot(readflow):
    #fig,ax = plt.subplots(1,1)
    x = np.arange(0,10,0.5)
    y1 = x*0
    y2 = x*0
    frame = plt.figure(figsize=(15,8))
    frame.subplots_adjust(left=0.05,
                          bottom=0.05,
                          hspace=0.25,
                          wspace=0.25,
                          top=0.95,
                          right=0.95)
    line1 = frame.add_subplot(211)
    line2 = frame.add_subplot(212)
    plot1, = line1.plot(x,y1)
    plot2, = line2.plot(x,y2)
    #index = 1
    y1min,y1max,y2min,y2max = 100,0,100,0
    for row in readflow:
        line = row[0].split(',')
        x += 0.1
        y1[0] = line[1]
        y2[0] = line[3]
        if y1[0]<y1min:
            y1min = y1[0]*0.9
        if y1[0]>y1max:
            y1max = y1[0]*1.1
        if y2[0]<y2min:
            y2min = y2[0]*0.9
        if y2[0]>y2max:
            y2max = y2[0]*1.1
        #for i in range(index+1,0,-1):
        for i in range(19,0,-1):
            y1[i] = y1[i-1]
            y2[i] = y2[i-1]
        plot1.set_data(x,y1)
        plot2.set_data(x,y2)
        line1.set_xlim((x.min(),x.max()))
        line2.set_xlim((x.min(),x.max()))
        line1.set_ylim((y1min,y1max))
        line2.set_ylim((y2min,y2max))
        line1.grid(True)
        line2.grid(True)
        #index += 1
        plt.pause(0.001)

if __name__=="__main__":
    with open('./exrateFile_YAN.csv','r',newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar=',')
        next(reader)
        pause_plot(reader)
