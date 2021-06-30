import numpy as np
import sxpPlotBar
import os
import sxpReadFileMan
import sxpLinearReg
def testdecr():
    ls = [6, 5, 4, 3, 1, 1, 1, 1, 1]
    s = np.array(ls).reshape(-1,1)
    ds = np.diff(s,0).reshape(-1,1)
    sds_idx = np.argsort(-ds,0)
    n,r = s.shape
    wt = np.ones((n,1))
    nr = 1/(np.array(range(n))+1).reshape(-1,1)
    wt = np.multiply(sds_idx,nr)
    dn = n-1
    avg_dcr = np.ones((n-1,1))
    var_dcr = np.ones((n-1,1))
    print(avg_dcr.shape)
    for t in range(2,n+1):
        rs = s[0:t,0].sum()/t
        print(t,)
        avg_dcr[t - 2,0] = rs
        var_dcr[t - 2,0] = np.std(ds[0:t, 0], 0)
    print('var',var_dcr.shape,var_dcr)
    dv = np.abs(MyDiff(var_dcr))
    print('diff var',dv.shape,dv)
    pv = var_dcr[0:dn-1,0].reshape((-1,1))

    av = np.multiply(dv, 1/pv)
    print('diff per var',av.shape,av)

    da = np.abs(MyDiff(avg_dcr))
    pa = avg_dcr[0:dn-1,0].reshape((-1,1))
    aa = np.multiply(da, 1/pa)

    fname3 = 'math.jpg'
    t1='var diff'
    t2 = 'avg_diff'

    sxpPlotBar.plotlinelist([av, aa], [t1, t2], title='sum word len'
                            , fname=fname3)
def testtop3():
    #  ls = [7, 5, 4, 3, 0, 0, 0, 0, 0]
    ls = [10, 5, 4, 3, 0, 0, 0, 0, 0]


# ls = [16,13,12,10, 5, 4, 3, 0, 0, 0, 0, 0]
    s = np.array(ls).reshape(-1,1)
    ds = MyDiff(s,abs_mode=True)
    sds_idx = np.argsort(-ds,0).reshape((-1,1))
    startidx = 0
    topk0  = SplitList(ls,mode='left')
    #topk1 = RecursiveSplit(ds,startidx,1,1,'top')
    topk1 = SplitList(ls,mode='top')
    topk2  = SplitList(ls,mode='right')
    fname3 = 'math.jpg'
    sxpPlotBar.plotlinelist([s, ds], ['s', 'ds'], title='test',fname = fname3
                            , vline = [topk0,topk1,topk2])
def SplitArray(s,mode = 'top'):
    rs= s.reshape((-1,1))
    ds = MyDiff(rs,abs_mode=True)
    startidx = 0
    topk = RecursiveSplit(ds,startidx,1,-1,mode = mode) +1
    return topk #note here topk + 1 is the right range of original seq, topk is for diff seq
def MaxGap(s,mode='Max'):
    rs= s.reshape((-1,1))
    ds = MyDiff(rs,abs_mode=True)
    m = np.argmax(ds,0)[0]

    return m+1 #note here topk + 1 is the right range of original seq, topk is for diff seq
def ScoreAtK(s,k):
    s1= s[:k,0]
    n1 = len(s1)
    tk = 0
    for i in range(n1-1):
        for j in range(i+1,n1):
            sd = np.abs(s1[j]-s1[i])
            tk = tk + sd
    tk = tk /n1/(n1-1)*2
    s2 = s[k:,0]
    n2 = len(s2)
    dk = 0
    for i in range(n1-1):
        for j in range(n2):
            sd = np.abs(s2[j]-s1[i])
            dk = dk + 1-sd
    dk = dk / (n1-1)/n2
    return tk + dk
def ArgMinSD(s):
    n,c = s.shape
    ks = []
    st = 2
    for k in range(st,n-1):
        topkscore = ScoreAtK(s,k)
        ks.append(topkscore)
    im = np.argmin(ks)+2
    return im
def SplitList(ls,mode = 'top'):
    s = np.array(ls).reshape(-1,1)
    ds = MyDiff(s,abs_mode=True)
    startidx = 0
    topk = RecursiveSplit(ds,startidx,1,-1,mode = mode)
    return topk #note here topk + 1 is the right range of original seq, topk is for diff seq
def RecursiveSplit(ds,startidx,level=1,maxlevel=1,mode = 'top'):
    sds_idx = np.argsort(-ds,0).reshape((-1,1))
    n,r = sds_idx.shape
    top1 = sds_idx[0,0]
    # lefttop = range(0,top1)
    # rightop = range(top1+1,n)
    # top2 = sds_idx[1,0]
    # top3 = sds_idx[2,0]
    # leftspliter = min(sds_idx[0:3,0])
    # rigthspliter = max(sds_idx[0:3,0])
    if level == maxlevel:
        return top1+ startidx
    if n <= 2:
        return top1+ startidx

    if mode == 'top':
        return top1+startidx;
    if mode == 'left':
        if top1 < 1:
            return top1 + startidx;
        nextds = ds[0:top1, 0].reshape((-1, 1))
        lefttop = np.Inf;
        if TrySplit(nextds,0, top1):

            lefttop = RecursiveSplit(nextds,0, level + 1, maxlevel)
        print(lefttop,top1,startidx)
        return min(lefttop,top1)+ startidx
    if mode == 'right':
        if top1 >= n - 1:
            return top1 + startidx;
        nextleftds = ds[top1+1:, 0].reshape((-1, 1))
        rightop = -1;
        nstartidx = top1+1;
        if TrySplit(nextleftds, nstartidx,top1):
            rightop = RecursiveSplit(nextleftds,nstartidx, level + 1, maxlevel)
        return max(rightop,top1)+ startidx
    if mode == 'lefthalf':
        if top1 >= n - 1:
            return top1 + startidx;
        nextleftds = ds[0:top1, 0].reshape((-1, 1))
        if top1 <=2:
            return top1 + startidx;
        nstartidx = 0;

        rightop = RecursiveSplit(nextleftds, nstartidx, level + 1, maxlevel)
        return min(rightop, top1) + startidx
    if mode == 'both':
        nextds = ds[0:top1, 0].reshape((-1, 1))
        lefttop = None;
        if TrySplit(nextds, top1):
            lefttop = RecursiveSplit(nextds, level + 1, maxlevel)
        nextleftds = ds[top1:, 0].reshape((-1, 1))
        rightop = None;
        if TrySplit(nextleftds, top1):
            rightop = RecursiveSplit(nextleftds, level + 1, maxlevel)
        if lefttop:
            return min(lefttop,top1)
        if rightop:
            return min(rightop,top1)
        return top1

def TrySplit(ds,startidx,top1,granularity=0.1):
    sds_idx = np.argsort(-ds,0).reshape(-1,1)
    n,r = sds_idx.shape
    ntop1 = sds_idx[0,0]+startidx;
    if abs((ntop1 - top1)/n)<=granularity:
        return False
    sd = np.std(ds)
    if sd <=granularity:
        return False;
    else:
        return True;
def MyDiff(s,abs_mode=False):
    ds = np.diff(s.ravel()).reshape(-1, 1)
    if abs_mode:
        ds = np.abs(ds)
    return ds
def LoadS(chid):
    dname =r"E:\pythonworknew\code\textsum\test\multipaper\test\out\keywordquery"
    fname = r"wordquery_allv6ks_dual_sentrank_{0}_dfscorelist.jpgs.list".format(chid)
    fullname = os.path.join(dname,fname)
    return sxpReadFileMan.LoadObject(fullname)
def LoadAllS():
    dname = r"E:\pythonworknew\code\textsum\test\multipaper\test\out\keywordquery"
    pat =  r"wordquery_allv6ks_dual_sentrank_\d+\.*\d*_dfscorelist.jpgs.list"
    flist = sxpReadFileMan.GetDirFileListByPat(dname,pat)
    doclist = []
    for i,f in enumerate(flist):
        print(i,f)
        truenum,s = sxpReadFileMan.LoadObject(f)
        doclist.append([truenum,s,f])
    return doclist
def TestS():
    chid = '4.2' # this has a large gap to truth because first 3 papers are droping fast then,
    #  chid = '4'
    #chid = '7'
    truetopk,s = LoadS(chid)
    topk1 = SplitArray(s,mode = 'top')
    topk2 = SplitArray(s, mode='lefthalf')
    topk3 = sxpLinearReg.TestLinearRegFit(s)
    topk4 = sxpLinearReg.TestVARFit(s)
    topk5 = sxpLinearReg.LinearFitLeft(s,draw=True,truetopk=truetopk)
    topk6 = MaxGap(s)
    a = [truetopk,topk1, topk2, topk3, topk4, topk5,topk6]
    print('truetopk','top','lefthalf','TestLinearRegFit','TestVARFit','LinearFitLeft','MaxGap')
    print(a)
    ds = MyDiff(s,True)
    fname3 = 'math.jpg'
    sxpPlotBar.plotlinelist([s, ds], ['s', 'ds'], title='topk',fname = fname3
                            , vline = [truetopk,topk4])

def TestAllS():
    doclist = LoadAllS()
    n = len(doclist)
    truelist= []
    top1list =[]
    top2list =[]
    top3list = []
    top4list = []
    topklist =[]
    for i,each in enumerate(doclist):
        truetopk = each[0]
        s = each[1]
        fname = each[2]
        topk1 = SplitArray(s, mode='top')
        topk2 = SplitArray(s, mode='lefthalf')
        #topk3 = sxpLinearReg.TestLinearRegFit(s)
        #topk3 = sxpLinearReg.VarMaxSplit(s)
        topk3 = ArgMinSD(s)
        topk4 = sxpLinearReg.LinearFitLeft(s)
        topk5 = sxpLinearReg.AvgGapMax(s)
        truelist.append(truetopk)

        a = [topk1,topk2,topk3,topk4,topk5]
        topklist.append(a)
        print('true,topk1,topk2,topk3,topk4,topk5',truetopk,a,fname)

    k = len(a)
    tname =[
        'top','toplefthalf','ArgMinSD','LinearFit','AvgGapMax'
    ]
    d = [np.array(truelist).reshape(-1,1)]
    dname=['true']
    ta = np.array(topklist)
    for i in range(k):
        topkilist=ta[:,i].reshape(-1,1)
        dist = computediff(truelist,topkilist)
        print('topk model:{0}'.format(i),tname[i],dist)
        d.append(topkilist)
        dname.append(tname[i])
    fname3 = 'topk1.jpg'
    sxpPlotBar.plotlinelist(d, dname, title='sum word len'
                            , fname=fname3)
    #
    # t1='true'
    # t2 = 'top'
    # t3 = 'top-lefthalf'
    # d1 = np.array(truelist).reshape(-1,1)
    # d2 = np.array(top1list).reshape(-1, 1)
    # d3 = np.array(top2list).reshape(-1, 1)
    # d4 = np.array(top3list).reshape(-1, 1)
    # d5 = np.array(top4list).reshape(-1, 1)
    # sxpPlotBar.plotlinelist([d1, d2, d3,d4,d5], ['true','top','top-lefthalf','VAR','LR',], title='sum word len'
    #                         , fname=fname3)
def computediff(nd1,nd2):
    d1 = np.array(nd1).reshape((-1,1))
    d2 = np.array(nd2).reshape((-1, 1))
    nd = 1/d1
    diff = (d2 - d1)*nd #d1 is true
    diff_dict={}
    absdiff = np.abs(d1 - d2)*nd
    diff_dict['avg'] = np.mean(diff, 0)
    diff_dict['va'] = np.std(diff, 0)
    diff_dict['aavg'] = np.mean(absdiff, 0)
    diff_dict['ava'] = np.std(absdiff, 0)
    return diff_dict
def main():
    #testtop3()
    cmd = ['TestAllS']
    if 'TestS' in cmd:
        TestS()
    if 'TestAllS' in cmd:
        TestAllS()
    #LoadAllS()
    #TestAllS()
if __name__ == '__main__':
    main()
