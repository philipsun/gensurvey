#coding=UTF-8

from numpy import linalg as LA

import numpy as np

import sxpMathTest
def DecrAvgRank(s):
    s.reshape(-1,1)
    n,c = s.shape
    movg =np.zeros((n-1,1))
    for i in range(1,n):
        rg = np.mean(s[0:i],0)
        movg[i-1,0]=rg[0]
    return movg
def RemoveEntropy(s):
    s.reshape(-1,1)
    n,c = s.shape
    ts = s.copy()
    removeE =np.zeros((n-1,1))
    for i in range(1,n):
        rg = np.mean(ts[i:n],0)
        rg = rg[0]
        ts[0:i]=rg
        e = Entropy(ts)
        removeE[i-1,0]=e
    return removeE
def AvgRankRemoveEntropy(s):
    dr = normalization(DecrAvgRank(s),'max')
   # reomveEntropy =RemoveEntropy(s)
    ds = normalization(Diff(s,ae = True)*-1,'01sum')
    nle = normalization(RemoveEntropy(ds),'01sum')
    tot = dr + nle
    # print('AvgRankRemoveEntropy')
    # print('AvgRankRemoveEntropy s',s)
    # print('AvgRankRemoveEntropy dr',dr)
    # print('AvgRankRemoveEntropy nle',nle)

    return dr,nle,tot
def SelectTopk(tot):
    df = Diff(tot,False)
    n,c = df.shape
    for i in range(1,n):
        if (df[i-1]*df[i])<=0:
            return i
    return 1
def SelectTopkByScoreRank(s,mode = 'top'):
    ds = np.diff(s,0)
    topk = sxpMathTest.SplitArray(s,mode = 'left')
    return max(topk+1,1)



def HistRankOptimize(s):
    ds = np.diff(s,0)
  #  ds.reshape((-1,1))
    nr,nc = ds.shape
    nb = np.log2(nr)
    nb = np.power(nr,0.5)
    bsize = int(np.ceil(nb+1))
    eb,cb_avg = EntropCurvAtBin(s,ds, bsize)
    tot = eb + cb_avg
    return eb,cb_avg,tot
def EntropCurvAtBin(s,ds,nb):

    #  ds = np.diff(s)
    nd = normalization(ds)
    nr,nc = nd.shape

    # nb = np.log2(nc)
    # #bsize = int(np.ceil(nb+1))

    #nb = nc *2/ 4;
    #nb = np.log2(nc)
    #nb = np.power(nc,0.5)
    bsize = int(np.ceil(nb+1))
    bn = bsize

    cbin_prob, cbin_avg, bin_list = MakeBin(s, bn)
    print("cbin_prob, cbin_avg")
    print(s.shape,s)
    print(cbin_prob.shape,cbin_prob)
    print(cbin_avg.shape,cbin_avg)
    avg_decr=AvgRankDecre(cbin_avg)
    eb = EntropyCurve(cbin_prob)
    return eb,avg_decr

def AvgRankDecre(r):
    n,c = r.shape;
    avglist=[]
    for i in range(1,n-1):
        c = r[0:i,0]
        avglist.append(np.mean(c,0))
    if len(avglist) <=1:
        avg = r;
    else:
        avg = normalization( np.array(avglist).reshape((-1,1)),'01sum')
    return avg
def EntropyCurve(ss):
    # std = standardization(ds)
    ts=[]
    for sm in ss.ravel():
     ts.append(sm)
    #ds = np.diff(ss,0).reshape((-1,1))
    ds = np.diff(ts).reshape(-1, 1)
    ds = normalization(ds,'01sum')
    nr,nc = ds.shape
    s = np.ones((nr,1))
    for i in range(0,nr):
        et = Entropy(ds[i:nr,0])
        s[i,0]=et
    s = s.ravel()
    print("EntropyCurve(s)",s)
    de = normalization(np.diff(s),'01sum')
    return de.reshape((-1,1))
def Entropy(p):
    nozero = p[p!=0]
    if len(nozero)==0:
        return 0
    e = np.multiply(nozero, np.log2(nozero))
  #  print(e,e.shape)
    s = np.sum(e)*-1
    return s;
def normalization(data,norm='sum'):
    data.reshape((-1,1))
    if norm=='max':
        _range = LA.norm(data,0,0)
    if norm == 'range':
        _range = np.max(data) - np.min(data)
    if norm == 'sum':
        _range=np.sum(data)
    if norm == '01sum':
        _range=np.sum(data - np.min(data))
    if _range == 0:
        return data
    r= (data - np.min(data)) / _range
    return r.reshape((-1,1))

# ord	norm for matrices	norm for vectors
# None	Frobenius norm	2-norm
# ‘fro’	Frobenius norm	–
# ‘nuc’	nuclear norm	–
# inf	max(sum(abs(x), axis=1))	max(abs(x))
# -inf	min(sum(abs(x), axis=1))	min(abs(x))
# 0	–	sum(x != 0)
# 1	max(sum(abs(x), axis=0))	as below
# -1	min(sum(abs(x), axis=0))	as below
# 2	2-norm (largest sing. value)	as below
# -2	smallest singular value	as below
# other	–	sum(abs(x)**ord)**(1./ord)
def MakeBin(s,binnum):
    s.reshape((-1, 1))
    s = normalization(s,'01sum')
    ds = np.diff(s,0)

    h = np.array(ds[0,0]).reshape(-1,1)
  #  ds = np.vstack((h,ds))
    n,c = ds.shape

    binsize = int(np.ceil(n / binnum))
    print("s.shape,n,c,binsize",s.shape,n,c,binsize)
    cbin = []
    cbin_avg = []
    bin_list = []
    bini = binsize
    cbin_count = []
    cbin_prob = []
    tot = np.sum(s,0)
    for i in range(int(n)):
        if i <= bini:
            cbin.append(i)
        else:
            cbin.append(i)
            if np.sum(s[cbin],0)[0]<=0.0:
                break;
            bini = bini + binsize
            bin_list.append(cbin)
            cbin_count.append(len(cbin))
            #cbin_prob.append(len(cbin)*1.0/n)
            cbin_prob.append(np.sum(s[cbin],0)[0]/tot)
            cbin_avg.append(np.mean(s[cbin],0))
            cbin = []
    if len(cbin)>0:
        bin_list.append(cbin)
      # print('cbin',cbin)
        #cbin_prob.append(len(cbin) * 1.0 / n)
        cbin_prob.append(np.sum(s[cbin], 0)[0] / tot)
        cbin_avg.append(np.mean(s[cbin], 0))
        cbin_count.append(len(cbin))
    cbin_prob = np.array(cbin_prob).ravel().reshape(-1,1)
    cbin_avg = np.array(cbin_avg).reshape(-1,1)
 #   print('cbin_prob','cbin_avg',cbin_prob,cbin_avg,cbin_prob.shape,cbin_avg.shape)
  #  bin_list = np.array(cbin_avg).reshape(-1,1)
    print('cbin_prob',cbin_prob.shape,cbin_prob)
    return cbin_prob,cbin_avg,bin_list
def standardization(data):
    data.reshape((-1,1))
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma
def Diff(s,ae = True):
    ds = np.diff(s.ravel()).reshape(-1,1)*-1
    if ae:
        ds = np.vstack((ds,[s[-1,0]]))
    return ds