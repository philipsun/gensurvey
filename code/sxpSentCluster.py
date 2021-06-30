#coding=utf-8
#-------------------------------------------------------------------------------
# Name:        ****
# Purpose:
#
# Author:      Sun Xiaoping
#
# Created:     03/10/2020
# Copyright:   (c) sunxp 971994252@qq.com 2020
# Licence:     <mit licence>
#-------------------------------------------------------------------------------
import sxpFenciMakeTFIDF
from nltk.corpus import reuters
import numpy as np
import matplotlib.pyplot as plt
from time import time

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import NMF

import somePLSAV
import sxpExtractText
import gensim
from gensim import corpora, models, similarities
from collections import defaultdict

def preparedata(sentlist):
    doclist =[]
    for s in sentlist:
        doc = [s]
        doclist.append(s)
    rt_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(doclist)
    data = rt_tfidf.ct.toarray()
    return data
def cluster_sent(sentlist,ncluster=2,method='kmeans'):
    data = preparedata(sentlist)
    predict = []
    if method=='kmeans':
        predict=kmeansclustersentdoc(data,ncluster)
    cluster_sent_dict,cluster_idxdict = maplabeltosent(predict,sentlist)
    return cluster_sent_dict,cluster_idxdict
def kmeansclustersentdoc(data,ncluster):

    km =  sxpKMeans(data,ncluster,initstr = 'random')
    predict_labels = np.array(km.labels_, copy=True)
    return predict_labels
def maplabeltosent(predict_labels,sentlist):
    ulabels = np.unique(predict_labels)

    cluster_idxdict={}
    cluster_sent_dict ={}
    for ui in ulabels:
        uipos = np.where(predict_labels == ui)
        idx = list(uipos[0]) #using 0 because predict_labels is (n,) shape, only the 0 dim is used
        ##        print idx[0]
        cluster_idxdict[ui] = idx
        sentcluster =[]
        for i in idx:
            sentcluster.append(sentlist[i])
        cluster_sent_dict[ui]=sentcluster
    
    return cluster_sent_dict,cluster_idxdict
def sxpKMeans(tfidf,ncluster,initstr = 'random'):
    kmeans = KMeans(init=initstr, n_clusters=ncluster, n_init=20)
    return kmeans.fit(tfidf)
def test():
    sentlist = [
        'hello, i am ok',
        'good, i am ok two',
        'how old are you',
        'i am 3 years old'
    ]
    cluster_sent_dict,cluster_idxdict = cluster_sent(sentlist,2)
    for ui,sentcluster in cluster_sent_dict.items():

        print('----',ui)
        print(sentcluster)
def main():

    test()

if __name__ == '__main__':
    main()
