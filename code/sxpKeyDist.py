#-------------------------------------------------------------------------------
# Name:        sxpSGTree.py
# Purpose:
#
# Author:      sunxp
#
# Created:     10/31/2019
# Copyright:   (c) sunxp 2019
# Licence:     <MIT>
#-------------------------------------------------------------------------------
#coding=UTF-8

import numpy as np
import sxpReadFileMan
import sxpJudgeCharacter
import Levenshtein


import os
basedir = os.path.abspath(os.path.dirname(__file__))
#this is to replace the host url

def sortlistidxbywt(a,reverse=False):
    i = list(range(len(a)))
    sai = sorted(i, key=lambda k: a[k], reverse=reverse)
    return sai
def sortlistbywt(a,oblist,reverse=False):
    i = list(range(len(a)))
    sai = sorted(i, key=lambda k: a[k], reverse=reverse)
    sa = [a[i] for i in sai]
    sob = [oblist[i] for i in sai]
    return sa,sob
def sortlist(a,reverse=False):
    i = list(range(len(a)))
    sai = sorted(i, key=lambda k: a[k], reverse=reverse)
    sa = [a[i] for i in sai]
    return sai,sa

def dg(sent,keywordpath):
    ks = dd(sent,keywordpath)
 #   print(ks)
    return normdg(ks)
def dl(sent,keywordpath):
    ks = dd(sent,keywordpath)
    return normdl(ks)
#compute general path distance
def dd(sent,keywordpath):
    ss = sxpJudgeCharacter.segsenttowords(sent.lower())
    if len(ss)==0:
        return 1
    ds = []
    for i, ks in enumerate(keywordpath):
        edlist=[]

        for sw in ss:
            if len(sw)==0:
                ed = 0
            else:
                #ed=Levenshtein.distance(ks, sw)
                ed = strjaccard(ks,sw)
            edlist.append(ed)
        mind= min(edlist) #each word is compared with the keyword and use the closet one
        maxd = max(edlist)
      #  ds.append(mind*1.0/maxd)
        ds.append(mind)
    #how each keyword in keywordpath is matched by this sent the more match the less dist.
    return ds
def normdg(ks):
    vs = np.array(ks) * 1.0
    n = len(ks)
    mx = np.max(ks)
    ms = np.min(ks)
    st = (mx - ms) * 1.0 / n
    if st == 0:
        w  = np.ones((n,))
    else:
        w = np.arange(mx, ms, -st)
        w = w[0:n]
        w = np.power(w / np.sum(w), 2)
    w = w / np.sum(w)
    # if len(w)!=n:
    #     print(w,vs)
    #w = w[0:n]
    ss =np.sum( np.dot(vs , w))
    #   ss = ss / np.sum(ss)
    return ss
#compute detailness path distance
def normdl(ks):
    vs = np.array(ks) * 1.0
    n = len(ks)
    mx = np.max(ks)
    ms = np.min(ks)
    st = (mx - ms) * 1.0 / n
    if st == 0:
        w  = np.ones((n,))
    else:
        sw = np.arange(ms, mx, st)
        sw =sw[0:n]
        ew = np.power(sw / np.sum(sw), 2)
        w = ew / np.sum(ew)
    if len(w)!=n:
        print((ms,mx,st,sw,ew,w,vs))
    ss = np.sum( vs * w)
    #   ss = ss / np.sum(ss)
    return ss
def testdist():
    sent1 = "hello this is a survey"
    sent2 = "hello this is a keyword survey"
    keypath = ['survey','keyword']
    print((sent1,dg(sent1,keypath)))
    print((sent2,dg(sent2,keypath)))
def strjaccard(s1,s2):
    u=[]
    n=[]
    c1=[]
    c2=[]
    for c in s1:
        if c in s2:
            n.append(c)
        else:
           c1.append(c)
    for c in s2:
        if c in s1:
           continue
        else:
            c2.append(c)
    d1=  len(n)*1.0/len(s1)
    d2 = len(n)*1.0/len(s2)
    dd = 1.0-len(n)*1.0/(len(c1)+len(c2)+len(n))
    return dd
def main():
    testdist()

if __name__ == '__main__':
    main()
