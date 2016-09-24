import time
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation

def GeneratePlotDataFile(textfile, y_values, start_time):
    tf = textfile
    f = open(tf, 'a+')
    plottemp = ','.join(y_values)
    elapsed_time = str(int(time.time() - start_time))
    x_value = elapsed_time
    f.write(plottemp + '-' + x_value + '\n')
    f.close()

def Plot(textfile,y_amount):
    #Source File
    tf = textfile
    # Setup figure and subplots
    f = figure(num = 0, figsize = (12, 8))#, dpi = 100)
    f.suptitle("Temperature Plot", fontsize=12)
    a = subplot2grid((1, 1), (0, 0))

    # Set titles of subplots
    a.set_title('Temperature vs Time')

    # Turn on grids
    a.grid(True)

    # set label names
    a.set_xlabel("t(s)")
    a.set_ylabel("Temperature(C)")

    #set y limits
    a.set_ylim(0,50)

    #Data Placeholders
    dph = zeros(0)

    # set plots
    plots = {}
    lph1 = []
    lph2 = []
    for i in range(0,y_amount):
        plots['plt{}'.format(i)], = a.plot(dph,dph, label="Sensor{}".format(i+1))
        lph1.append(plots['plt{}'.format(i)])
        lph2.append(plots['plt{}'.format(i)].get_label())
        #set legends
    a.legend(lph1, lph2)

    #Setup animation function
    def updateData(self):
        pullData = open(tf,"r").read()
        dataList = pullData.split('\n')

        # Setup Lists
        xList = []
        for i in range(0,y_amount):
            plots['yList{}'.format(i)] = []

        for eachLine in dataList:
            if len(eachLine) > 1:
                y_all, x = eachLine.split('-')
                xList.append(int(x))
                y = y_all.split(',')
                for i in range(0,len(y)):
                    plots['yList{}'.format(i)].append(int(round(float(y[i]),0)))
        for i in range(0,y_amount):
            plots['plt{}'.format(i)].set_data(xList,plots['yList{}'.format(i)])
            plots['plt{}'.format(i)].axes.relim()
            plots['plt{}'.format(i)].axes.autoscale_view(True,True,True)
    ani = animation.FuncAnimation(f, updateData, interval=1000)
    plt.show()
