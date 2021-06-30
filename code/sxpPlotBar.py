#-------------------------------------------------------------------------------
# Name:        sxpPlotBar.py
# Purpose:
#
# Author:      sunxp
#
# Created:     25-11-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np

import sxpReadFileMan
def PlotBar():
    #!/usr/bin/env python
    # a bar plot with errorbars

    N = 5
    menMeans = (20, 35, 30, 35, 27)
    menStd = (2, 3, 4, 1, 2)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd, label='Man')

    womenMeans = (25, 32, 34, 20, 25)
    womenStd = (3, 5, 2, 3, 3)
    rects2 = ax.bar(ind + width, womenMeans, width, color='y', yerr=womenStd, label='Woman')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

 #   ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
    plt.legend(loc=2,fontsize=5);

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.show()
mycnames = {
'aliceblue':            '#F0F8FF',
'antiquewhite':         '#FAEBD7',
'aqua':                 '#00FFFF',
'aquamarine':           '#7FFFD4',
'azure':                '#F0FFFF',
'beige':                '#F5F5DC',
'bisque':               '#FFE4C4',
'black':                '#000000',
'blanchedalmond':       '#FFEBCD',
'blue':                 '#0000FF',
'blueviolet':           '#8A2BE2',
'brown':                '#A52A2A',
'burlywood':            '#DEB887',
'cadetblue':            '#5F9EA0',
'chartreuse':           '#7FFF00',
'chocolate':            '#D2691E',
'coral':                '#FF7F50',
'cornflowerblue':       '#6495ED',
'cornsilk':             '#FFF8DC',
'crimson':              '#DC143C',
'cyan':                 '#00FFFF',
'darkblue':             '#00008B',
'darkcyan':             '#008B8B',
'darkgoldenrod':        '#B8860B',
'darkgray':             '#A9A9A9',
'darkgreen':            '#006400',
'darkkhaki':            '#BDB76B',
'darkmagenta':          '#8B008B',
'darkolivegreen':       '#556B2F',
'darkorange':           '#FF8C00',
'darkorchid':           '#9932CC',
'darkred':              '#8B0000',
'darksalmon':           '#E9967A',
'darkseagreen':         '#8FBC8F',
'darkslateblue':        '#483D8B',
'darkslategray':        '#2F4F4F',
'darkturquoise':        '#00CED1',
'darkviolet':           '#9400D3',
'deeppink':             '#FF1493',
'deepskyblue':          '#00BFFF',
'dimgray':              '#696969',
'dodgerblue':           '#1E90FF',
'firebrick':            '#B22222',
'floralwhite':          '#FFFAF0',
'forestgreen':          '#228B22',
'fuchsia':              '#FF00FF',
'gainsboro':            '#DCDCDC',
'ghostwhite':           '#F8F8FF',
'gold':                 '#FFD700',
'goldenrod':            '#DAA520',
'gray':                 '#808080',
'green':                '#008000',
'greenyellow':          '#ADFF2F',
'honeydew':             '#F0FFF0',
'hotpink':              '#FF69B4',
'indianred':            '#CD5C5C',
'indigo':               '#4B0082',
'ivory':                '#FFFFF0',
'khaki':                '#F0E68C',
'lavender':             '#E6E6FA',
'lavenderblush':        '#FFF0F5',
'lawngreen':            '#7CFC00',
'lemonchiffon':         '#FFFACD',
'lightblue':            '#ADD8E6',
'lightcoral':           '#F08080',
'lightcyan':            '#E0FFFF',
'lightgoldenrodyellow': '#FAFAD2',
'lightgreen':           '#90EE90',
'lightgray':            '#D3D3D3',
'lightpink':            '#FFB6C1',
'lightsalmon':          '#FFA07A',
'lightseagreen':        '#20B2AA',
'lightskyblue':         '#87CEFA',
'lightslategray':       '#778899',
'lightsteelblue':       '#B0C4DE',
'lightyellow':          '#FFFFE0',
'lime':                 '#00FF00',
'limegreen':            '#32CD32',
'linen':                '#FAF0E6',
'magenta':              '#FF00FF',
'maroon':               '#800000',
'mediumaquamarine':     '#66CDAA',
'mediumblue':           '#0000CD',
'mediumorchid':         '#BA55D3',
'mediumpurple':         '#9370DB',
'mediumseagreen':       '#3CB371',
'mediumslateblue':      '#7B68EE',
'mediumspringgreen':    '#00FA9A',
'mediumturquoise':      '#48D1CC',
'mediumvioletred':      '#C71585',
'midnightblue':         '#191970',
'mintcream':            '#F5FFFA',
'mistyrose':            '#FFE4E1',
'moccasin':             '#FFE4B5',
'navajowhite':          '#FFDEAD',
'navy':                 '#000080',
'oldlace':              '#FDF5E6',
'olive':                '#808000',
'olivedrab':            '#6B8E23',
'orange':               '#FFA500',
'orangered':            '#FF4500',
'orchid':               '#DA70D6',
'palegoldenrod':        '#EEE8AA',
'palegreen':            '#98FB98',
'paleturquoise':        '#AFEEEE',
'palevioletred':        '#DB7093',
'papayawhip':           '#FFEFD5',
'peachpuff':            '#FFDAB9',
'peru':                 '#CD853F',
'pink':                 '#FFC0CB',
'plum':                 '#DDA0DD',
'powderblue':           '#B0E0E6',
'purple':               '#800080',
'red':                  '#FF0000',
'rosybrown':            '#BC8F8F',
'royalblue':            '#4169E1',
'saddlebrown':          '#8B4513',
'salmon':               '#FA8072',
'sandybrown':           '#FAA460',
'seagreen':             '#2E8B57',
'seashell':             '#FFF5EE',
'sienna':               '#A0522D',
'silver':               '#C0C0C0',
'skyblue':              '#87CEEB',
'slateblue':            '#6A5ACD',
'slategray':            '#708090',
'snow':                 '#FFFAFA',
'springgreen':          '#00FF7F',
'steelblue':            '#4682B4',
'tan':                  '#D2B48C',
'teal':                 '#008080',
'thistle':              '#D8BFD8',
'tomato':               '#FF6347',
'turquoise':            '#40E0D0',
'violet':               '#EE82EE',
'wheat':                '#F5DEB3',
'white':                '#FFFFFF',
'whitesmoke':           '#F5F5F5',
'yellow':               '#FFFF00',
'yellowgreen':          '#9ACD32'}
def MakeColorList():
    color_set = []
    for eachname,eachhex in list(mycnames.items()):
        color_set.append(eachname)
    return color_set
default_color = MakeColorList()

def PlotBarFromCoordSetAx(ax,titlename, coordset,coordname,colorset = default_color,fname='output.jpg',highratio=0.2, symax = 1.0, widthratio = 1.0,xshift=1.0,xfontdict = {},xtickrotation=0):
    N = len(coordname)

    numtype = N
    modelnum = len(coordset)
    cidx = (np.arange(modelnum)+1.0)/modelnum
    coloridx = cidx[0:modelnum]#np.random.rand(4)


    ymajorLocator   = MultipleLocator(0.05) #将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%1.2f') #设置y轴标签文本的格式
    yminorLocator   = MultipleLocator(0.01) #将此y轴次刻度标签设置为0.1的倍数

    ind = np.arange(N)  # the x locations for the groups
    width = N/(modelnum*(N+2.0))*widthratio #0.15       # the width of the bars
    column_width = 0.05
    #coordname = ['precision','recall','f-sore']
    #coordset = [[legend1, [10,20,10]], [legend2, [11,20,120]],[legend2, [11,20,120]]]

  #  fig, ax = plt.subplots()
    i = 0
    legendname = []
    rect_set = []
    rect_set0 = []

    cmhot = plt.get_cmap("Spectral")
    nm = matplotlib.colors.Normalize(vmin=0.0, vmax=1.0, clip=False)
    m = matplotlib.cm.ScalarMappable(norm = nm,cmap = cmhot)
    my = 0
    for eachd in coordset:
        legendname.append(eachd[0])
        ydata = eachd[1] #(20, 35, 30, 35, 27)
        print(ydata)
        my = max(my,max(ydata))
        #menStd = (2, 3, 4, 1, 2)
        rc = coloridx[i]
        rgba = m.to_rgba(rc)
        if colorset is None:
            cl = matplotlib.colors.rgb2hex(rgba)
        else:
            cl = colorset[i]
        rects2 = ax.bar(ind + width * i*xshift, ydata, column_width,color = cl )
        rect_set.append(rects2[0])
        rect_set0.append(rects2)
        i = i + 1

    s = ()
    i = 0
    ymax = my+my*highratio
    print(ymax)
    if symax is not None:
        ymax = symax
    tn = tuple(coordname)
    ln = tuple(legendname)
    recn = tuple(rect_set)
    ax.set_ylabel('Scores')
    ax.set_title(titlename)
    ax.set_xticks(ind + width*xshift)
    fontdict =xfontdict
    ax.set_xticklabels(tn,fontdict,rotation=xtickrotation)
##    yticks = np.arange(0,ymax,0.05)
##    ytickstr = str(yticks)
##    ax.set_yticks(yticks)
##    ax.set_yticklabels(ytickstr)
    ax.set_ylim(0,ymax)
##    ax.yaxis.grid(True)
   # ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
    ax.legend(recn,ln)
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)
    ax.yaxis.set_minor_locator(yminorLocator)
##    ax.yaxis.grid(True, which='major') #y坐标轴的网格使用次刻度
    ax.yaxis.grid(True, which='major') #y坐标轴的网格使用次刻度
    ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度
##    plt.show()
##
##    plt.savefig(fname)

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')
##    for eachr in rect_set0:
##        autolabel(eachr)
def testmultibar():
    Strain1_Mean = [0.5137,3.2830, 1.5887, 5.9188];
    Strain2_Mean = [0.4042, 2.9884, 0.5709, 2.7766];
    Strain1_std = [1.1393, 2.8108, 2.2203, 3.5233];
    Strain2_std = [0.8762, 2.8478, 0.9878, 2.2197];
    plt.bar([1,2, 3, 4], ['Strain1_Mean', 'Strain2_Mean'])
    plt.legend('Strain 1', 'Strain 2')
    plt.pause;
    plt.close(all);
def PlotBarFromCoordSet(titlename, coordset,coordname,colorset = default_color,fname='output.jpg',highratio=0.2, symax = 1.0, widthratio = 1.0,xshift=1.0,xfontdict = {},xtickrotation=0,xmax_ratio = 1.5):
    #coordname = ['precision','recall','f-sore']
    #coordset = [[legend1, [10,20,10]], [legend2, [11,20,120]],[legend2, [11,20,120]]]
    N = len(coordname)

    numtype = N
    groupnum = len(coordset) #= 10, here because we have 10 models each has one score
    cidx = (np.arange(groupnum)+1.0)/groupnum
    coloridx = cidx[0:groupnum]#np.random.rand(4)


    ymajorLocator   = MultipleLocator(0.10) #将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%1.2f') #设置y轴标签文本的格式
    yminorLocator   = MultipleLocator(0.05) #将此y轴次刻度标签设置为0.1的倍数

    ind = np.arange(N)  # the x locations for the groups
##    width = N/(groupnum*(N+2.0))*widthratio #0.15       # the width of the bars
##    column_width = 0.05

    len_group = 1.0
    occupy_one_bar = len_group / groupnum/1.1
    width=occupy_one_bar*0.5
    column_width =occupy_one_bar*0.5

    #coordname = ['precision','recall','f-sore']
    #coordset = [[legend1, [10,20,10]], [legend2, [11,20,120]],[legend2, [11,20,120]]]
    #when there is only one score in coordname, N = 1 groupnum = 10
    fig, ax = plt.subplots()
    i = 0
    legendname = []
    rect_set = []
    rect_set0 = []

    cmhot = plt.get_cmap("Spectral")
    nm = matplotlib.colors.Normalize(vmin=0.0, vmax=1.0, clip=False)
    m = matplotlib.cm.ScalarMappable(norm = nm,cmap = cmhot)
    my = 0
    xtickpos = []
    for i in range(N):
        xtickpos.append(ind[i] + 0.2)
    i =0
    xmaxpos = []
    for eachd in coordset:
        legendname.append(eachd[0])
        ydata = eachd[1] #(20, 35, 30, 35, 27)
        print(ydata)
        my = max(my,max(ydata))
##        num_bar_in_one_group = len(ydata)
##        column_width = width / num_bar_in_one_group*1.05
        #menStd = (2, 3, 4, 1, 2)
        rc = coloridx[i]
        rgba = m.to_rgba(rc)
        if colorset is None:
            cl = matplotlib.colors.rgb2hex(rgba)
        else:
            cl = colorset[i]
        #rects2 = ax.bar(ind + width * i*xshift, ydata, column_width,color = cl, label=eachd[0])
        rects2 = ax.bar(ind + width * i * xshift, ydata, column_width, label=eachd[0])
        xmaxpos.append(max(ind+ + width * i*xshift))
        rect_set.append(rects2[0])
        rect_set0.append(rects2)
        ax.legend(loc='upper right', borderaxespad=0.)
        i = i + 1

    s = ()
    i = 0
    ymax = my+my*highratio
    print(ymax)
    if symax is not None:
        ymax = symax
    tn = tuple(coordname)
    ln = tuple(legendname)
    recn = tuple(rect_set)
    ax.set_ylabel('Scores')
    ax.set_title(titlename)
##    ax.set_xticks(ind + width*xshift)
    ax.set_xticks(xtickpos)
    xmax = max(xmaxpos)

    ax.set_xlim(0,xmax*xmax_ratio)
    fontdict =xfontdict
    ax.set_xticklabels(tn,fontdict,rotation=xtickrotation)
##    yticks = np.arange(0,ymax,0.05)
##    ytickstr = str(yticks)
##    ax.set_yticks(yticks)
##    ax.set_yticklabels(ytickstr)
    ax.set_ylim(0,ymax)
##    ax.yaxis.grid(True)
   # ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
#    ax.legend(recn,ln)
    plt.legend(loc=2, fontsize=5);
 #   ax.legend(recn,ln,bbox_to_anchor=(1, 1),loc=2, borderaxespad=0.)
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)
    ax.yaxis.set_minor_locator(yminorLocator)
##    ax.yaxis.grid(True, which='major') #y坐标轴的网格使用次刻度
    ax.yaxis.grid(True, which='major') #y坐标轴的网格使用次刻度
    ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度
##    plt.show()
##
##    plt.savefig(fname)

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')
##    for eachr in rect_set0:
##        autolabel(eachr)

def TestBar():
    colorset = ['r','b','g']
    coorname = ['precision','recall','f-score']
    dataset = [['v1',[0.8,0.9,0.85]],
    ['v2',[0.4,0.5,0.65]],
    ['v3',[0.4,0.5,0.55]]
    ]
    PlotBarFromCoordSet('test',dataset,coorname,colorset)
def LoadData():
    fname = 'duc_output_set.pk'
    ds = sxpReadFileMan.LoadSxptext(fname)
    print(ds)
    fname = 'paper_output_set.pk'
    ds = sxpReadFileMan.LoadSxptext(fname)
    print(ds)
def ProcessRougeScore(ds,fhead):
    modelname = ['v1','TFIDF','GS','GW','Context']
    metric_set = [['ROUGE-1','rouge_1_precision','rouge_1_recall','rouge_1_f_score'],
    ['ROUGE-2','rouge_2_precision','rouge_2_recall','rouge_2_f_score'],
    ['ROUGE-3','rouge_2_precision','rouge_2_recall','rouge_2_f_score'],
    ['ROUGE-4','rouge_2_precision','rouge_2_recall','rouge_2_f_score']
    ]
    coorname = ['precision','recall','f-score']
    for eachm in metric_set:# weplot one bar figure
        title = eachm[0]
        colorset = ['r','b','g','c','m']

        dataset= []
        metric_name = eachm[1:]

        i = 0
        #for figure rouge-1, we need to get
        #input = [['v1',[0.8,0.9,0.85],['tfidf',[0.3,0.2,0.4]]]
        print(title)
        for eachmodel in ds:#for five models, we extract each model's metric
        #for tfidf model
            #this is the name 'tfidf'
            legendname  = modelname[i]
            datarow = []
            for eachm in metric_name:
                datarow.append(eachmodel[eachm])
            dataset.append([legendname, datarow])
            i = i + 1
        print(dataset)
        PlotBarFromCoordSet(title,dataset,coorname,colorset,fhead + title+'.jpg')

def plotlinelist(xlist,keylist,title='multiplelines',fname="",vline=[]):
    # Set the plot curve with markers and a title
    # fig = plt.figure()
    # ax = fig.add_axes()
    fig, ax = plt.subplots()
    n = len(xlist)

    for i in range(n):
        nr,nc = xlist[i].shape
        x = range(nr)
        xa = np.array(x).reshape(1,-1)
        ax.plot(xa.reshape(-1,1),xlist[i].reshape(-1,1), marker='o', label=str(keylist[i]))
        ax.legend(loc='upper right', borderaxespad=0.)
    cm = ['r','g','b','c','m','y','k','w']
    nc = len(cm)
    for i, v in enumerate(vline):
        kc =i % nc;
        plt.axvline(x=v, ls="-", c=cm[kc])  # 添加垂直直线
    plt.title(title)
    if len(fname)>0:
        fig.savefig(fname)
#    plt.ion()
    plt.ioff()
    plt.show()
def plotlinelistinbox(xlist,keylist,title='multiplelines',fname="",vline=[]):
    # Set the plot curve with markers and a title
    # fig = plt.figure()
    # ax = fig.add_axes()
    fig, ax = plt.subplots()
    n = len(xlist)

    for i in range(n):
        nr,nc = xlist[i].shape
        x = range(nr)
        xa = np.array(x).reshape(1,-1)
        ax.plot(xa.reshape(-1,1),xlist[i].reshape(-1,1), marker='o', label=str(keylist[i]))
        ax.legend(loc='upper right', borderaxespad=0.)
    cm = ['r','g','b','c','m','y','k','w']
    nc = len(cm)
    for i, v in enumerate(vline):
        kc =i % nc;
        plt.axvline(x=v, ls="-", c=cm[kc])  # 添加垂直直线
    plt.title(title)
    if len(fname)>0:
        fig.savefig(fname)
#    plt.ion()
    plt.show()


def Test():
    fn = 'duc_output_set.pk'
##    ds = sxpReadFileMan.LoadSxptext(fn)
##    fhead = 'duc'
##    ProcessRougeScore(ds,fhead)
##    fn = 'output_set_sec_exc_mymodel.pk'
    ds = sxpReadFileMan.LoadSxptext(fn)
    fhead = 'paper'
    ProcessRougeScore(ds,fhead)
def TestPlot():
    coorname = ['precision','recall','f-score']
    model_score = [['v1',[0.8,0.9,0.85]],
    ['v2',[0.4, 0.5, 0.65]],
    ['v3',[0.4, 0.5, 0.55]]
    ]
    myfontdict = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 14 }
    myxrotate = 0.0
    title = 'hello'
    PlotBarFromCoordSet(title,model_score,coorname,highratio=1.0,symax=1.0,widthratio=0.9,xshift=1.2,xfontdict=myfontdict,xtickrotation=myxrotate)
    plt.savefig('bar.jpg')
    plt.show()
def TestLine():
    n = 3
    xlist =[]
    keylist=[]

    for i in range(n):
        x = np.random.randint(0,30,50)
        xlist.append(x)
        keylist.append('line+'+str(i))
    plotlinelist(xlist,keylist)
def main():
    #TestPlot()
    #TestLine()
    #testmultibar()
    PlotBar()
if __name__ == '__main__':
    main()
