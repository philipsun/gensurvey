#-------------------------------------------------------------------------------
# Name:        sxpSurveyData.py
# Purpose:
#
# Author:      sunxp
#
# Created:     23/10/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=UTF-8
import re
import os
import json
import collections
import numpy as np
from scipy.sparse import csr_matrix
from scipy import *


import sxpReadFileMan
import sxpTextEncode
import sxpExtractText
import sxpFenciMakeTFIDF
import sxpReferMan
from graphengine.sxpGraphEngine import sxpNetwork
import sxpTestWordDistQuerySurvey
import sxpMultiPaperData
#from graphengine.sxpGraphEngine import *
import sxpSurveyData
from sxpSurveyData import sxpNode,sxpNetwork
import sxpPlotBar
import pandas as pd

f = open('stopwords.txt', 'r')
lines = f.readlines()
f.close()
remove_stopwords = 1
if remove_stopwords == 1:
    stopwords = [line.strip() for line in lines]
elif remove_stopwords == 0:
    stopwords = []


def main(maincmd=""):
    testdict = [
        {
            "survgenmethod": 'abstract_top2',
            "testname": 'wordquery_allv6'
        },
        {
            "survgenmethod": 'abstract_top2',
            "testname": 'wordquery_allv6'
        },
        {
            "survgenmethod": 'abstract',
            "testname": 'tfidf_all'
        },
        {
            "survgenmethod": 'abstract',
            "testname": 'wordquery_allv6'
        },
        {
            "survgenmethod": 'abstract',
            "testname": 'wordquery_allv6ks'
        }
    ]

    ##   survgenmethod = 'abstract'
    ##   testname = 'wordquery_allv6ks'
    testdict = [
        {

            "survgenmethod": 'opt',
            "testname": 'wordquery_allv6ks_dual_sentrank'
        }
        ]

    testdict=[
        {

            "survgenmethod": 'abstract',
            "testname": 'wordquery_allv6ks_dual_sentrank'
        }
    ]
    testdict = [
        {

            "survgenmethod": 'abstract',
            "testname": 'tfidf_all'
        }
    ]
    testdict = [
        {

            "survgenmethod": 'orig',
            "testname": 'dtfipf_all_stop'
        }
    ]


    testdict = [
        {

            "survgenmethod": 'LR',
            "testname": 'wordquery_allv6ks_dual_sentrank'
        }
    ]
    testdict=[
        {

            "survgenmethod": 'LR',
            "testname": 'wordquery_allv6ks_dual_sentrank'
        },
        {

            "survgenmethod": 'orig',
            "testname": 'wordquery_allv6ks_dual_sentrank'
        },
        {

            "survgenmethod": 'orig',
            "testname": 'dtfipf_all_stop'
        },
        {

            "survgenmethod": 'LR',
            "testname": 'dtfipf_all_stop'
        }
    ]
    if maincmd:
        cmd = maincmd
    else:
        #cmd = 'TraverseShowSurvey'
        ci = [1,2,3]
        cmdlist=[]
        if 1 in ci:
            cmd = 'BuildChapterSurvPaperSent'  # first step,
            cmdlist.append(cmd)
        if 2 in ci:
            cmd = 'CompareSentDiff'  # first step,
            cmdlist.append(cmd)

    if 'BuildChapterSurvPaperSent' in cmdlist:
        for eachtest in testdict:
          #  BuildSurveyChapterByRankResult(eachtest['survgenmethod'],eachtest['testname'])
            BuildChapterSurvPaperSent(eachtest['survgenmethod'],eachtest['testname'])
    if 'CompareSentDiff' in cmdlist:
        resultdict={}
        for eachtest in testdict:
          #  BuildSurveyChapterByRankResult(eachtest['survgenmethod'],eachtest['testname'])
            keyname,intra_paper_sim,inter_paper_sim = CompareSentDiff(eachtest['survgenmethod'],eachtest['testname'])
            resultdict[keyname]=[intra_paper_sim,inter_paper_sim]
        fname = sxpTestWordDistQuerySurvey.output_dir + '/' + 'CompareSentDiff.result.csv'
        df = pd.DataFrame(resultdict).T
        df.to_csv(fname)

def BuildChapterSurvPaperSent(survgenmethod,testname):
    fname = sxpTestWordDistQuerySurvey.output_dir + '/' + testname + '_wd_top_len.result.dict'
    allresult = sxpReadFileMan.LoadObject(fname)

    fname = sxpTestWordDistQuerySurvey.output_dir + '/' + 'allchapter_survey_sent.dict'
    all_chapter_dict = sxpReadFileMan.LoadObject(fname)
    # chapter_dict = {}
    # chapter_dict['fid'] = '{:0=4}'.format(i)
    # chapter_fid_dict[chapter_dict['fid']] = chapter_sent_dict[chapter]
    # chapter_dict['title'] = chapter;
    # chapter_dict['sent'] = chapter_sent_dict[chapter]

    chapter_refid_dict = sxpReferMan.GetRefFid()

    doc_sent_num_dict = sxpMultiPaperData.LoadAllPaperSentNum()
    stlen_dict = doc_sent_num_dict['sent_dict']
    all_paper_sent_len = 0
    all_paper_word_len = 0
    # testname = 'wordquery_allv6'
    # testname = 'tfidf_all'
    # testname = 'wordquery_allv2'
    suverypaper = sxpSurveyData.GetSuveryChapterSent()
    chapter_list = suverypaper['chapter_list']
    chapter_title = suverypaper['chapter_title']

    print('--------')
    #   sxpTestWordDistQuerySurvey.ShowAllChapter(testname)
    print(('--------', survgenmethod, testname))
    chapter_gensurv_dict = {}
    for chpater, testinfo in allresult.items():
        print('processing chapter:-------->', chpater)
        if chpater == '1':
            br = 1
        print('num of words in this chapter', all_chapter_dict[chpater]['wordlen'])
        print("num of sents in this chapter", all_chapter_dict[chpater]['sentlen'])

        topk = sxpTestWordDistQuerySurvey.LoadDualRankTopk(testname, survgenmethod, chpater)

        print("topk['chapter_gensum_topk']=topkdoc is a list contains the select paper's inform: num",
              len(topk['chapter_gensum_topk']))
        # print('''
        #     for i in range(topk):
        # d = {}
        # d['fid']=docfid_list[i]
        # d['title']=rankresult[i][3]
        # d['raw_doc_len'] = paper_len_dict[docfid_list[i]]
        # d['sum_sent_len']=selsentnum*p[i,0]
        # d['rank']=i
        # d['score']=s[i,0]
        # d['percent']=p[i,0]
        # topkdoc.append(d)
        # ''')
        sent_rank_result = testinfo['sent_rank_result']
        # sent_rank_dict['score']=dual_sent_score
        # sent_rank_dict['ranked_sent'] = ranked_sent
        # sent_rank_dict['idx_sent'] = idx_sent
        # sent_rank_result[fname_dict['fid']]=sent_rank_dict
        chapter_survey_sent_list = []

        refpaperwordlen = 0
        for eachpaper in topk['chapter_gensum_topk']:
            [sl, wl] = stlen_dict[eachpaper['fid']]
            refpaperwordlen = refpaperwordlen + wl

        chapter_gensum_word_len = 0
        chapter_paper_sent_list_dict = {}
        for eachpaper in topk['chapter_gensum_topk']:  # here store every paper in topk
            onepaper_sent = []
            fid = eachpaper['fid']

            sent_dict = sent_rank_result[eachpaper['fid']]
            if eachpaper['fid'] in chapter_refid_dict.keys():
                refdict = chapter_refid_dict[eachpaper['fid']]
                refname = refdict['refname']
            else:
                refname = eachpaper['fid']

            percent = eachpaper['percent']
            print('percent', percent, eachpaper['score'])

            sum_word_len = eachpaper['sum_word_len']
            sum_sent_len = eachpaper['sum_sent_len']
            t = 0
            refsent = 'In ({0}): '.format(refname)
            chapter_survey_sent_list.append(refsent)
            w = 0;
            for s in sent_dict['ranked_sent']:
                # if t>sum_sent_len:
                #    break
                chapter_survey_sent_list.append(s)
                onepaper_sent.append(s)
                t = t + 1
                chapter_gensum_word_len = chapter_gensum_word_len + len(s)
                w = w + len(s)
                if w > sum_word_len and t > 2:
                    break

            eachpaper['sum_sent_len'] = t
            chapter_paper_sent_list_dict[fid]=[refname,fid,onepaper_sent]
           # chapter_paper_sent_list.append(onepaper_sent)

        chapter_gensurv_dict[chpater]=chapter_paper_sent_list_dict
        print('true chapter ref num', topk['true_citedoc_num'])
        print('gensum chapter ref num', topk['chapter_gensum_topknum'])
        print('true chapter sent num', topk['survey_chapter_sent_len'])
        print('gensum chapter sent num', topk['chapter_gensum_sentnum'])
        print('true chapter word num', topk['survey_chapter_wd_len'])
        print('gensum chapter word num', topk['chapter_gensum_word_len'])


        print('gen survy word num', chapter_gensum_word_len)

        # chapter_topk_dict['chapter_gensum_topknum'] = topk
        # chapter_topk_dict['chapter_gensum_sentnum'] = selsentnum

    fname = sxpTestWordDistQuerySurvey.output_dir + '/' + testname + '_' + survgenmethod+ '_'+'chapter_paper_sent.dict'
    sxpReadFileMan.SaveObject(chapter_gensurv_dict,fname)
def CompareSentDiff(survgenmethod,testname):
    fname = sxpTestWordDistQuerySurvey.output_dir + '/' + testname + '_' + survgenmethod+ '_'+'chapter_paper_sent.dict'
    chapter_gensurv_dict = sxpReadFileMan.LoadObject(fname)
    ch_avg_intra_sim =[]
    ch_avg_inter_sim =[]
    for chapter, chapter_paper_sent_list_dict in chapter_gensurv_dict.items():
     #   print('processing chatper--------',chapter)
        sim_intra= []
        sim_inter=[]
        if len(chapter_paper_sent_list_dict)<=1:
            continue
        for fid,paper in chapter_paper_sent_list_dict.items():
        #    print('processing each paper:******')
        #    print(paper)
            sentlist = paper[2]
            for eachsent in sentlist:
                intra_sim = computesent2listsim(eachsent,sentlist)
                inter_sim = computersent2papersentsim(eachsent,fid,chapter_paper_sent_list_dict)
                sim_intra.append(intra_sim)
                sim_inter.append(inter_sim)
        avg_intra = np.mean(sim_intra)
        avg_inter = np.mean(sim_inter)
        ch_avg_inter_sim.append(avg_inter)
        ch_avg_intra_sim.append(avg_intra)
    print("==========",survgenmethod,testname)
    print('average inter sim in chapter',np.mean(ch_avg_inter_sim))
    print('average intra sim in chapter', np.mean(ch_avg_intra_sim))

    fname3 = fname +'.topkdiffsim.jpg'
    t1='intra_paper_sim'
    t2 = 'inter_paper_sim'
    title = testname +'_'+survgenmethod +", intra:{:.2f}; inter:{:.2f}".format(np.mean(ch_avg_intra_sim),np.mean(ch_avg_inter_sim))

    intra_paper_sim = np.array(ch_avg_intra_sim).reshape(-1,1)
    inter_paper_sim = np.array(ch_avg_inter_sim).reshape(-1, 1)
    sxpPlotBar.plotlinelist([intra_paper_sim, inter_paper_sim], [t1,t2], title=title
                            , fname=fname3)
    diffname = fname +'diffsim.csv'
    diffdict = {}
    diffdict['ch_avg_inter_sim']=ch_avg_inter_sim
    diffdict['ch_avg_intra_sim']=ch_avg_intra_sim
    df =pd.DataFrame(diffdict)
    df.to_csv(diffname)
    keyname = survgenmethod + '-'+testname
    return keyname,intra_paper_sim,inter_paper_sim
def computesentsim(sent_i,sent_j):
    sent_a = set([w for w in sent_i.split() if w not in stopwords])
    sent_b = set([w for w in sent_j.split() if w not in stopwords])

    common_word = sent_a.intersection(sent_b)
    if not common_word:
        return 0
    jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
    return jaccard
def computesent2listsim(sent,sentlist):
    d = []
    for each in sentlist:
        jd = computesentsim(sent,each)
        d.append(jd)
    avgd = np.mean(d)
    return avgd;
def computersent2papersentsim(sent,fid,chapter_paper_sent_list_dict):
    #chapter_paper_sent_list_dict[fid] = [refname, fid, onepaper_sent]
    d = []
    for fid,eachpaper in chapter_paper_sent_list_dict.items():
        sentlist = eachpaper[2]
        tfid = eachpaper[1]
        jd = computesent2listsim(sent,sentlist)
        d.append(jd)
    return np.mean(d)
if __name__ == '__main__':
    main()
