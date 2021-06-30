from sklearn import linear_model
import numpy as np
import sxpPlotBar
import os
import sxpReadFileMan
import sxpMetricScore
def LinearRegAccuracy(s,targets):
    n,r = s.shape
    x = range(0,n)
    X_train = np.array(x).reshape((n,-1))
    LR = linear_model.LinearRegression()
    LR.fit(X_train, s)
    tn,r = targets.shape
    nx = range(tn)
    X_test = np.array(nx).reshape((tn,1))
    score = LR.score(X_test, targets)
    return score
def MaxAccLR(s, startseg = 3):
    n,r = s.shape
    acc_list = []
   # startseg = 3;
    for k in range(startseg,n):
        seg = s[0:k,0].reshape((-1,1))
        acc_list.append(LinearRegAccuracy(seg,seg))
    ds = np.array(acc_list).reshape((-1,1))
    n,r = ds.shape
    ds = ds[0:n,0].reshape((-1,1))
    acindex = np.argsort(-ds,0).reshape((-1,1))
    top = acindex[0,0] +startseg;

    return acc_list,top
def GetLinearPeak(acclist):
 #   ds = np.array(acclist).reshape((-1, 1))


    ds = MyDiffList(acclist)
    acindex = np.argsort(-ds,0).reshape((-1,1))
    n,r = ds.shape
    minpoint = []
    dec = True
    maxtrue = True;
    maxpoint = []
    if ds[0,0]<0:
        beingdown = True
        maxpoint.append(0)
    else:
        beingdown = False;
        minpoint.append(0)
    for i in range(n):
        if ds[i,0] < 0:
            if beingdown==False:
                maxpoint.append(i)
                beingdown = True;
        else:
            if beingdown==True:
                minpoint.append(i)
                beingdown = False
    if beingdown:
        minpoint.append(i)
    else:
        maxpoint.append(i)
    return maxpoint,minpoint,ds,acindex
def LinearRegFitHead(s,granularity=0.4):
    startseg = 3
    acc_list, top = MaxAccLR(s,startseg=startseg)
    top = top - startseg #here top is the index in acc_list,not in the whole range of s
    maxpoint, minpoint, ds, acindex=GetLinearPeak(acc_list)
    ln,r = s.shape
    topidx = acindex[0,0]
    n = len(maxpoint)
    seltop = topidx
    cmax =maxpoint[0]
    maxcov = ln*granularity
    for i in range(n):
        if maxpoint[i]>=top:
            seltop = top
            break
        dist = abs(cmax - maxpoint[i])
        if IsClose(dist,maxcov):
            seltop = cmax
            break

        if i >= n-1:
            break;
        if acc_list[maxpoint[i+1]] >= acc_list[cmax]:
            cmax=maxpoint[i+1]
        else:
            cov = abs(cmax-maxpoint[i+1]) #how current max is close to a maximum
            closeness = cov/ln
            if closeness <= 0.08:
                if TryProb(ln,ln-abs(cov)):
                    cmax = maxpoint[i + 1]
                else:
                    continue
            else:
                continue


    return seltop + startseg

def VarMaxSplit(s,startseg=3):
    n, r = s.shape
    acc_list = []
    # startseg = 3;
    for l in range(startseg, n):
        seg = s[0:l, 0].reshape((-1, 1))
        acc_list.append(np.std(seg,0))
    ds = np.array(acc_list).reshape((-1, 1))
    n, r = ds.shape
    ds = ds[0:n, 0].reshape((-1, 1))
    acindex = np.argsort(-ds, 0).reshape((-1, 1))
    top = acindex[0, 0] + startseg;

    return top
def TestVarMaxSplit(s,startseg=3):
    n, r = s.shape
    acc_list = []
    # startseg = 3;
    for l in range(startseg, n):
        seg = s[0:l, 0].reshape((-1, 1))
        acc_list.append(np.std(seg,0))
    ds = np.array(acc_list).reshape((-1, 1))
    n, r = ds.shape
    ds = ds[0:n, 0].reshape((-1, 1))
    acindex = np.argsort(-ds, 0).reshape((-1, 1))
    top = acindex[0, 0] + startseg;

    return acc_list,top
def LinearFitTP(s,draw=False,truetopk=1):
    startseg =3
    acc_list, top = MaxAccLR(s,startseg=startseg)
    top = top - startseg #here top is the index in acc_list,not in the whole range of s

    a = np.array(acc_list).reshape((-1,1))
    ds = MyDiff(a,abs_mode=True)
    peak,valey = FindPeak(a)
    top = max(peak[0],valey[0]) + 1
    if draw:

        fname3 = 'linearfitleft.jpg'
        sxpPlotBar.plotlinelist([s, a, ds], ['rank','lrscore', 'grd'], title='LinearRegressionErrFit', fname=fname3
                                , vline=[truetopk, top])
    if top <=0:
        top = 1
    return top
def evaluate(truth_fid,predict_topk):
    return sxpMetricScore.precisionat_topk(predict_topk, truth_fid, topk=-1)
def LinearFitLeft(s,draw=False,truetopk=1):
    startseg =4
    acc_list, top = MaxAccLR(s,startseg=startseg)
    top = top - startseg #here top is the index in acc_list,not in the whole range of s
    maxpoint, minpoint, ds, acindex=GetLinearPeak(acc_list)

    if draw:
        y = np.array(acc_list).reshape((-1,1))
        fname3 = 'linearfitleft.jpg'
        sxpPlotBar.plotlinelist([s, y, ds], ['rank','lrscore', 'grd'], title='LinearRegressionErrFit', fname=fname3
                                , vline=[truetopk, top])

    ln,r = s.shape
    topidx = acindex[0,0]
    n = len(maxpoint)
    seltop = topidx
    cmax =maxpoint[0]

    maxcov = ln*0.1
    spliter = cmax;
    for i in range(n):
        if maxpoint[i]>=top:
            spliter = top
            break
        if i == n-1:
            spliter = top
            break
        if acc_list[maxpoint[i+1]] >= acc_list[cmax]:
            if abs(cmax - maxpoint[i+1])>maxcov:
                break;
            else:
                cmax=maxpoint[i+1]
                spliter = cmax
        else:
            cov = abs(cmax - maxpoint[i+1])
            if cov < maxcov:
                spliter = maxpoint[i+1]
                maxcov = maxcov /2;

    return max(int(np.ceil((spliter+ startseg)/2)),1)
    # return max(int(np.ceil(spliter-1)),1)


def AvgGapMax(s, draw=False, truetopk=1):
    n, c = s.shape
    if n <= 2:
        return n
    dav = []
    nmax = -1
    maxid = [0]
    for i in range(1,n):
        if i <n-1:
            s1=s[:i,:]
            s2 = s[i:,:]
            av1 = np.mean(s1,0)
            av2 = np.mean(s2,0)
            d = av1 - av2
            dav.append(d)
            if d >= nmax:
                nmax = d;
                maxid.append(i)
        else:
            d = np.mean(s,0)
            if d >= nmax:
                nmax = d
                maxid.append(i)
            dav.append(d)
    return maxid[-1]

def IsClose(d1,d2):
    if abs(d2-d1)/d2 >0.10:
        return False
    if TryProb(d2,d2-abs(d2-d1)):
        return True
    return False
def TryProb(maxrange,v):
    p = v/maxrange
    return np.random.rand() <=p
def LinearRegFit(s):
    acc_list,top = MaxAccLR(s)
    return top
def TestLinearRegFit(s):
    acc_list,top = MaxAccLR(s)

    fname3 = 'lineareg.jpg'
    ls = np.array(s).reshape((-1,1))
    acc_list = np.array(acc_list).reshape((-1,1))
    sxpPlotBar.plotlinelist([acc_list], [ 'acc'], title='test',fname = fname3
                            , vline = [])
    sxpPlotBar.plotlinelist([ls], ['s'], title='test', fname=fname3
                            , vline=[top])
    return top
def TestMaxGap(s):
    ds = MyDiff(s)

def TestVARFit(s):
    acc_list,top = TestVarMaxSplit(s)

    fname3 = 'lineareg.jpg'
    ls = np.array(s).reshape((-1,1))
    acc_list = np.array(acc_list).reshape((-1,1))
    sxpPlotBar.plotlinelist([acc_list], [ 'acc'], title='var line',fname = fname3
                            , vline = [])
    sxpPlotBar.plotlinelist([ls], ['s'], title='ls and s', fname=fname3
                            , vline=[top])
    return top
def MyDiff(s,abs_mode=False):
    ds = np.diff(s.ravel()).reshape(-1, 1)
    if abs_mode:
        ds = np.abs(ds)
    return ds
def MyDiffList(s,abs_mode=False):
    ds = np.diff(s).reshape(-1, 1)
    if abs_mode:
        ds = np.abs(ds)
    return ds
def MaxSegTopk(s):
    if isinstance(s,list):
        a = np.array(s)
    else:
        a = s
    if len(a)<=2:
        return 1
    df = MyDiff(a,abs_mode=True)
    topk = np.argmax(df,0)[0] + 1
    return topk
def MaxDiffTurnPointTopk(s):
    if isinstance(s,list):
        a = np.array(s)
    else:
        a = s
    if len(a)<=2:
        return 1
    df = MyDiff(a,abs_mode=True)
    topk = np.argmax(df,0)[0] + 1
    return topk
def InfelctionPointTopk(s):
    if isinstance(s,list):
        a = np.array(s).reshape((-1,1))
    else:
        a = s.reshape((-1,1))
    if len(a)<=2:
        return 1
    # g1 = np.gradient(a, axis=0, edge_order=1)
    #
    # g2 = np.gradient(a, axis=0, edge_order=2)

    df = MyDiff(a,False)
    # ddf = MyDiff(df,False)
    # fname3 = 'lineareg.jpg'
    # sxpPlotBar.plotlinelist([a], [ 'ls'], title='test',fname = fname3
    #                         , vline = [])
    # sxpPlotBar.plotlinelist([df], [ 'df'], title='test',fname = fname3
    #                         , vline = [])
    # sxpPlotBar.plotlinelist([ddf], [ 'ddf'], title='test',fname = fname3
    #                         , vline = [])

    peak,valey= FindPeak(df)
    #print(peak,valey)
    return peak[0]+1



    # sxpPlotBar.plotlinelist([g1], [ 'g1'], title='test',fname = fname3
    #                         , vline = [])
    # sxpPlotBar.plotlinelist([g2], [ 'g2'], title='test',fname = fname3
    #                         , vline = [])

    #print(g1)
    #print(g2)

def FindPeak(s):
    n,c = s.shape

    peak =[]
    valey =[]
    zm = []
    if n<=2:
        if s[0,0]<s[1,0]:
            peak=[0]
            valey=[1]
        if s[0,0]>s[1,0]:
            peak =[1]
            valey=[0]
        if s[0,0]==s[1,0]:
            peak = [0,1]
            valey = [0,1]
        return peak,valey
    for i in range(n):
        lefti = i - 1
        if lefti < 0:
            if s[i,0] < s[i+1,0]:
                valey.append(i)
            if s[i,0] > s[i+1,0]:
                peak.append(i)
            continue
        righti = i + 1
        if righti >=n:
            righti = n-1
            if s[i,0]> s[i-1,0]:
                peak.append(i)
            if s[i,0]< s[i-1,0]:
                peak.append(i)
            continue
        if s[i,0] > s[lefti,0] and s[i,0] >= s[righti,0]:
            peak.append(i)
        if s[i,0] < s[lefti,0] and s[i,0] <= s[righti,0]:
            valey.append(i)
    if len(peak) == 0:
        peak =[0]
    if len(valey)==0:
        valey=[0]
    return peak,valey
def testgrad():
    ls = [16, 13, 12, 10, 5, 4, 3, 0, 0, 0, 0, 0]
    #ls = [1, 2,3]
    InfelctionPointTopk(ls)
def Test():
    #ls = [7, 5, 4, 3, 0, 0, 0, 0, 0]
    #ls = [10, 5, 4, 3, 0, 0, 0, 0, 0]

    ls = [16,13,12,10, 5, 4, 3, 0, 0, 0, 0, 0]
    topk_max = MaxSegTopk(ls)

    infpoint = InfelctionPointTopk(ls)
    print(infpoint)
    maxpoint,minpoint,ds,acindex=GetLinearPeak(ls)

    print(maxpoint,minpoint)

    s = np.array(ls).reshape((-1,1))
    acc_list,top = MaxAccLR(s)

    maxpoint,minpoint,ds,acindex=GetLinearPeak(acc_list)

    print(maxpoint,minpoint)

    fname3 = 'lineareg.jpg'
    ls = np.array(ls).reshape((-1,1))


    # sxpPlotBar.plotlinelist([ds], [ 'ds'], title='test',fname = fname3
    #                         , vline = [])
    topk4 = LinearRegFit(ls)

    topk5 = AvgGapMax(ls)
    print('LinearRegFitHead',topk4)
    acc_list = np.array(acc_list).reshape((-1,1))
    sxpPlotBar.plotlinelist([ls], [ 'ls'], title='test',fname = fname3
                            , vline = [topk_max])

    sxpPlotBar.plotlinelist([acc_list], [ 'acc'], title='test',fname = fname3
                            , vline = [])
    sxpPlotBar.plotlinelist([ls], ['s'], title='test', fname=fname3
                            , vline=[topk4,top,topk_max])
    sxpPlotBar.plotlinelist([ls], ['s'], title='test', fname=fname3
                            , vline=[topk5])
def main():
    Test()
    #testgrad()
if __name__ == '__main__':
    main()
