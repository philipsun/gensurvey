# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:
# Purpose:
# Create Time: 2021/2/23 10:28
# Author: Xiaoping Sun
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------

#coding=UTF-8

import numpy as np


#import sxpPackage
import sxpReadFileMan

import sxpParseDUCText
import sxpSentDistanceGraph
from sxpSentDistanceGraph import sxpText

import sxpWordCloseQueryRank
import sxpRemoveDup
from bs4 import BeautifulSoup
import re
import sxpTfidfBM25
#duc2007sgml = r'E:\pythonworknew\code\textsum\data\DUC2007_Summarization_Documents\DUC2007_Summarization_Documents\duc2007_testdocs\duc2007_topics.sgml'
duc2006sgml = r'E:\pythonworknew\code\textsum\data\DUC2006_Summarization_Documents\DUC2006_Summarization_Documents\duc2006_topics.sgml'
#duc2007srcdir = r'E:\pythonworknew\code\textsum\data\DUC2007_Summarization_Documents\DUC2007_Summarization_Documents\duc2007_testdocs\main'
duc2006srcdir = r'E:\pythonworknew\code\textsum\data\DUC2006_Summarization_Documents\DUC2006_Summarization_Documents\duc2006_docs'
#duc2007modelsrcdir = r'E:\pythonworknew\code\textsum\data\DUC2007_Summarization_Documents\DUC2007_Summarization_Documents\summs\models'
duc2006modelsrcdir = r'E:\pythonworknew\code\textsum\data\DUC2006_Summarization_Documents\DUC2006_Summarization_Documents\NISTeval\ROUGE\models'
#duc2007peersrcdir = r'E:\pythonworknew\code\textsum\data\DUC2006_Summarization_Documents\DUC2006_Summarization_Documents\NISTeval\ROUGE\peers'
duc2006peersrcdir = r'E:\pythonworknew\code\textsum\data\DUC2006_Summarization_Documents\DUC2006_Summarization_Documents\NISTeval2\ROUGE\peers'

paperpath = './test/duc2006mult/papers'
fdir = './test/duc2006mult'
pkdir = r'./test/duc2006mult/papers_pk'
graph_dir =   './test/duc2006mult/papers_graph'
data_dir =r'./test/duc2006mult/data'
sxpReadFileMan.CheckMkDir(fdir)
sxpReadFileMan.CheckMkDir(paperpath)
sxpReadFileMan.CheckMkDir(pkdir)
sxpReadFileMan.CheckMkDir(graph_dir)
sxpReadFileMan.CheckMkDir(data_dir)
def main(cmdlist = [],summethod=[]):
   # cmdlist =['sgml', 'makemodel','PrepareTargetTopicSourceFile'
   #     ,'loadalltopicsrc','MakeSumByModel']
    # cmdlist=['PrepareTargetTopicSourceFile','loadalltopicsrc']
    cmdlist = ['loadalltopicsrc']
    #cmdlist = ['makemodel','makediffgraph','MakeSumByModel']
    #cmdlist = ['PrepareTargetTopicSourceFile','MakeSumByModel']
    #cmdlist = ['MakeSumByModel']
    if len(cmdlist)==0:
        cmdlist = ['MakeSumByModel']

    if 'sgml' in cmdlist:
        processmainsgml()
    if 'makemodel' in cmdlist:
        makemodelfortest('testduc2006')
    if 'PrepareTargetTopicSourceFile' in cmdlist:
        PrepareTargetTopicSourceFile()
    if 'loadalltopicsrc'in cmdlist:
        counttopic()
      #  loadalltopicsrc()
    if 'makediffgraph' in cmdlist:
        MakeSumByDiff(summethod='diffgraph')
    if 'MakeSumByModel'in cmdlist:
        if len(summethod)==0:
            summethod = [
             # 'bymodel0',
             # 'head1',
             # 'head2',
             # 'onefromsrc',
             # 'diffsimgraph',
             # 'diffgraph',
             # 'simgraph',
             # 'simdiffskip',
             # 'wordclosetopic',
             # 'wordclosetopicone',
             # 'wordclosesim'
            #'duc2006s15',
             'wordclosetopic',
            ]
        if 'bymodel0' in summethod:
            MakeSumByModel(summethod='bymodel0')
        if 'head1' in summethod:
            MakeSumByHeadWord(summethod='head1')
        if 'head2' in summethod:
            MakeSumByHeadWord(summethod='head2')
        if 'onefromsrc' in summethod:
            MakeSumByOneSrc(summethod='onefromsrc')
        if 'diffgraph' in summethod:
            MakeDiffRank(summethod='diffgraph')
        if 'diffsimgraph' in summethod:
            MakeDiffRank(summethod='diffsimgraph')
        if 'simgraph' in summethod:
            MakeDiffRank(summethod='simgraph')
        if 'simdiffskip' in summethod:
            MakeDiffRank(summethod='simdiffskip')
        if 'wordclosetopic' in summethod:
            MakeSumByClose(summethod='wordclosetopic'
                           ,rankerversion = 'dual_v6')
        if 'wordclosetopicone' in summethod:
            MakeSumByCloseOne(summethod = 'wordclosetopicone'
                              , rankerversion = 'dual_v6')
        if 'wordclosetopiconev1' in summethod:
            MakeSumByCloseOne(summethod = 'wordclosetopiconev1'
                              ,rankerversion = 'dual_v6_exclusion_meanclose_v1')
        if 'worddirectedclose' in summethod:
            MakeSumByClose(summethod = 'worddirectedclose'
                              ,rankerversion = 'dual_v6_directed')
        if 'even' in summethod:
            MakeSumByCloseOne(summethod='even'
                          , rankerversion='dual_v6_even_v1')
        if 'wordclosesim' in summethod:
            MakeSumBySimClose(summethod ='wordclosesim')
        if 'tfidf' in summethod:
            MakeSumByTFIDFBM25('tfidf')
        if 'dtfipf' in summethod:
            MakeSumByTFIDFBM25('dtfipf')
        if 'BM25Okapi' in summethod:
            MakeSumByTFIDFBM25('BM25Okapi')

        if 'tfidfone' in summethod:
            MakeSumByTFIDFOne('tfidfone')
        if 'BM25Okapione' in summethod:
            MakeSumByTFIDFOne('BM25Okapione')
        if 'dtfipfone' in summethod:
            MakeSumByTFIDFOne('dtfipfone')

        for each in summethod:
            if re.match(r'duc2006s(\d+)',each):
                MakeDUCPeers(each)
def counttopic():
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    alen = []
    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        a = countone(topicid)
        alen.append(a)
    print('mean',np.mean(alen))
def countone(topicid):
    pkfname = pkdir +'/'+ topicid + '.topicsrc.pk'
    rawlists = sxpReadFileMan.LoadObject(pkfname)
    print('----', topicid)
    l=0.0
    for rawdict in rawlists:
      #  print(rawdict['sxptxt'].sentence_list)
        l = l + len(rawdict['sxptxt'].sentence_list)

    a = l/len(rawlists)
    print('avg sent len',a,topicid)
    return a
def processmainsgml():
    soup = BeautifulSoup(open(duc2006sgml),features="lxml")
    topics = soup.find_all('topic')
    topic_dict = {}
    for i,topic in enumerate(topics):
        print(i)
  #      print(topic.num.get_text())
        doctopic = {}
        doctopic['id']=topic.num.get_text().strip()
  #      print(topic.title.get_text())
        doctopic['title']=topic.title.get_text().strip()
  #      print(topic.narr.get_text())
        doctopic['narr']=topic.narr.get_text().strip()
        print(doctopic)
        subdir = duc2006srcdir + '\\' + doctopic['id']
        docs = sxpReadFileMan.GetDirFileList(subdir)

        docidlist=[]
        for each in docs:
            d= each.strip()
            if d:
                docidlist.append(d)
                print(d)
        doctopic['docidlist']=docidlist

        topic_dict[doctopic['id']]=doctopic
    fname = data_dir +'\\' + 'duc2006topictitle.dict'
    sxpReadFileMan.SaveObject(topic_dict,fname)
def makemodelfortest(testname):
    testmodeldir = fdir +'\\'+testname
    sxpReadFileMan.CheckMkDir(testmodeldir)
    fname = data_dir + '\\' + 'duc2006topictitle.dict'
    topic_dict = sxpReadFileMan.LoadObject(fname)
    doc_model_dict = {}
    doc_model_sent_list = []
    for topicid, docdict in topic_dict.items():
        subdirid = re.match('D(\d+)[A-Z]',topicid)
        print('topicid,subdirid',topicid,subdirid.groups()[0])
        filepat = "D"+subdirid.groups()[0] + "\.M\.250" + "\.[A-Z]\.[A-Z]"
        srcmodelsubdir = duc2006modelsrcdir
        filenamelist = sxpReadFileMan.GetDirFileList(duc2006modelsrcdir,filepat)
        model_info_sent_list = []

        model_len = []
        for eachfile in filenamelist:
            fullname = srcmodelsubdir + "\\"+eachfile
            txt = sxpReadFileMan.Read(fullname,encode='iso8859-1')
            #print(txt.encode('utf-8'))
            utxt = txt.encode('utf-8').decode('utf-8')
            sentlist = re.split("\.\s",utxt)
            print("-------:",eachfile)
            modelsent = []
            for eachsent in sentlist:
                if len(eachsent.strip())==0:
                    continue
                modelsent.append(eachsent)

            model_info = {}
            model_info['fid'] = eachfile
            model_info['subdir'] = srcmodelsubdir
            model_info['len'] = 250
            model_info['topicid']=topicid
            model_info['file_name'] = eachfile #this is for the model file name that is used in making model
            model_info['sent_list'] = modelsent
            model_len.append(model_info['len'])
            model_info_sent_list.append((model_info,model_info['sent_list']))
        doc_dict = {}
        doc_dict['model']=model_info_sent_list
        doc_dict['title']=docdict['title']
        doc_dict['narr'] = docdict['narr']
        doc_dict['fid']=topicid
        doc_dict['model_len']=model_len
        doc_dict['model_idx']=topicid#'{0:0>4}'.format(i)
        print('topic title,',doc_dict['title'])
        print('topic narr', doc_dict['narr'])
        doc_model_sent_list.append(doc_dict)

    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    sxpReadFileMan.SaveObject(doc_model_sent_list,doc_model_sent_list_name)
    return doc_model_sent_list
def LoadDocModelSentence():
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list = sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    return doc_model_sent_list
def PrepareTargetTopicSourceFile():
    filelist, subdirlist = sxpReadFileMan.GetDir(duc2006srcdir)
   #Q model_raw_src_dict = {}
    for eachsub in subdirlist:
       # print(eachsub)
        g=re.match('[A-Z](\d+[A-Z])',eachsub)
        if g:
            topicid = 'D'+g.groups()[0]
            print('topicid,',topicid)
        else:
            continue
        fullsub = duc2006srcdir + '\\'+eachsub
        filelist, subdirlist = sxpReadFileMan.GetDir(fullsub)
        rawlists = []
        for eachf in filelist:
            fname = fullsub + r'/' + eachf
            print(fname)
            ##            sxpReadFileMan.ReadTextUTF(fname)
            sxptxt = sxpParseDUCText.ParseDUC2006(fname)
            rawdict = {}
            rawdict['file_name'] = eachf
            rawdict['sxptxt'] = sxptxt
            rawlists.append(rawdict)
       # model_raw_src_dict[topicid] = rawlists
        #pkfname = pkdir +'/'+ 'allltopicsrc' + '.pk'
        pkfname = pkdir + '/' + topicid + '.topicsrc.pk'
        sxpReadFileMan.SaveObject(rawlists, pkfname)
def loadalltopicsrc():
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        rawlist = loadalltopicsrcone(topicid)
def loadalltopicsrcone(topicid):
    pkfname = pkdir +'/'+ topicid + '.topicsrc.pk'
    rawlists = sxpReadFileMan.LoadObject(pkfname)
    print('----', topicid)
    for rawdict in rawlists:
        print(rawdict['sxptxt'].sentence_list)

    return rawlists
def MakeSumByModel(summethod='bymodel0'):
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}
    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        sent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        for sent in model_sent:
            sent_list.append(sent)
        model_sent_dict[topicid]=sent_list
        #rawlist = loadalltopicsrcone(topicid)
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def LoadSys(summethod,topicid):
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    model_sent_dict = sxpReadFileMan.LoadObject(fname)
    return model_sent_dict[topicid]
def MakeSumByHeadWord(summethod='head2'):
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}
    g = re.match('head(\d+)',summethod)
    headtopk = int(g.groups()[0])
    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)


        rawlist = loadalltopicsrcone(topicid)
        sentlist = []
        twdlen = 0
        wdlen = 250
        for eachdoc in rawlist:
            thisdocsentlist = eachdoc['sxptxt'].sentence_list[0:headtopk]
            for s in thisdocsentlist:
                if twdlen>wdlen:
                    break
                sentlist.append(s)
                g = re.split('\s+',s)
                nl = len(g)
                twdlen = twdlen + nl

        model_sent_dict[topicid] = sentlist
        print('gen sum',sentlist)
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def MakeSumByOneSrc(summethod='onefromsrc'):
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)


        rawlist = loadalltopicsrcone(topicid)
        sentlist = []
        twdlen = 0

        rndpaper=np.random.randint(len(rawlist))
        thisdocsentlist = rawlist[rndpaper]['sxptxt'].sentence_list
        wdlen = 250
        for s in thisdocsentlist:
            if twdlen > wdlen:
                break
            sentlist.append(s)
            g = re.split('\s+', s)
            nl = len(g)
            twdlen = twdlen + nl

        model_sent_dict[topicid] = sentlist
        print('gen sum',sentlist)
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)

def MakeSumByDiff(summethod='diffgraph'):
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)


        rawlist = loadalltopicsrcone(topicid)
        sentlist = []
        twdlen = 0
        for eachdoc in rawlist:
            thisdocsentlist = eachdoc['sxptxt'].sentence_list
            for s in thisdocsentlist:
                sentlist.append(s)
                twdlen = twdlen + len(s)
        print('doc num has total sent num',len(rawlist),len(sentlist))
        sxptext  = sxpSentDistanceGraph.MyDiffGraph(sentlist)
        twdlen = 250
        ranksent = sxptext.OutputAllRankSentence(twdlen)

        fname = pkdir + '\\' + 'sumby_sxptext_' + summethod + '_'+ topicid +'.dict'
        sxpReadFileMan.SaveObject(sxptext, fname)

        model_sent_dict[topicid] = ranksent
        print('gen sum',sentlist)
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def MakeDiffRank(summethod='diffsimgraph'):
    print('build rank for',summethod)
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)

        fname = pkdir + '\\' + 'sumby_sxptext_' + 'diffgraph' + '_'+ topicid +'.dict'
        sxptext = sxpReadFileMan.LoadObject( fname)
        wdlen = 250
        ranksent = sxptext.rankbydiff(use_diff=summethod,wlen=wdlen,simr = 0.4)

        twdlen = 0
       # sentlist = []
        # for s in ranksent:
        #     if twdlen > wdlen:
        #         break
        #     ranksent.append(s)
        model_sent_dict[topicid] = ranksent
        print('gen sum',ranksent)
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def MakeSumByClose(summethod='wordclosetopic', rankerversion = 'dual_v6'):
    print('build rank for',summethod)
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)



        rawlist = loadalltopicsrcone(topicid)
        sentlist = []
        twdlen = 0
        for eachdoc in rawlist:
            thisdocsentlist = eachdoc['sxptxt'].sentence_list
            for s in thisdocsentlist:
                sentlist.append(s.lower())
                twdlen = twdlen + len(s)
        print('doc num has total sent num',len(rawlist),len(sentlist))
        wdlen = 250
        prefix = []
        #  keywordseq = [doc_dict['title']]
       # keywordseq = [doc_dict['title'] + ' ' + doc_dict['narr']]
        keywordseq = [doc_dict['narr']]
        sent_rank_dict = sxpWordCloseQueryRank.queryrank(keywordseq,prefix, sentlist
                                                         ,wdlen = 250
                                                         ,simr = 0.5, removestop=True,selectbydiff='NO'
                                                         ,version = rankerversion )
        #, version = 'dual_v6', 'v4'，‘dual_v6_noeven’
        wdlen = 0
        # sentlist = []
        # for s in ranksent:
        #     if twdlen > wdlen:
        #         break
        #     ranksent.append(s)
        simr = 0.2
        # using group sim will descreas the su4 score
        print('select diff')
        sentlist = sxpRemoveDup.SelectDiffSent(sent_rank_dict['ranked_sent'], simr, 250)
        print('doc num has total sent num', len(rawlist), len(sentlist))

        model_sent_dict[topicid] = sentlist
        print('gen sum',summethod, sentlist)
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def MakeSumByTFIDFBM25(summethod):
    print('build rank for',summethod)
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)



        rawlist = loadalltopicsrcone(topicid)
        sentlist = []
        twdlen = 0
        for eachdoc in rawlist:
            thisdocsentlist = eachdoc['sxptxt'].sentence_list
            for s in thisdocsentlist:
                sentlist.append(s.lower())
                twdlen = twdlen + len(s)
        print('doc num has total sent num',len(rawlist),len(sentlist))
        wdlen = 250
        prefix = []
        #      keywordseq = [doc_dict['title']]
        keywordseq = [doc_dict['title'] + ' ' + doc_dict['narr']]

        # sent_rank_dict = sxpWordCloseQueryRank.queryrank(keywordseq,prefix, sentlist
        #                                                  ,wdlen = 250
        #                                                  ,simr = 0.5, removestop=True,selectbydiff='NO')
        testname = 'DUC2006'
        sent_rank_dict = sxpTfidfBM25.RankSentence(keywordseq, sentlist, testname, bmmodel=summethod, selectbydiff='NO')
        wdlen = 0
        # sentlist = []
        # for s in ranksent:
        #     if twdlen > wdlen:
        #         break
        #     ranksent.append(s)
        simr = 0.2
        # using group sim will descreas the su4 score
        sentlist = sxpRemoveDup.SelectDiffSent(sent_rank_dict['ranked_sent'], simr, 250)
        print('doc num has total sent num', len(rawlist), len(sentlist))

        model_sent_dict[topicid] = sentlist
        print('gen sum',summethod, sentlist)
        # model_sent_dict[topicid] = sent_rank_dict['topsent']
        # print('gen sum',sent_rank_dict['topsent'])
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    print('save summethod',fname)
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def MakeSumByCloseOne(summethod = 'wordclosetopicone',rankerversion = 'dual_v6'):
    print('build rank for',summethod)
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)

        rawlist = loadalltopicsrcone(topicid)
        sentlist = []
        twdlen = 0

        prefix = []
        #  keywordseq = [doc_dict['title']]
        keywordseq = [doc_dict['title']+' ' + doc_dict['narr']]

        docsent_list=[]
        for eachdoc in rawlist:
            thisdocsentlist = eachdoc['sxptxt'].sentence_list
            eachdocsent = []
            sent_rank_dict = sxpWordCloseQueryRank.queryrank(keywordseq, prefix, thisdocsentlist
                                                             , wdlen=250
                                                             ,simr = 0.4, removestop=True
                                                             ,groupsim = True,selectbydiff='NO'
                                                             ,version = rankerversion)
            for s in sent_rank_dict['topsent']:
                eachdocsent.append(s.lower())
                twdlen = twdlen + len(s)
            docsent_list.append(eachdocsent)

        simr= 0.4
        #using group sim will descreas the su4 score
        sentlist = sxpRemoveDup.SelectDiff(docsent_list,simr,250)
        print('doc num has total sent num',len(rawlist),len(sentlist))

        model_sent_dict[topicid] = sentlist
        print('gen sum',sent_rank_dict['topsent'])
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def MakeSumByTFIDFOne(summethod = 'tfidfone'):
    print('build rank for',summethod)
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}
    testname = 'DUC2006'
    pt = '(\w+)one'
    g = re.match(pt,summethod)
    method = g.groups()[0]
    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)

        rawlist = loadalltopicsrcone(topicid)
        sentlist = []
        twdlen = 0

        prefix = []
        #  keywordseq = [doc_dict['title']]
        keywordseq = [doc_dict['title']+' ' + doc_dict['narr']]

        docsent_list=[]
        for eachdoc in rawlist:
            thisdocsentlist = eachdoc['sxptxt'].sentence_list
            eachdocsent = []
            # sent_rank_dict = sxpWordCloseQueryRank.queryrank(keywordseq, prefix, thisdocsentlist
            #                                                  , wdlen=250
            #                                                  ,simr = 0.4, removestop=True
            #                                                  ,groupsim = True,selectbydiff='NO')
            sent_rank_dict = sxpTfidfBM25.RankSentence(keywordseq, thisdocsentlist, testname, bmmodel=method,
                                                       selectbydiff='NO')

            for s in sent_rank_dict['topsent']:
                eachdocsent.append(s.lower())
                twdlen = twdlen + len(s)
            docsent_list.append(eachdocsent)

        simr= 0.4
        #using group sim will descreas the su4 score
        sentlist = sxpRemoveDup.SelectDiff(docsent_list,simr,250)
        print('doc num has total sent num',len(rawlist),len(sentlist))

        model_sent_dict[topicid] = sentlist
        print('gen sum',sent_rank_dict['topsent'])
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def MakeSumBySimClose(summethod ='wordclosesim'):
    print('build rank for',summethod)
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)

        rawlist = loadalltopicsrcone(topicid)
        sentlist = []
        twdlen = 0

        prefix = []
        #  keywordseq = [doc_dict['title']]
        keywordseq = [doc_dict['title']+' ' + doc_dict['narr']]
        docsent_list = []
        alldocsent_list=[]
        score = []
        allrawscore = []
        for eachdoc in rawlist:
            print('topic file:',topicid,eachdoc['file_name'])
            thisdocsentlist = eachdoc['sxptxt'].sentence_list
            eachdocsent = []
            sent_rank_dict = sxpWordCloseQueryRank.queryrank(keywordseq, prefix, thisdocsentlist
                                                             , wdlen=250
                                                             ,simr = 0.45, removestop=True
                                                             ,groupsim = False)
            topscore = sent_rank_dict['topscore']
            rawtopscore =sent_rank_dict['rawtopscore']
            for i,s in enumerate(sent_rank_dict['topsent']):
                eachdocsent.append(s.lower())
                twdlen = twdlen + len(s)
                alldocsent_list.append(s)
                score.append(topscore[i])
                allrawscore.append(rawtopscore[i])
            docsent_list.append(eachdocsent)
        simr= 0.35
        #using group sim will descreas the su4 score
        # sentlist = sxpRemoveDup.rankimpdiff(score,docsent_list,250)
        # print('doc num has total sent num',len(rawlist),len(sentlist))
        sentlist = sxpRemoveDup.SelectDiff(docsent_list,simr,250)
        wdlen = 250;
        simr = 0.15
    # sentlist= sxpRemoveDup.SelectDiffByAllRankScore(allrawscore,alldocsent_list,simr,wdlen)
        print('doc num has total sent num',len(rawlist),len(sentlist))

        model_sent_dict[topicid] = sentlist
        print('gen sum',sent_rank_dict['topsent'])
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def MakeDUCPeers(summethod = 'duc2006s15'):
    g = re.match('duc2006s(\d+)',summethod)
    peerid = g.groups()[0]
    peerdir = r'E:\pythonworknew\code\textsum\data\DUC2006_Summarization_Documents\DUC2006_Summarization_Documents\summs\peers'

    print('build rank for',summethod)
    doc_model_sent_list_name =  graph_dir +'/'+'doc_model_sent_list.list'
    doc_model_sent_list=sxpReadFileMan.LoadObject(doc_model_sent_list_name)
    model_sent_dict = {}

    for doc_dict in doc_model_sent_list:
        topicid = doc_dict['fid']
        print('===for topic',topicid)
        print('topic title',doc_dict['title'])
        print('topic narr',doc_dict['narr'])
        model_info_sent_list = doc_dict['model']
        #doc_dict['model'] =
        msent_list=[]
        model_info, model_sent = model_info_sent_list[0] # since each one topic has many model
        wdlen = 0
        for sent in model_sent:
            msent_list.append(sent)
            wdlen = wdlen + len(sent)


        peer_rankedsent = ReadPeerSys(peerdir,topicid,peerid)

        model_sent_dict[topicid] = peer_rankedsent
        print('gen sum',peer_rankedsent)
    fname = pkdir + '\\' + 'sumby_'+summethod + '.dict'
    sxpReadFileMan.SaveObject(model_sent_dict,fname)
def ReadPeerSys(peerdir,topicid,peerid):
    g = re.match('D(\d+)(\w)',topicid)
    dirid = g.groups()[0]
    fid = g.groups()[1]
    fname = peerdir +'\\D{0}'.format(dirid)  +"\\D{0}.M.250.{1}.{2}".format(dirid,fid,peerid)
    sentlines = sxpReadFileMan.ReadTxtLines(fname)
    return sentlines
if __name__ == '__main__':
   main()

