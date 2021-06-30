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

import os
import sxpKeyDist
import sxpdoc
import sxpSGT
import sxpTextEncode
import sxpJudgeCharacter
import copy
from sxpMultiPaperData import sxpNode

basedir = os.path.abspath(os.path.dirname(__file__))
#this is to replace the host url

def MakeSurvey(paperlist,temptree,surv_conf):
    print(('making survey for the tree',temptree.title))
    keypath = []
    sentlist,refdoc_idxlist = MakeSurveyBySGT(paperlist,temptree.root,keypath,surv_conf)
    return sentlist,refdoc_idxlist
def MakeSurveyBySGT(paperlist,sgt,keypath,surv_conf):

    dim_sent=[]
    sec_sent=[]
    newkeypath = copy.copy(keypath)
    newkeypath.append(sgt.keyword)
    if len(sgt.dim)==0 and len(sgt.topic)==0:

        topdocsent,refdoc_idxlist = MakeLeafDocSurvey(paperlist,newkeypath,surv_conf)
        print(keypath)
        for eachsent in topdocsent:
            sec_sent.append(eachsent)
        return sec_sent,refdoc_idxlist
    ref =[]
    if len(sgt.dim)>0:
        makehead(len(sgt.dim))
        for eachnode in sgt.dim:
            dimdocsent,refdoc_idxlist = MakeSurveyBySGT(paperlist,eachnode,newkeypath,surv_conf)
            for docidx in refdoc_idxlist:
                ref.append(docidx)
            dim_sent.append([eachnode.keyword,dimdocsent])
        dimsum = MakeAllDimSum(sgt,dim_sent)
        for each in dimsum:
            sec_sent.append(each)
        for (eachdimnode,dimdocsent) in dim_sent:
            dimtitle = ('','We discuss {0} of {1}'.format(eachdimnode,sgt.keyword))
            sec_sent.append(dimtitle)
            for eachsent in dimdocsent:
                sec_sent.append(eachsent)
    if len(sgt.topic)>0:
        TopicDocCluster_dict = MakeTopicDocCluster(paperlist,keypath,sgt.topic)
        sec_sent.append(('','We next discussed following topics in {0}'.format(sgt.keyword)))
        topic_sent =[]
        for i, eachtopic in enumerate(sgt.topic):
            topicpaper = TopicDocCluster_dict[i]

            topdocsent,refdoc_idxlist = MakeSurveyBySGT(topicpaper,eachtopic,newkeypath,surv_conf)
            for docidx in refdoc_idxlist:
                ref.append(docidx)
            topic_sent.append([eachtopic.keyword,topdocsent])
        topsum = MakeAllDimSum(sgt,topic_sent)
        for each in topsum:
            sec_sent.append(each)
        i = 0
        n = len(topic_sent)
        for (eachtoptitle,topic_sent) in topic_sent:
           # toptitle = 'In this section, we discuss topic of {0} {1}'.format(eachtopnode,sgt.keyword)
            toptitle = maketopichead(i, n, eachtoptitle, parentkeyword=sgt.keyword)
            i = i + 1
            sec_sent.append(toptitle)
            for eachsent in topic_sent:
                sec_sent.append(eachsent)
    return sec_sent,ref

def MakeLeafDocSurvey(paperlist,keywordpath,surv_conf):
    docscore_list=[]
    docsent_list=[]
    refdoc_idxlist=[]
    breakthis = False
    for eachdoc in paperlist:
        swt,sortsent = RankOneDocSentByKeyPath(eachdoc.sent,keywordpath)
        if eachdoc.idx == '0044':
            breakthis = True
        else:
            breakthis = False
        if breakthis:
            print(('break for print ----',eachdoc.idx,'.'.join(keywordpath)))
            for i,each in enumerate(sortsent):
                print((i,each))
        docscore = RankDoc(swt)
        docscore_list.append(docscore)
        docsent_list.append(sortsent)
    topdoc = surv_conf['topdoc']
    topsent = surv_conf['topsent']
    sortdocidx = sxpKeyDist.sortlistidxbywt(docscore_list)
    topdocn = int(np.ceil(len(sortdocidx)*1.0*topdoc))
    topdocsent=[]
    i = 0
    for idx in sortdocidx[0:topdocn]:
        for j,sent in enumerate(docsent_list[idx][0:topsent]):
          #  sumsent=makedoctopsent(j, paperlist[idx].idx, sent)
            docid = paperlist[idx].idx
            #topdocsent.append(sent)

          #  topdocsent.append((docid,sent+'.'.join(keywordpath))) #this is to indicate that sent is from which doc
            topdocsent.append((docid, sent))  # this is to indicate that sent is from which doc
      #   docsum = u'. '.join(docsent_list[idx][0:topsent])
      # #  sumsent = "Finally, in [{0}], {1}".format(paperlist[idx].idx,docsum)
      #   sumsent = makeleafsum(i, topdocn, paperlist[idx].idx, docsum)
        i = i + 1

        refdoc_idxlist.append(paperlist[idx].idx)
    return topdocsent,refdoc_idxlist
def makedoctopsent(j,  idx, sent):
    usent = sxpTextEncode.makeutf(sent)
    a = usent
    if j == 0:
        if np.random.rand() > 0.5:
            a = "Authors introduced {0} in [{1}]".format(usent, idx)
        else:
            a = "In [{0}], {1}".format(idx, sent)
    return a
def makeleafsum(i,n,idx,sent):
    usent = sxpTextEncode.makeutf(sent)
    if np.random.rand() > 0.5:
        a="Authors introduced {0} in [{1}]".format(usent, idx)
    else:
        a="In [{0}], {1}".format(idx, sent)
    if i == n-1 and n >= 2:
        a = "Finally, " + a
    return a
def maketopichead(i,n,eachtoptitle,parentkeyword):
    h = makehead(n,i)
    toptitle = ('','{0} topic of {1} {2}'.format(h,eachtoptitle,parentkeyword))
    return toptitle
def makehead(n,i=0):
    if n == 1:
        return ["We mainly discuss"]
    if n == 2:
        a=[]
        a.append('First, we discuss')
        a.append('And, we also discuss')
        return a[i]
    if n > 2:
        a=[]
        a.append('First, we discuss')
        for i in range(n-2):
            a.append('Then, we introduce')

        a.append('And, we also discuss')
        return a[i]
def MakeTopicDocCluster(paperlist,keypath,topic):
    docscore_list = []

    topic_dict={}
    for i, eachnode in enumerate(topic):
        keypath.append(eachnode.keyword)
        docscoreklist=ComputeDocDist(paperlist,keypath)
        docscore_list.append(docscoreklist)
        topic_dict[i]=[]
    sc = np.array(docscore_list)
    topicidx = np.argmin(sc,0)
    for i, eachpap in enumerate(paperlist):
        ti = topicidx[i]
        topic_dict[ti].append(eachpap)

    return topic_dict
def ComputeDocDist(paperlist,keywordpath):
    docscore_list =[]
    docsent_list=[]
    for eachdoc in paperlist:
        swt,sortsent = RankOneDocSentByKeyPath(eachdoc.sent,keywordpath)
        docscore = RankDoc(swt)
        docscore_list.append(docscore)
        docsent_list.append(sortsent)
    return docscore_list


def MakeAllDimSum(sgt,dim_sent):
    sent='In this section, we discussed following works of {0} :'.format(sgt.keyword)
    # dims = []
    # for eachdim in dim_sent:
    #     dimname = eachdim[0]
    #     dimsent = eachdim[1]
    #     dims.append(dimname)
    # sent = sent + ', '.join(dims)
    #return [sent]
    return []

def SelectDocAndSent(docscore_list,docsent_list,topk=0.5):
    sortdocidx = sxpKeyDist.sortlistidxbywt(docscore_list)
    topdocn = len(sortdocidx)*1.0/topk
    topdocsent=[]
    for idx in sortdocidx[0:topdocn]:
        topdocsent.append(docsent_list[idx])
    return sortdocidx,topdocsent

def RankSentInDim(paperlist,nextkeypath,level):
    pass
def RankSentInTopic(paperlist,nextkeypath,level):
    pass
def RankDoc(swt):
    #here swt is a list of weights of sortsent
    w = np.array(swt)
    mv = np.average(w)
    mw = np.max(w)
    st = np.sum(w)
    return mv
def SelectSent(keywordpath,swt,sortsent,topk=3):
    return swt[0:topk],sortsent[0:topk]
    pass

def RankOneDocSentByKeyPath(docsentlist,keywordpath):
    distlist=[]
    for i,sent in enumerate(docsentlist):

        d1 = dist_sent_keyword(sent,keywordpath)
        distlist.append(d1)
    #note that swt are list of real numbers, not a np.array.
    swt,sortsent=sxpKeyDist.sortlistbywt(distlist,docsentlist)
    return swt,sortsent
global_conf={}
def dist_sent_keyword(sent,keywordpath):

    # a = 1.0
    # b = 0
    [a,b]=global_conf['dist_para']
    return a*sxpKeyDist.dg(sent,keywordpath)+b*sxpKeyDist.dl(sent,keywordpath)

def Test():
    paperlist = sxpdoc.GetTestDoc()
    sgt = sxpSGT.GetTestTemp1()
    surv,refdoc_idxlist  = MakeSurvey(paperlist,sgt)
    for each in surv:
        print(each)
    print('reference---')
    already =[]
    for idx in refdoc_idxlist:
        if idx in already:
            continue
        print((idx,paperlist[idx].title))
        already.append(idx)
def MakeSurveyRefPaper(projectname,testcasename,treename,surv_conf):
    subdir = './test/'+ projectname
    sxpReadFileMan.CheckMkDir(subdir)
    print(('going to save it at',subdir))
    paperlist = sxpdoc.GetSurveyAllRefDocs()
    paperidx_dict ={}
    for each in paperlist:
        paperidx_dict[each.idx]=each
    #sgt = sxpSGT.GetTestTemp1(treename)
    sgt = sxpSGT.GetTreeByName(treename)
    surv,refdoc_idxlist  = MakeSurvey(paperlist,sgt,surv_conf)
    for each in surv:
        print(each)
    print('reference---')
    already =[]
    ref_dict={}
    for eachpaper in paperlist:
        ref_dict[eachpaper.idx]=eachpaper
    for idx in refdoc_idxlist:
        if idx in already:
            continue
        pap = ref_dict[idx]
        print((idx,pap.title))
        already.append((idx,pap.title))
    fname = './test/'+ projectname + '/' + testcasename + '_' + treename + '.dict'
    result_dict={}
    result_dict['sent_list']=surv
    result_dict['ref_doc_idxlist']=already
    result_dict['paperidx_dict']=paperidx_dict
    sxpReadFileMan.SaveObject(result_dict,fname)
    return result_dict
def LoadResult(projectname,testcasename,treename):
    fname = './test/'+ projectname + '/' + testcasename + '_' + treename + '.dict'
    return sxpReadFileMan.LoadObject(fname)
def TestSurveyRefPaper(eachtest):

    projectname, testcasename, treename, surv_conf =LoadTestName(eachtest)
    result_dict = MakeSurveyRefPaper(projectname, testcasename, treename, surv_conf)
def LoadTestName(eachtest):
    projectname = "test";
    testcasename = "test";
    treename = "test";
    surv_conf = {'topdoc': 1.0, 'topsent': 2}
    global_conf['dist_para'] = [0., 1.]
    if eachtest == 'sgt5':
        projectname = 'surveych4'
        testcasename = 'test1dist'
        treename = "extractivedim"
        surv_conf = {'topdoc': 1.0, 'topsent': 2}
        global_conf['dist_para'] = [0., 1.]

    if eachtest == 'sgt4':
        projectname = 'surveych4'
        testcasename = 'test1dist'
        treename = "extractive"
        surv_conf = {'topdoc': 1.0, 'topsent': 2}
        global_conf['dist_para'] = [0., 1.]

    if eachtest == 'sgt3':
        projectname = 'surveych4'
        testcasename = 'test1dist'
        treename = "test"
        surv_conf = {'topdoc': 1.0, 'topsent': 2}
        global_conf['dist_para'] = [0., 1.]

    if eachtest=='sgt':
        projectname='surveych4'
        testcasename='test2dist'
        treename = "test"
        surv_conf={'topdoc':1.0,'topsent':2}
        global_conf['dist_para'] = [0.5, 0.5]

    if eachtest =='sgt2':# focuse on dh
        projectname='surveych4'
        testcasename='test0dist'
        treename = "test"
        surv_conf={'topdoc':1.0,'topsent':2}
        global_conf['dist_para']=[1.0,0]
    return projectname,testcasename,treename,surv_conf
def LoadTreeSurvey(eachtest):
    projectname,testcasename,treename, surv_dict=LoadTestName(eachtest)
    result_dict=LoadResult(projectname, testcasename, treename)
    sentlist=[]
    for id, eachsent in enumerate( result_dict['sent_list']):
        sentlist.append((eachsent[0],eachsent[1])) #because here eachsent is a tuple (id, senttext), where id is the reference di

    return sentlist, result_dict['paperidx_dict']
def PrintSurvey(eachtest):
    projectname, testcasename, treename, surv_dict = LoadTestName(eachtest)
    fname = './test/'+ projectname + '/' + testcasename + '_' + treename + '_'+eachtest+'_survey.txt'

    sentlist,paperidx_dict=LoadTreeSurvey(eachtest)
    fulltxt=""
    for (sid,sent) in sentlist:
        us =sxpJudgeCharacter.removestops([sent[1]])
        if len(sid)==0:
            sid='Section title:'
        print((sid,sent))
        fulltxt = fulltxt + "{0}, {1}\n".format(sid,sent)
    print('reference document title:-----------')
    fulltxt = fulltxt + 'Reference paper title:-----------'
    mylist =[]
    for each in list(paperidx_dict.keys()):
        mylist.append(each)
    mylist.sort(key=lambda x: x.lower())
    print(mylist)
    for each in mylist:
        if each in list(paperidx_dict.keys()):
            print((each,paperidx_dict[each].title))
            if len(each)==0:
                each="section title"
            if len(paperidx_dict[each].title)==0:
                title = "no title?"
            else:
                title =paperidx_dict[each].title
            fulltxt = fulltxt + "{0}, {1}\n".format(each, title)
        else:
            print((each,'not in dict'))
            fulltxt = fulltxt + "{0}, {1}\n".format(each, 'not in dict')
    sxpReadFileMan.SaveTxtFile(fname,fulltxt)
def TestSent(eachtest):
    sentlist,paperidx_dict=LoadTreeSurvey(eachtest)

    for (id,sent) in sentlist:
        us =sxpJudgeCharacter.removestops([sent[1]])
        print((id,sent))
    print((len(sentlist)))

def TestLoad():
    eachtest ='sgt2'
    sentlist,paperidx_dict=LoadTreeSurvey(eachtest)

    for (id,sent) in sentlist:
        us =sxpJudgeCharacter.removestops([sent])
        print((id,us[0]))
    print((len(sentlist)))
    eachtest ='sgt'
    sentlist,paperidx_dict=LoadTreeSurvey(eachtest)

    for (id,sent) in sentlist:
        us =sxpJudgeCharacter.removestops([sent])
        print((id,us[0]))
    print((len(sentlist)))
    eachtest ='sgt3'
    sentlist,paperidx_dict=LoadTreeSurvey(eachtest)

    for (id,sent) in sentlist:
        us =sxpJudgeCharacter.removestops([sent])
        print((id,us[0]))
    print((len(sentlist)))
def TestOnePaper():
    fid = '0044'
    paper = sxpdoc.GetRefDocByfid(fid)
    print((paper.title))
    # for i,s in enumerate( paper.sent):
    #     print(i, s)
    keywordpath1 = ['summarization','method','extractive','supervised']
    keywordpath2 = ['summarization', 'method', 'extractive', 'unsupervised']
    global_conf['dist_para']=[0.0,1.0]
    swt,sortsent=RankOneDocSentByKeyPath(paper.sent, keywordpath1)
    fulltxt = ""
    for i, s in enumerate(sortsent):
        print((i,s,swt[i]))
        fulltxt = fulltxt + "{0},{1},{2}\n".format(i,s,swt[i])
    eachtest = 'sgt5'
    projectname, testcasename, treename, surv_dict = LoadTestName(eachtest)
    fname = './test/' + projectname + '/' + testcasename + '_' + treename + '_' + eachtest +'_'+fid+'_sentrank.txt'
    sxpReadFileMan.SaveTxtFile(fname,fulltxt)
def TestOneSurvey():
    eachtest = 'sgt5'
    projectname, testcasename, treename, surv_conf = LoadTestName(eachtest)
    keywordpath1 = ['summarization','method','extractive','supervised'] #summarization.method.extractive.supervised
    keywordpath2 = ['summarization', 'method', 'extractive', 'unsupervised']
    fid = '0044'
    paper = sxpdoc.GetRefDocByfid(fid)
    print((paper.title))
    paperlist =[paper]
    topdocsent, refdoc_idxlist = MakeLeafDocSurvey(paperlist, keywordpath2, surv_conf)
    sec_sent = []
    fulltxt = ""
    for i, eachsent in enumerate(topdocsent):
        sec_sent.append(eachsent)
        fulltxt = fulltxt + "{0}, {1}\n".format(i,eachsent)
    fname = './test/' + projectname + '/' + testcasename + '_' + treename + '_' + eachtest +'_'+fid+'_survey.txt'
    sxpReadFileMan.SaveTxtFile(fname,fulltxt)

def main():
    TestSurveyRefPaper('sgt')
    TestSurveyRefPaper('sgt2')
    TestSurveyRefPaper('sgt3')
    TestSurveyRefPaper('sgt4')
    TestSurveyRefPaper('sgt5')
    #TestLoad()
    #TestSent('sgt4')
   # PrintSurvey('sgt')
   # PrintSurvey('sgt2')
   # PrintSurvey('sgt3')
   # PrintSurvey('sgt4')
  #  PrintSurvey('sgt5')
  #  TestOnePaper()
 #   TestOneSurvey()
if __name__ == '__main__':
    main()
