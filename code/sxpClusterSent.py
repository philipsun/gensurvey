#coding=UTF-8
#-------------------------------------------------------------------------------
# Name:        sxpClusterText
# Purpose:
#
# Author:      sunxp
#
# Created:     23-05-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
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


def TestPLSA():
    print(reuters.categories())
    doctype = ['corn','acq','barley']
    groundtruth = []
    doc_set = []
    setbound = 20
    cat = 0
    for dt in doctype:
        ds =reuters.fileids(dt)
        for fid in ds[0:setbound]:
            groundtruth.append(cat)
            file_cat = reuters.categories(fid)
            rawstr= reuters.raw(fid)
            ur = str(rawstr)
            doc_set.append(ur)
        cat =   cat + 1
    agrdtruth = np.array(groundtruth)

    rt_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(doc_set)

    ncluster = 3
    ntopic= 10
    data = rt_tfidf.ct.toarray()

    plsa = somePLSAV.pLSA()
    print('begin to train plsa')
    t0 = time()
    plsa.train(data.T,ntopic)
    topic_doc = plsa.document_topics()
    initstr ='random'
    kmeans = KMeans(init=initstr, n_clusters=ncluster, n_init=20)
    km = kmeans.fit(topic_doc.T)
    BenchmarkA(data,'pLSA_topic',agrdtruth,km,t0)

def TestNMF():
    print(reuters.categories())
    doctype = ['corn','acq','barley']
    groundtruth = []
    doc_set = []
    setbound = 20
    cat = 0
    for dt in doctype:
        ds =reuters.fileids(dt)
        for fid in ds[0:setbound]:
            groundtruth.append(cat)
            file_cat = reuters.categories(fid)
            rawstr= reuters.raw(fid)
            ur = str(rawstr)
            doc_set.append(ur)
        cat =   cat + 1
    agrdtruth = np.array(groundtruth)

    rt_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(doc_set)

    ncluster = 3
    ntopic= 10
    data = rt_tfidf.tfidf.toarray()

    t0 = time()
    estimator1 = sxpNMF(rt_tfidf,data,ntopic, ncluster,initstr = 'random')
    BenchmarkA(data,'NMF_topic',agrdtruth,estimator1,t0)
def sxpNMF(rt_tfidf,data,ntopic, ncluster,initstr = 'random'):
    n_top_words = 20
    nmf = NMF(n_components=ntopic, random_state=1).fit(data)
    feature_names = rt_tfidf.word
    topic_word = nmf.components_
    for topic_idx, topic in enumerate(nmf.components_):
        print(topic_idx)
        print((topic.shape))
        print(("Topic #%d:" % topic_idx))
        print((" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]])))
        print()
    doc_topic = np.dot(data,topic_word.T)
    kmeans = KMeans(init=initstr, n_clusters=ncluster, n_init=20)
    return kmeans.fit(doc_topic)

def sxpKMeans(tfidf,ncluster,initstr = 'random'):
    kmeans = KMeans(init=initstr, n_clusters=ncluster, n_init=20)
    return kmeans.fit(tfidf)
def sxpPCAKmeans(tfidf,pcanum, ncluster,initstr='k-means++'):
    reduced_data = PCA(n_components=pcanum).fit_transform(tfidf)
    kmeans = KMeans(init=initstr, n_clusters=ncluster, n_init=20)
    return kmeans.fit(reduced_data)

def sxpTruncSVD(tfidf, comnum, ncluster,initstr = 'random'):
    svd = TruncatedSVD(n_components=comnum, random_state=42)
    reduced_data = svd.fit_transform(tfidf)
    kmeans = KMeans(init=initstr, n_clusters=ncluster, n_init=20)
    return kmeans.fit(reduced_data)


def Benchmark(data,name,groundtruth,estimator, t0):
    sample_size = None
    print(('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(groundtruth, estimator.labels_),
             metrics.completeness_score(groundtruth, estimator.labels_),
             metrics.v_measure_score(groundtruth, estimator.labels_),
             metrics.adjusted_rand_score(groundtruth, estimator.labels_),
             metrics.adjusted_mutual_info_score(groundtruth,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size))))
    glab = MatchClusterTrue(groundtruth,estimator.labels_)
    pr,rec,fm,sp =metrics.precision_recall_fscore_support(groundtruth, glab, average='micro')
    print((' f: %.3f   %.3f   %.3f '
          %( pr,rec,fm)))
def BenchmarkA(data,name,groundtruth,estimator, t0):
    sample_size = None
    glab = MatchClusterTrue(groundtruth,estimator.labels_)
    print(('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(groundtruth, glab),
             metrics.completeness_score(groundtruth, glab),
             metrics.v_measure_score(groundtruth, glab),
             metrics.adjusted_rand_score(groundtruth, glab),
             metrics.adjusted_mutual_info_score(groundtruth,  glab),
             metrics.silhouette_score(data, glab,
                                      metric='euclidean',
                                      sample_size=sample_size))))
    pr,rec,fm,sp =metrics.precision_recall_fscore_support(groundtruth, glab, average='micro')
    print((' f: %.3f   %.3f   %.3f '
          %( pr,rec,fm)))
def TestFreqCount():
    data= np.array([1, 1, 3, 3, 2, 5])
    print(FreqCount(data))
def FreqCount(data):
    uq = np.unique(data)
    ct = []
    for u in uq:
        nb =(data == u).sum()
        ct.append(nb)
    a = np.array(ct)
    sidx = np.argsort(-a, axis=0)
    sct = a[sidx]
    uq = uq[sidx]
    return sct,uq
def MatchClusterTrue(groundtruth, predict_labels):
    ulabels = np.unique(predict_labels)
    npred = np.array(predict_labels,copy=True)
    for ui in ulabels:
        idx = np.where(predict_labels == ui)
##        print idx[0]
        trc = groundtruth[idx[0]]
        sct,labels = FreqCount(trc)
        npred[idx] = labels[0]
       # print npred[idx]
    return npred

def TestReuter():
    print(reuters.categories())
    corn= reuters.fileids('corn')
    bank =reuters.fileids('acq')
    groundtruth = []
    cat = 0
    doc_set = []
    setbound = 20
    for fid in corn[0:setbound]:
        groundtruth.append(cat)
        file_cat = reuters.categories(fid)
        rawstr= reuters.raw(fid)
        doc_set.append(rawstr)
    cat =   cat + 1
    for fid in bank[0:setbound]:
        groundtruth.append(cat)
        file_cat = reuters.categories(fid)
        rawstr= reuters.raw(fid)
        doc_set.append(rawstr)
    rt_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(doc_set)
    print(rt_tfidf.ct.shape)
def TestReuterSet():
    print(reuters.categories())
    doctype = ['corn','acq','barley']
    groundtruth = []
    doc_set = []
    setbound = 20
    cat = 0
    for dt in doctype:
        ds =reuters.fileids(dt)
        for fid in ds[0:setbound]:
            groundtruth.append(cat)
            file_cat = reuters.categories(fid)
            rawstr= reuters.raw(fid)
            ur = str(rawstr)
            doc_set.append(ur)
        cat =   cat + 1

    rt_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(doc_set)
    data = rt_tfidf.ct.toarray()
   # print rt_tfidf.word
##    print (data==np.Inf).sum()
##    print (data==np.NaN).sum()
##    print (data==np.NAN).sum()
##    print (data==0).sum()
##    print data.shape
##    print (data>0).sum()

    print((79 * '_'))
    print(('% 9s' % 'init'
          '    time  inertia    homo   compl  v-meas     ARI AMI  silhouette'))
    data = rt_tfidf.tfidf.toarray()
    docn,keywordn = data.shape
    ncluster = len(doctype)
    agrdtruth = np.array(groundtruth)
##    print (data==np.Inf).sum()
##    print (data==np.NaN).sum()
##    print (data==np.NAN).sum()
##    print (data==0).sum()
##    print data.shape
    print((data>0).sum())

    t0 = time()
    estimator = sxpKMeans(data,ncluster,initstr = 'random')
    BenchmarkA(data,'kmean_random',agrdtruth,estimator,t0)

    t0 = time()
    estimator = sxpKMeans(data,ncluster,initstr = 'k-means++')
    BenchmarkA(data,'kmean++',agrdtruth,estimator,t0)

    pcanum = 50
    t0 = time()
    estimator1 = sxpTruncSVD(data,pcanum, ncluster,initstr = 'k-means++')
    BenchmarkA(data,'TrunctSVD',agrdtruth,estimator1,t0)

    pcanum = 20
    data0 =rt_tfidf.tfidf.toarray()
    print('sxpPCAKmeans starts')
##    print (data0==np.Inf).sum()
##    print (data0==np.NaN).sum()
##    print (data0==np.NAN).sum()
##    print (data0==0).sum()
##    print data0.shape
##    print (data0>0).sum()
    t0 = time()
    estimator2 = sxpPCAKmeans(data0,pcanum, ncluster)
    print('benchmark starts')
    BenchmarkA(data,'kmean_pca',agrdtruth,estimator2,t0)
def TestLSI():
    print(reuters.categories())
    doctype = ['corn','acq','barley']
    groundtruth = []
    texts = []
    setbound = 20
    cat = 0
    for dt in doctype:
        ds =reuters.fileids(dt)
        for fid in ds[0:setbound]:
            groundtruth.append(cat)
            file_cat = reuters.categories(fid)
            rawstr= reuters.raw(fid)
            wordset = sxpExtractText.ExtractEnglishWordA(rawstr)
            texts.append(wordset)
        cat =   cat + 1
    agrdtruth = np.array(groundtruth)

    dictionary = gensim.corpora.Dictionary(texts)
   # print dictionary
    #print(dictionary.token2id)

    corpus = [dictionary.doc2bow(text) for text in texts]
    #print(corpus)
    ntopic = 10
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=ntopic) # initialize an LSI transformation

    shstr = lsi.print_topics(num_topics = 50, num_words=10)
    for t in shstr:
        print(t)
    print(lsi.projection.u.shape)
    V = gensim.matutils.corpus2dense(lsi[corpus_tfidf], len(lsi.projection.s)).T / lsi.projection.s
    print(lsi.projection.s.shape)
    print(V.shape)

    print('begin to cluster')
    data = V
    t0 = time()
    ncluster = 3
    estimator = sxpKMeans(data,ncluster,initstr = 'random')
    BenchmarkA(data,'kmean_random',agrdtruth,estimator,t0)
def TestPCA():
    print(reuters.categories())
    doctype = ['corn','acq','barley']
    groundtruth = []
    texts = []
    setbound = 20
    cat = 0
    for dt in doctype:
        ds =reuters.fileids(dt)
        for fid in ds[0:setbound]:
            groundtruth.append(cat)
            file_cat = reuters.categories(fid)
            rawstr= reuters.raw(fid)
            wordset = sxpExtractText.ExtractEnglishWordA(rawstr)

            texts.append(" ".join(wordset))
        cat =   cat + 1
    agrdtruth = np.array(groundtruth)
    pcanum = 10
    rt_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(texts)
    data = rt_tfidf.ct.toarray()
    print('sxpPCAKmeans starts')
##    print (data0==np.Inf).sum()
##    print (data0==np.NaN).sum()
##    print (data0==np.NAN).sum()
##    print (data0==0).sum()
##    print data0.shape
##    print (data0>0).sum()
    t0 = time()
    ncluster = 3
    estimator2 = sxpPCAKmeans(data,pcanum, ncluster)
    print('benchmark starts')
    BenchmarkA(data,'kmean_pca',agrdtruth,estimator2,t0)
def TestLDA():
    print(reuters.categories())
    doctype = ['corn','acq']
    groundtruth = []
    texts = []
    setbound = 50
    cat = 0
    for dt in doctype:
        ds =reuters.fileids(dt)
        for fid in ds[0:setbound]:
            groundtruth.append(cat)
            file_cat = reuters.categories(fid)
            rawstr= reuters.raw(fid)
            wordset = sxpExtractText.ExtractEnglishWordA(rawstr)
            texts.append(wordset)
        cat =   cat + 1
    agrdtruth = np.array(groundtruth)

    dictionary = gensim.corpora.Dictionary(texts)
   # print dictionary
    #print(dictionary.token2id)

    corpus = [dictionary.doc2bow(text) for text in texts]
    #print(corpus)
    ntopic = 50
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=ntopic,  update_every=0, passes=20)
    shstr = lda.print_topics(num_topics = ntopic, num_words=10)
    for t in shstr:
        print(t)
    print(lda.alpha)
    print(lda.alpha.shape)
    print(lda.state.get_lambda().shape)
    t,kn= lda.state.get_Elogbeta().shape
    k_t = lda.state.get_lambda().T

    d_k = gensim.matutils.corpus2dense(corpus, num_terms =kn),
    print(d_k[0].shape)
    d_k = d_k[0].T
    d_t = np.dot(d_k,k_t)
    t0 = time()
    ncluster = 2
    estimator2 = sxpKMeans(d_t,ncluster,initstr = 'k-means++')
    print('benchmark starts')
    BenchmarkA(d_t,'kmean_pca',agrdtruth,estimator2,t0)

def main():
    #TestFreqCount()
    #TestReuterSet()
    #TestNMF()
   # TestPLSA()
    #TestLSI()
    #TestPCA()
    TestLDA()
if __name__ == '__main__':
    main()
