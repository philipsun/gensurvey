# -------------------------------------------------------------------------------
# Name:        sxpRemoveDup.py
# Purpose:
#
# Author:      sunxp
#
# Created:     23/10/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# coding=UTF-8

import re
import numpy as np
import sxpJudgeCharacter
import sxpSentCluster


def SelectDiffByAllRankScore(allrawscore, sentlist, simr=0.4, wdlen=250):
    v = np.array(allrawscore).reshape(-1, 1)

    a = list(np.argsort(-v, axis=0).flat)
    w = 0;
    topk = []
    for i in a:
        s = sentlist[i]

        if simsent(s, topk, simr):
            continue
        topk.append(s)
        seg = re.split('\s+', s)
        w = w + len(seg)
        if w >= wdlen:
            break
    return topk

def SelectDiffSent(sent_list, simr =0.4, wdlen = 250):
    w = 0;
    topk = []
    for s in sent_list:

        if simsent(s, topk, simr):
            continue
        seg = re.split('\s+', s)
        for each in seg:
            if len(each.strip())==0:
                continue
            if each.strip() in ['.',',',':','"',"'","?"]:
                continue
            w = w + 1
        if w > wdlen:
            break
        topk.append(s)

    print('sum word len',w)
    return topk


def SelectDiff(docsent_list, simr=0.4, wdlen=250):
    i = 0
    sentdict = {}
    stillrun = True
    while stillrun == True:
        stillrun = False
        for doc in docsent_list:
            if i < len(doc):
                if i not in sentdict.keys():
                    sentdict[i] = []
                sentdict[i].append(doc[i])
                stillrun = True;
        i = i + 1
    rankedsent = []
    for i in range(len(sentdict.keys())):
        doc = sentdict[i]
        top2 = SelectTopSentByWordLim(doc, wdlen=250)
        for each in top2:
            if simsent(each, rankedsent, simr):
                continue
            else:
                rankedsent.append(each)
    return OutputRankSentByWordLen(rankedsent, wdlen=wdlen)


def OutputRankSentByWordLen(sentlist, wdlen=250):
    w = 0;
    topk = []
    for s in sentlist:
        seg = re.split('\s+', s)
        w = w + len(seg)
        if w >= wdlen:
            break
        topk.append(s)


    return topk


def simsentgroup(sent, sent_txt_set, simr=0.4):
    ds = []
    for each in sent_txt_set:
        sim = sxpJudgeCharacter.jaccard_similarity(sent, each)
        ds.append(sim)
    sim = np.mean(ds)
    if sim >= simr:
        return True;
    return False


def simsent(sent, sent_txt_set, simr=0.4):
    for each in sent_txt_set:
        sim = sxpJudgeCharacter.jaccard_similarity(sent, each)
        print(sim)
        if sim > simr:
            return True
    return False


def SelectTopSentByWordLim(sentlist, wdlen=250):
    n = len(sentlist)
    dm = np.zeros((n, n))
    for i, s in enumerate(sentlist):
        for j, t in enumerate(sentlist):
            if i == j:
                continue
            dm[i, j] = sxpJudgeCharacter.jaccard_similarity(s, t)
    v = np.sum(dm, 1)
    r = np.argsort(-v, axis=0).reshape(-1, 1)
    if n == 1:
        return [sentlist[r[0, 0]]]
    if n >= 3:
        return [sentlist[r[0, 0]], sentlist[r[1, 0]], sentlist[r[2, 0]]]
    if n >= 2:
        return [sentlist[r[0, 0]], sentlist[r[1, 0]]]


import sxpSentDistanceGraph
import sxpPageRank


def rankimpdiff(score, sentlist, wdlen=250):
    ss = sxpSentDistanceGraph.BuildSentGraph(sentlist, sim='dis')
    r = sxpPageRank.pagerank(ss) + score
    a = list(np.argsort(-r, axis=0).flat)
    w = 0;
    topk = []
    for i in a:
        s = sentlist[i]
        seg = re.split('\s+', s)
        topk.append(s)
        w = w + len(seg)
        if w >= wdlen:
            break
    return topk


def RankSelTopByDiffImp(doc_list, wdlen='same'):
    diffsentdoc = []
    simsentdoc = []
    for i, (refname,doc) in enumerate(doc_list):
        diffsurv, simsurv = computediff(doc, i, doc_list)
        diffsurv.insert(0,'In  {0}: '.format(refname))
        diffsentdoc.append(diffsurv)
        simsurv.insert(0,'In  {0}: '.format(refname))
        simsentdoc.append(simsurv)
    return diffsentdoc, simsentdoc


def computediff(doc, current_i, doc_list):
    othersentlist = []
    for i, (refname,restdoc) in enumerate(doc_list):
        if i == current_i:
            continue
        for eachsent in restdoc:
            othersentlist.append(eachsent)
    ns = len(doc)
    ncs = len(othersentlist)
    dfm = np.zeros((ns, ncs))
    for i, s in enumerate(doc):
        for j, cs in enumerate(othersentlist):
            dfm[i, j] = sxpJudgeCharacter.jaccard_similarity(s, cs)

    avgdiff = np.mean(dfm, 1)
    idx = list(np.argsort(-avgdiff, 0))
    diffsurv = []
    simsurv = []
    for i in range(ns):
        if i <= ns / 2:
            simsurv.append(doc[idx[i]])
        else:
            diffsurv.append(doc[idx[i]])
    return diffsurv, simsurv


def submodular(gensum, doc_list, alpha=0.64, wdlen='same'):
    allsent = []
    for doc in doc_list:
        for s in doc:
            allsent.append(s)
    ts = 0
    for s in allsent:
        sc0 = CoverageSent(s, gensum)
        sc1 = CoverageSent(s, allsent)
        ts = ts + min(sc0, alpha * sc1)
    rs = sumbmodular_div(gensum, allsent)
    LS = ts + alpha * rs
    return LS


def CoverageSent(sent, gensum):
    score = 0
    for s in gensum:
        score = score + sxpJudgeCharacter.jaccard_similarity(s, sent)
    return score



def sumbmodular_div(gensum, allsent):
    ng = len(gensum)
    na = len(allsent)
    w = np.zeros((ng, na))
    for i, senti in enumerate(gensum):
        for j, sentj in enumerate(allsent):
            w[i, j] = sxpJudgeCharacter.jaccard_similarity(senti, sentj)
    n = int(0.3 * len(allsent))
    cluster_sent_dict, cluster_idxdict = sxpSentCluster.cluster_sent(allsent, n, 'kmenas')
    k = 0
    for ci, sentclusteridx in cluster_idxdict.items():
        s = 0
        for i in range(ng):  # for each si in gensum
            for j in sentclusteridx:  # for each sj in cluster
                if (1 - w[i, j]) <= 0.05:  # means si is same as sj, so it should be include
                    sc = np.sum(w[i, :], 1) / na
                    s = s + sc
        k = k + np.sqrt(s)
    return k
