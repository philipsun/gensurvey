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
import sxpWordCloseQueryRank
import sxpTfidfBM25
import sxpRemoveDup
import re
from nltk.corpus import stopwords
def stop_words():
    sw = stopwords.words("english")
    return sw
def processkeywordstr(keywordseqstr,removestop = True):
    stopwords= stop_words()

    nk = []
    keywordseq = re.split('\s+', keywordseqstr)
    for each in keywordseq:
        if len(each.strip()) == 0:
            continue
        if removestop:
            if each in stopwords:
                continue
        nk.append(each)
    return nk
def QueryByClose(keywordseqstr,sentlist,prefix=[],testname='tfidf',wdlen=200,selectdiff = 'NO'):
    keywordseq = processkeywordstr(keywordseqstr)
    sent_rank_dict = sxpWordCloseQueryRank.queryrank(keywordseq, prefix, sentlist
                                                     , wdlen=wdlen
                                                     , simr=0.4, removestop=True
                                                     , selectbydiff = selectdiff
                                                     , groupsim=True
                                                     ,version = 'dual_v6'
                                                     )
    simr = 0.2
    # using group sim will descreas the su4 score
    if selectdiff == 'YES':
        topk = sxpRemoveDup.SelectDiffSent(sent_rank_dict['ranked_sent'], simr, wdlen)
        print('doc num has total sent num', len(topk))
        print('gen sum', testname, topk)
    else:
        topk = sent_rank_dict['topsent']
    return topk
def QueryByTfidf(keywordseqstr,sentlist,prefix,testname='tfidf',wdlen=200,selectdiff = 'NO'):

    method = 'tfidf'
    topk =  tfidfquery(keywordseqstr, sentlist, prefix=prefix, testname=testname, bmmodel=method, selectdiff=selectdiff,wdlen = wdlen)
    return topk

def QueryByDTFIPF(keywordseqstr,sentlist,prefix,testname='dtfipf',wdlen=200,selectdiff = 'NO'):

    method = 'dtfipf'
    topk =  tfidfquery(keywordseqstr, sentlist, prefix=prefix, testname=testname, bmmodel=method, selectdiff=selectdiff,wdlen = wdlen)
    return topk
def QueryByBM25(keywordseqstr,sentlist,prefix=[],testname='BM25Okapi',wdlen=200,selectdiff='NO'):

    method = 'BM25Okapi'
    topk =  tfidfquery(keywordseqstr, sentlist, prefix=prefix, testname=testname, bmmodel=method, selectdiff=selectdiff,wdlen = wdlen)
    return topk
def tfidfquery(keywordseqstr,sentlist,prefix=[],testname='tfidftest',wdlen=300,selectdiff=False,bmmodel='BM250kapi'):
    keywordseq = processkeywordstr(keywordseqstr)
    sent_rank_dict = sxpTfidfBM25.RankSentence(keywordseq, sentlist, testname, bmmodel=bmmodel, selectbydiff='NO',wdlen = wdlen)
    wdlen = 0
    # sentlist = []
    # for s in ranksent:
    #     if twdlen > wdlen:
    #         break
    #     ranksent.append(s)
    simr = 0.2
    # using group sim will descreas the su4 score
    if selectdiff == 'YES':
        topk = sxpRemoveDup.SelectDiffSent(sent_rank_dict['ranked_sent'], simr, wdlen)
        print('doc num has total sent num', len(topk))
        print('gen sum', testname, topk)
    else:
        topk = sent_rank_dict['topsent']
    return topk
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