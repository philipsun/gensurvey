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
import sxpRemoveDup
class sxpNode:
    node_type=''
    node_text = ''
    node_child = []
    node_id =0
    node_idx=0
    def __init__(self,ndtype):
        self.notde_type=ndtype
        self.node_child=[]
        self.node_text = []
        self.node_title=''
        self.node_id =0
        self.node_idx=0
    def AddSubNode(self,sxpnode):
        self.node_child.append(sxpnode)
    def AddSubText(self,txtnd):
        self.node_text.append(txtnd)

fdir = './test/survey/papers_json'
pkdir = r'./test/survey/papers_pk'
graph_dir =   './test/survey/papers_graph'
data_dir =r'./test/survey'
sxpReadFileMan.CheckMkDir(fdir)
sxpReadFileMan.CheckMkDir(pkdir)
sxpReadFileMan.CheckMkDir(graph_dir)

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

            "survgenmethod": 'opt_num',
            "testname": 'wordquery_allv6ks_dual_sentrank'
        },
        {

            "survgenmethod": 'orig',
            "testname": 'dtfipf_all_stop'
        },
        {

            "survgenmethod": 'LR',
            "testname": 'dtfipf_all_stop'
        },
        {

            "survgenmethod": 'sim_abs',
            "testname": 'test_origin'
        }
        ,
        {

            "survgenmethod": 'diff_abs',
            "testname": 'test_origin'
        }
        ,
        {

            "survgenmethod": 'origin_abs',
            "testname": 'test_origin'
        }
        ,
        {

            "survgenmethod": 'LR',
            "testname": 'tfidf_BM25'
        }
    ]
    if maincmd:
        cmdlist = maincmd
    else:
        #cmd = 'TraverseShowSurvey'
        ci = [1,2,3]
        cmdlist=[]
        if 1 in ci:
            cmd = 'BuildSurveyChapterByRankResult'  # first step,
            cmdlist.append(cmd)
        if 2 in ci:
            cmd = 'TraverseMakeSurvey'  # second step
            cmdlist.append(cmd)

        if 3 in ci:
            cmd = 'TraverseShowSurvey'  # third step
            cmdlist.append(cmd)
    #cmdlist = ['BuildSurveyChapterByRankResult']
        #  cmd = 'TestLoadAllChapterModelDoc'
    if 'GenDocGenSurveByChiID' in cmdlist:
        survgenmethod = 'opt_num'
        testname = 'wordquery_allv6ks_dual_sentrank'
        chid = '4'
        subcmd = 'allchapter'
        if subcmd =='makeonechapter':
            GenDocGenSurveByChiID(chid,survgenmethod,testname)
            GenChpaterOrig(chid, testname)
        if subcmd == 'allchapter':
            MakeChapterOriginDocDict(testname)
        if subcmd == 'origin_abs':
            MakeChapterOriginRefAbs()
        if subcmd =='diff_abs':
            MakeDiffSimSurvByAbs(survgenmethod='diff_abs', testname='test_origin')
            MakeDiffSimSurvByAbs(survgenmethod='sim_abs', testname='test_origin')
    if 'MakeSurveyPaperDocDict' in cmdlist:
        MakeSurveyPaperDocDict()
    if 'BuildSurveyChapterByRankResult' in cmdlist:
        for eachtest in testdict:
          #  BuildSurveyChapterByRankResult(eachtest['survgenmethod'],eachtest['testname'])
          print('---------',eachtest)
          if eachtest['testname'] == 'test_origin':
             MakeSurveyByOriginResult(eachtest['survgenmethod'],eachtest['testname'])
          else:
             MakeSurveyByRankTopkResult(eachtest['survgenmethod'],eachtest['testname'])
    if 'TraverseMakeSurvey' in cmdlist:
        for eachtest in testdict:
            TraverseMakeSurvey(eachtest['survgenmethod'],eachtest['testname'])
    if 'TraverseShowSurvey' in cmdlist:
        for eachtest in testdict:
            TraverseShowSurvey(eachtest['survgenmethod'],eachtest['testname'])

    if 'MakeSurveyChapterID' in cmdlist:
        MakeSurveyChapterID()

    if 'TestLoadAllChapterModelDoc' in cmdlist:
        TestLoadAllChapterModelDoc()
    if 'TestSent' in cmdlist:
        TestSent()
    if 'TraverseSurveyGraph' in cmdlist:
        TraverseSurveyGraph()
    if 'TestWork' in cmdlist:
        TestWork()
    if 'Work' in cmdlist:
        Work()

    if 'LoadDocModelSentence' in cmdlist:
        print((LoadDocModelSentence()))
        LoadDocData()
    if 'abs' in cmdlist:
        fnamelist=LoadGraphFileName(pkdir,graph_dir)
        for f in fnamelist:
         print(f)
        fid = '0000'
        abs = LoadAbsCon(pkdir,graph_dir,fid,'abstract')
        for i in abs:
            print(i)
    if 'GetGraphNodeByTitleParaSent' in cmdlist:
        GetGraphNodeByTitleParaSent('0000','4-t Recent automatic text summarization extractive approaches',test_case='chapter_4')
        sentence_data_dict=LoadChapter4AllSentTitleSent()
        for each in sentence_data_dict['allch4sent']:
            print(each)
    if 'chapter4' in cmdlist:
        BuildChapter4()
    if 'showchapter4' in cmdlist:
        sentence_data_dict=LoadChapter4AllSentTitleSent()
        for each in sentence_data_dict['allch4sent']:
            print(each)
    if 'allsurveysent' in cmdlist:
        graph_dict, matrix_dict, sentence_data_dict = GetAllSentOfSurvey()
        for each in list(sentence_data_dict['sentence_dict'].items()):
            print(each)

def TestWork():
    TestProcessOne()
def Work():
    LoadExtractJsonFiles()
#    pkdir = r'./test/multipaper/papers_pk'
    ShowTitle(pkdir)
  #  TestProcessOne()
    BuildGraph()
    graph_dir =   './test/multipaper/papers_graph'
 #   LoadGraphFileName(pkdir,graph_dir)
def GetFileName(fdir,keystr):
    fname_dict={}
    fname_dict['grah_dict']=os.path.join(fdir, keystr)
    fname_dict['sentence_dict']=os.path.join(fdir,  keystr)
    return fname_dict
def ShowTitle(pkdir):
    fnamelist = sxpReadFileMan.GetDirFileListType(pkdir,'pk')
    graph_fname_list =[]
    for fname in fnamelist:
        graph_dict = sxpReadFileMan.LoadSxptext(fname)
        fid =graph_dict['id']
        title= graph_dict['title']
        print((fid,title))

def LoadGraphFileName(pkdir,graph_dir):
    fnamelist = sxpReadFileMan.GetDirFileListType(pkdir,'pk')
    graph_fname_list =[]
    for fname in fnamelist:
        graph_dict = sxpReadFileMan.LoadSxptext(fname)
    #    jsdict =  data_dict['jsdict']
    #    print(jsdict)
    #    graph_dir =   './test/multipaper/papers_graph'
        #print('build graph for',fname)
        #ParsePaperJson(jsdict,data_dict['id'],graph_dir)
        #here fid is 0000.pk, but not 0000, so this is still a problem.
        fid =graph_dict['id']
        title= graph_dict['title']
        graphname =fid +'.graph'
     #   graph_dict = MakeGraph(graph_root,graphname,graph_dir)
     #   sxpgraph = sxpGraphEngine.sxpNetwork(graph_dir,graphname,dbinit=False)
        graph_dictname = os.path.join(graph_dir,graphname+'.grah_dict')
        matrix_dictname = os.path.join(graph_dir,graphname+'.matrix_vec_dict')
        sentence_data_dictname =os.path.join(graph_dir,graphname+'.sentence_data_dict')
#        print('graphdict',graph_dictname)
        fname_dict={}
        fname_dict['fname']=fname
        fname_dict['graph_dictname']=graph_dictname
        fname_dict['matrix_dictname']=matrix_dictname
        fname_dict['sentence_data_dictname']=sentence_data_dictname
        fname_dict['graphname']=graphname
        fname_dict['title']=title
        fname_dict['fid']=fid
        graph_fname_list.append(fname_dict)

        #graph_dict=sxpReadFileMan.LoadSxptext(fdictname)

    return graph_fname_list
def BuildGraph():
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir =   r'./test/multipaper/papers_graph'
#    data_dir =r'./test/multipaper'
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    for fname_dict in graph_fname_list:
        data_dict = sxpReadFileMan.LoadSxptext(fname_dict['fname'])
        jsdict =  data_dict['jsdict']
    #    print(jsdict)
    #    graph_dir =   './test/multipaper/papers_graph'
        print(('build graph for',fname_dict['fname']))
        #here data_dict['id'] is 0000, not 0000.pk,
        ParsePaperJson(jsdict,data_dict['id'],graph_dir)
def BuildChapter4():
    fid = '0004'
    graph_root_sel = GetGraphNodeByTitle('0000','4-t Recent automatic text summarization extractive approaches')
    graph_root = graph_root_sel[0]
    title = 'chapter 4'
    PrepareData(fid,title,graph_root,graph_dir)

def LoadChapter4ModelSentence():
    sent_list,title_list= GetGraphNodeByTitleParaSent('0000','4-t Recent automatic text summarization extractive approaches')

    doc_dict ={}

    doc_dict['title']="chapter4"
    doc_dict['fid']='0004'

    md1=[]
    for (id, sent) in sent_list:
        md1.append((id,sent))
    md2=[]
    for id, sent in enumerate( title_list):
        md2.append((id,sent))
    doc_dict['model']=[md1,md2]
    return [doc_dict]
def LoadChapter4AllSentTitleSent():
    fid = '0000'
    test_case = 'chapter_4'
    [allsent,alltitle]=sxpReadFileMan.LoadSxptext(graph_dir + r'/all_sent_all_title_'+fid+'_'+test_case+".pk")
    sentence_data_dict = {}
    sentence_data_dict['allch4sent']=allsent
    sentence_data_dict['allch4title']=alltitle
    sentence_data_dict['abstraction']=GetAbs()
    sentence_data_dict['conclusion'] = GetCon()
    sentence_data_dict['abscon'] = GetAbsCon()
    return sentence_data_dict
def GetSentByFid(fid='0000'):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_model_sent_list = []
    for fname_dict in graph_fname_list:
        fname_dict = graph_fname_list[0]
        if fname_dict['fid']==fid:
            sentence_data_dict = sxpReadFileMan.LoadSxptext(fname_dict['sentence_data_dictname'])
            return sentence_data_dict
    return None

def LoadDocModelSentence():
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir = r'./test/multipaper/papers_graph'
#    data_dir = r'./test/multipaper'
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_model_sent_list = []
    for fname_dict in graph_fname_list:
        fname_dict = graph_fname_list[0]

        sentence_data_dict = sxpReadFileMan.LoadSxptext(fname_dict['sentence_data_dictname'])
        #because in sxpTestMan, we use (sid,sent) to produce Model Html File
        abstract =sentence_data_dict['abstract']#[each for (sentenceidstr,each) in sentence_data_dict['abstract']]
        conclusion = sentence_data_dict['conclusion']#[each for (sentenceidstr,each) in sentence_data_dict['conclusion']]
        doc_dict ={}
        doc_dict['model']=[abstract,conclusion]
        doc_dict['title']=fname_dict['title']
        doc_dict['fid']=fname_dict['fid']
        doc_model_sent_list.append(doc_dict)
    return doc_model_sent_list

def GetAbs():
    fid = '0000'
    return LoadAbsCon(pkdir, graph_dir, fid, 'abstract')

def GetCon():
    fid = '0000'
    return LoadAbsCon(pkdir, graph_dir, fid, 'conclusion')

def GetAbsCon():
    fid = '0000'
    return LoadAbsCon(pkdir, graph_dir, fid, 'all')
def LoadAbsCon(pkdir,graph_dir,fid, model='abstract'):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_dict_list = []
    for fname_dict in graph_fname_list:

     #   fname_dict = graph_fname_list[0]
        print((fname_dict['fid'])) #here fid is p_0000, but not p_0000.pk
        if fid == fname_dict['fid']:
            graph_dict, matrix_dict,sentence_data_dict=LoadFileDataByGraphFid(fname_dict['fid'])
            if model=='abstract':
                return sentence_data_dict['abstract']
            if model=='conclusion':
                return sentence_data_dict['conclusion']
            if model == 'all':
                allsent =[]
                for each in sentence_data_dict['abstract']:
                    allsent.append(each)
                for each in sentence_data_dict['conclusion']:
                    allsent.append(each)
                return allsent
    return None

def LoadDocData():
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_dict_list = []
    for fname_dict in graph_fname_list:
     #   fname_dict = graph_fname_list[0]
        graph_dict, matrix_dict,sentence_data_dict=LoadFileDataByGraphFid(fname_dict['fid'])
        doc_dict ={}
        doc_dict['model']=(sentence_data_dict['abstract'],sentence_data_dict['conclusion'])
        doc_dict['title']=fname_dict['title']
        doc_dict['fid']=fname_dict['fid']
        doc_dict['graph_dict']=graph_dict
        doc_dict['matrix_dict']=matrix_dict
        doc_dict_list.append(doc_dict)
    return doc_dict_list
def TestProcessOne():
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir =   r'./test/multipaper/papers_graph'
#    data_dir =r'./test/multipaper'
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)

    fname_dict=graph_fname_list[10]

    print((fname_dict['fname'],fname_dict['graphname'],fname_dict['graph_dictname'],fname_dict['matrix_dictname']))
    #the following commented code is for parsing json file of paper to build one graph for the
    json_dict = sxpReadFileMan.LoadSxptext(fname_dict['fname'])
    jsdict =  json_dict['jsdict']
##   # print(jsdict)
    graph_dict,matrix_dict,sentence_data_dict=ParsePaperJson(jsdict,json_dict['id'],graph_dir)
#    graph_dict = sxpReadFileMan.LoadSxptext(fname_dict['graph_dictname'])
#    matrix_dict = sxpReadFileMan.LoadSxptext(fname_dict['matrix_dictname'])
    print('abstract,*************')
    for sent in sentence_data_dict['abstract']:
        print(sent)
    print('conclusion,*************')
    for sent in sentence_data_dict['conclusion']:
        print(sent)

    print('sentence,*************')
    sentence_dict =sentence_data_dict['sentence_dict']
    for kid in sorted(sentence_dict.keys()):
        print((kid, sentence_dict[kid]))
    print((matrix_dict['d_c'].shape))
    print((matrix_dict['c_c'].shape))
    print((matrix_dict['c_p'].shape))
    print((matrix_dict['p_s'].shape))
    print((matrix_dict['s_k'].shape))

# the following codes are for showing how the matrix_dict is defined:
##    matrix_dict['section_vec']= section_vec
##    matrix_dict['paragraph_father']= paragraph_father
##    matrix_dict['paragraph_vec']= paragraph_vec
##    matrix_dict['sentence_vec']= sentence_vec
##    matrix_dict['sentence_vec_father']= sentence_vec_father
##    matrix_dict['d_c']= d_c
##    matrix_dict['c_c']= c_c
##    matrix_dict['c_p']= c_p
##    matrix_dict['p_s']= p_s
##    matrix_dict['s_k']= s_k
##    matrix_dict['sentence_dict']=sentence_dict
##    matrix_dict['word']=sentence_tfidf.word
##    matrix_dict['id']=graphname

def LoadExtractJsonFiles():

    fnamelist = sxpReadFileMan.GetDirFileListType(fdir,'json')

    for i, each in enumerate( fnamelist):
        print(('******', i))
        print(each)
        jstr = sxpReadFileMan.ReadTextUTF(each)
        if jstr is None:
            print('wrong in open')
            break
        us = sxpTextEncode.GetUnicode(jstr)
        jsdict = json.loads(us,encoding='utf-8')

        pkname = os.path.join(pkdir, 'p_{0:0>4}.pk'.format(i))
        json_dict ={}
        json_dict['fname']=each
        json_dict['id'] =  '{0:0>4}'.format(i)
        json_dict['title']=jsdict['title']
        json_dict['jsdict'] = jsdict
        sxpReadFileMan.StoreSxptext(json_dict,pkname)
def ParsePaperJson(jsdict,fid,graph_dir):
    title = jsdict['title']
    refid = jsdict['number']
    content_body = jsdict['content']
    node_dict = []
    root = sxpNode('root')
    root.node_title = "root"

    jsdict['kind']='Chapter'
    graph_root = ParseTree(jsdict,root)
    graphname =fid +'.graph'
 #   graph_dict = MakeGraph(graph_root,graphname,graph_dir)\
    graph_dict,matrix_dict,sentence_data_dict = MakeSubGraph(graph_root,graphname,graph_dir)
    graph_dict['title']=title
    matrix_dict['title']=title
    fdictname =  os.path.join(graph_dir, graphname+'.grah_dict')
    sxpReadFileMan.StoreSxptext(graph_dict,fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.matrix_vec_dict')
    sxpReadFileMan.StoreSxptext(matrix_dict,fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.sentence_data_dict')
    sxpReadFileMan.StoreSxptext(sentence_data_dict,fdictname)
    return graph_dict, matrix_dict,sentence_data_dict
def PrepareData(fid,title,graph_root,graph_dir):
    graphname =fid +'.graph'
 #   graph_dict = MakeGraph(graph_root,graphname,graph_dir)\
    graph_dict,matrix_dict,sentence_data_dict = MakeSubGraph(graph_root,graphname,graph_dir)
    graph_dict['title']=title
    matrix_dict['title']=title
    fdictname =  os.path.join(graph_dir, graphname+'.grah_dict')
    sxpReadFileMan.StoreSxptext(graph_dict,fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.matrix_vec_dict')
    sxpReadFileMan.StoreSxptext(matrix_dict,fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.sentence_data_dict')
    sxpReadFileMan.StoreSxptext(sentence_data_dict,fdictname)
    return graph_dict, matrix_dict,sentence_data_dict

def LoadFileDataByGraphFid(fid):
    graphname =fid +'.graph'
    fdictname =  os.path.join(graph_dir, graphname+'.grah_dict')
    graph_dict = sxpReadFileMan.LoadSxptext(fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.matrix_vec_dict')
    matrix_dict = sxpReadFileMan.LoadSxptext(fdictname)
    fdictname =  os.path.join(graph_dir, graphname+'.sentence_data_dict')
    sentence_data_dict=sxpReadFileMan.LoadSxptext(fdictname)
    return graph_dict, matrix_dict,sentence_data_dict
def makelabel(fullstr, labellen=10):
    nlen=len(fullstr)

    if nlen < labellen:
        return fullstr
    else:
        return fullstr[0:labellen]


def MakeGraph(graph_root, graphname, graph_dir):
    node_dict = {}
    node_stack = collections.deque([])
    node_stack.appendleft(graph_root)
    sxpgraph = sxpNetwork(graph_dir, graphname)
    node_name = 'root'
    node_label = makelabel(graph_root.node_title)
    rid = sxpgraph.AddNode(node_name, node_label, nodetype='root')
    node_dict = {}
    node_dict[rid] = graph_root
    sentence_dict = {}
    sentence_doc =[]
    while(len(node_stack)>0):
        cnd = node_stack.pop()
        for eachpara in cnd.node_text:
            node_name = 'para'
            node_label = makelabel(eachpara.node_title,30)
            nid = sxpgraph.AddNode(node_name, node_label, nodetype='para')
            node_dict[nid]=eachpara
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            sentenceset = sxpExtractText.MySentenceA(eachpara.node_title)
            print(eachpara.node_title)
            for eachsent in sentenceset:
                node_name = 'sentence'
                node_label = makelabel(eachsent, 30)
                sid = sxpgraph.AddNode(node_name, node_label,
                                       nodetype='sentence')
                sentnode = sxpNode('sentence')
                sentnode.node_title = eachsent
                node_dict[sid] = sentnode
                sentence_dict[sid] = eachsent
                sxpgraph.AddEdgeByID(nid, sid, edgename='contain')
                sentence_doc.append(eachsent)

        for eachsub in cnd.node_child:
            node_name = 'sub'
            node_label = makelabel(eachsub.node_title)
            nid = sxpgraph.AddNode(node_name, node_label, nodetype='section')
            node_dict[nid]=eachsub
            sxpgraph.AddEdgeByID(rid, nid, edgename='contain')

            node_stack.appendleft(eachsub)
    #one paper document has one word vector
    sxptfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentenceset)
    sxpgraph.Save()
    graph_dict = {}
    graph_dict['node_dict']=node_dict
    graph_dict['sentence_tfidf']=sxptfidf
    graph_dict['sxpgraph']=sxpgraph
    graph_dict['id']=graphname
    graph_dict['sentence_dict']= sentence_dict
    fdictname =  os.path.join(graph_dir, graphname+'.grah_dict')

    sxpReadFileMan.StoreSxptext(graph_dict,fdictname)

    return graph_dict

def GetSentence(graph_root,gid,graphname, graph_dir):
    node_dict = {}
    node_stack =collections.deque([])
    node_stack.appendleft((graph_root,0))
    sxpgraph = sxpNetwork(graph_dir, graphname)
    node_name = 'root'
    node_label = makelabel(graph_root.node_title)
    graph_root.node_id=0
    rid = sxpgraph.AddNode(node_name,node_label,nodetype='root')
    node_dict = {}
    node_dict[rid]=graph_root
    sentence_dict = {}
    sentence_doc =[]
    section_vec=[]
    section_father_vec=[]
    paragraph_vec=[]
    paragraph_father=[]
    sentence_vec =[]
    sentence_vec_father=[]
    word_vec=[]
    secid = 0
    paraid =0
    sentenceid=0
    current_secid=0
    abstract =[]
    conclusion =[]
    acknolwedge = []
    reference = []
    while(len(node_stack)>0):
        (cnd,current_secid) = node_stack.pop()
        rid = cnd.node_id

        for eachpara in cnd.node_text:
            node_name = 'para'
            node_label = makelabel(eachpara.node_title,30)
            nid = sxpgraph.AddNode(node_name,node_label,nodetype='para')
            eachpara.node_id = nid
            sentence_para_id =str(paraid)
            paragraph_vec.append(nid)
            paraid = paraid + 1
            paragraph_father.append(current_secid)
            node_dict[nid]=eachpara
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            sentenceset = sxpExtractText.MySentenceA(eachpara.node_title)
            for i, eachsent in enumerate( sentenceset):
                sentence_idstr = str(gid) + '.'+sentence_para_id + '.' + str(i)
                node_name = 'sentence'
                node_label = makelabel(eachsent,30)
                sid = sxpgraph.AddNode(node_name,node_label,nodetype='sentence')
                sentnode=sxpNode('sentence')
                sentnode.node_id=sid
                sentnode.node_title=eachsent
                node_dict[sid]=sentnode
                sentence_dict[sentenceid]=(sentence_idstr,eachsent)
                sxpgraph.AddEdgeByID(nid,sid,edgename='contain')
                sentence_doc.append(eachsent)
                sentence_vec.append(sid)
                sentenceid = sentenceid +1
                sentence_vec_father.append(paraid-1)
        for eachsub in cnd.node_child:
            node_name = 'sub'
            node_label = makelabel(eachsub.node_title)
            nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
            eachsub.node_id=nid
            node_dict[nid]=eachsub
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            section_vec.append(rid)
            section_father_vec.append(current_secid)
            node_stack.appendleft((eachsub,secid))
            secid=secid+1
    return sentence_dict
def GetSentenceAndTitle(graph_root,gid,graphname, graph_dir):
    node_dict = {}
    node_stack =collections.deque([])
    node_stack.appendleft((graph_root,0))
    sxpgraph = sxpNetwork(graph_dir, graphname)
    node_name = 'root'
    node_label = makelabel(graph_root.node_title)
    graph_root.node_id=0
    rid = sxpgraph.AddNode(node_name,node_label,nodetype='root')
    node_dict = {}
    node_dict[rid]=graph_root
    sentence_dict = {}
    sentence_doc =[]
    section_vec=[]
    section_father_vec=[]
    paragraph_vec=[]
    paragraph_father=[]
    sentence_vec =[]
    sentence_vec_father=[]
    word_vec=[]
    secid = 0
    paraid =0
    sentenceid=0
    current_secid=0
    abstract =[]
    conclusion =[]
    acknolwedge = []
    reference = []
    title_dict={}
    while(len(node_stack)>0):
        (cnd,current_secid) = node_stack.pop()
        rid = cnd.node_id

        for eachpara in cnd.node_text:
            node_name = 'para'
            node_label = makelabel(eachpara.node_title,30)
            nid = sxpgraph.AddNode(node_name,node_label,nodetype='para')
            eachpara.node_id = nid
            sentence_para_id =str(paraid)
            paragraph_vec.append(nid)
            paraid = paraid + 1
            paragraph_father.append(current_secid)
            node_dict[nid]=eachpara
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            sentenceset = sxpExtractText.MySentenceA(eachpara.node_title)
            for i, eachsent in enumerate( sentenceset):
                sentence_idstr = str(gid) + '.'+sentence_para_id + '.' + str(i)
                node_name = 'sentence'
                node_label = makelabel(eachsent,30)
                sid = sxpgraph.AddNode(node_name,node_label,nodetype='sentence')
                sentnode=sxpNode('sentence')
                sentnode.node_id=sid
                sentnode.node_title=eachsent
                node_dict[sid]=sentnode
                sentence_dict[sentenceid]=(sentence_idstr,eachsent)
                sxpgraph.AddEdgeByID(nid,sid,edgename='contain')
                sentence_doc.append(eachsent)
                sentence_vec.append(sid)
                sentenceid = sentenceid +1
                sentence_vec_father.append(paraid-1)
        for eachsub in cnd.node_child:
            node_name = 'sub'
            node_label = makelabel(eachsub.node_title)
            nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
            title_dict[nid]=eachsub.node_title
            eachsub.node_id=nid
            node_dict[nid]=eachsub
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            section_vec.append(rid)
            section_father_vec.append(current_secid)
            node_stack.appendleft((eachsub,secid))
            secid=secid+1
    return sentence_dict,title_dict
def GetSentenceFromNodeList(graph_root_list,graphname, graph_dir):
    all_sent = {}
    for i, graph_root in enumerate( graph_root_list):
        sent_dict = GetSentence(graph_root,i,graph_dir,graphname)
        for sid,sent in list(sent_dict.items()):
            all_sent[sid]=sent
    allsentlist=[]
    for sid in sorted(all_sent.keys()):
     allsentlist.append(all_sent[sid])
    return allsentlist
def GetSentenceTitleFromNodeList(graph_root_list,graphname, graph_dir):
    all_sent = {}
    all_title_dict={}
    for i, graph_root in enumerate( graph_root_list):
        sent_dict,title_dict = GetSentenceAndTitle(graph_root,i,graph_dir,graphname)
        for sid,sent in list(sent_dict.items()):
            all_sent[sid]=sent
        for sid,sent in list(title_dict.items()):
            all_title_dict[sid]=sent

    allsentlist=[]
    alltitlelist=[]
    for sid in sorted(all_sent.keys()):
     allsentlist.append(all_sent[sid])
    for sid in sorted(all_title_dict.keys()):
     alltitlelist.append(all_title_dict[sid])
    return allsentlist,alltitlelist

def MakeSubGraph(graph_root, graphname, graph_dir):
    node_dict = {}
    node_stack =collections.deque([])
    node_stack.appendleft((graph_root,0))
    sxpgraph = sxpNetwork(graph_dir, graphname)
    node_name = 'root'
    node_label = makelabel(graph_root.node_title)
    graph_root.node_id=0
    rid = sxpgraph.AddNode(node_name,node_label,nodetype='root')
    node_dict = {}
    node_dict[rid]=graph_root
    sentence_dict = {}
    sentence_doc =[]
    section_vec=[]
    section_father_vec=[]
    paragraph_vec=[]
    paragraph_father=[]
    sentence_vec =[]
    sentence_vec_father=[]
    word_vec=[]
    secid = 0
    paraid =0
    sentenceid=0
    current_secid=0
    abstract =[]
    conclusion =[]
    acknowledge = []
    reference = []
    while(len(node_stack)>0):
        (cnd,current_secid) = node_stack.pop()
        rid = cnd.node_id

        for eachpara in cnd.node_text:
            node_name = 'para'
            node_label = makelabel(eachpara.node_title,30)
            nid = sxpgraph.AddNode(node_name,node_label,nodetype='para')
            eachpara.node_id = nid
            sentence_para_id =str(paraid)
            paragraph_vec.append(nid)
            paraid = paraid + 1
            paragraph_father.append(current_secid)
            node_dict[nid]=eachpara
            sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
            sentenceset = sxpExtractText.MySentenceA(eachpara.node_title)
            for i, eachsent in enumerate( sentenceset):
                sentence_idstr = sentence_para_id + '.' + str(i)
                node_name = 'sentence'
                node_label = makelabel(eachsent,30)
                sid = sxpgraph.AddNode(node_name,node_label,nodetype='sentence')
                sentnode=sxpNode('sentence')
                sentnode.node_id=sid
                sentnode.node_title=eachsent
                node_dict[sid]=sentnode
                sentence_dict[sentenceid]=(sentence_idstr,eachsent)
                sxpgraph.AddEdgeByID(nid,sid,edgename='contain')
                sentence_doc.append(eachsent)
                sentence_vec.append(sid)
                sentenceid = sentenceid +1
                sentence_vec_father.append(paraid-1)
        for eachsub in cnd.node_child:
            node_name = 'sub'
            node_label = makelabel(eachsub.node_title)
            print(('section title:**********', node_label))
            if sxpExtractText.isabstract( eachsub.node_title,strict=True,stricttitle='Abstract'):
                abstract.append(eachsub)
                nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
                eachsub.node_id=nid
                node_dict[nid]=eachsub
                sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
                section_vec.append(rid)
                section_father_vec.append(current_secid)
                node_stack.appendleft((eachsub,secid))
                secid=secid+1
            elif sxpExtractText.isreference( eachsub.node_title):
                reference.append(eachsub)
            elif sxpExtractText.isconclusion( eachsub.node_title,strict=True,stricttitle='Conclusion'):
                conclusion.append(eachsub)
                nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
                eachsub.node_id=nid
                node_dict[nid]=eachsub
                sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
                section_vec.append(rid)
                section_father_vec.append(current_secid)
                node_stack.appendleft((eachsub,secid))
                secid=secid+1
            elif sxpExtractText.isacknolwedge( eachsub.node_title):
                acknowledge.append(eachsub)
            else:
                nid = sxpgraph.AddNode(node_name,node_label,nodetype='section')
                eachsub.node_id=nid
                node_dict[nid]=eachsub
                sxpgraph.AddEdgeByID(rid,nid,edgename='contain')
                section_vec.append(rid)
                section_father_vec.append(current_secid)
                node_stack.appendleft((eachsub,secid))
                secid=secid+1

    sentence_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentence_doc)

    if len(abstract)==0:
        print(("abstract is zeror*******",graphname))
    if len(abstract)==0:
        print(("conclusion is zeror*******",graphname))
    sentence_data_dict = {}
    sentence_data_dict['abstract']=GetSentenceFromNodeList(abstract,graphname, graph_dir)
    sentence_data_dict['reference']=GetSentenceFromNodeList(reference,graphname, graph_dir)
    sentence_data_dict['conclusion']=GetSentenceFromNodeList(conclusion,graphname, graph_dir)
    sentence_data_dict['acknowledge']=GetSentenceFromNodeList(acknowledge,graphname, graph_dir)
    sentence_data_dict['sentence_dict']=sentence_dict
##    print abstract
##    test = True
##    if test == True:
##        return
#***************************************************************
    print('we begin to build matrix')

    cs = len(section_vec)
    ps = len(paragraph_vec)
    ss = len(sentence_vec)
    ks = len(sentence_tfidf.word)
    print(('cs,ps,ss,ks:',cs,ps,ss,ks))
#first we build d-c matrix, which is actually a row vector
    print('d_c matrix')
    d_c = csr_matrix(np.ones((1,cs), dtype=np.float))

    print('building c_c matrix')
    c_c = csr_matrix((cs,cs), dtype=np.float64)
    for i, secid in enumerate( section_vec):
        f=section_father_vec[i]
        c_c[f,i]=1.0
    print('building c_p matrix')
    c_p = csr_matrix((cs,ps), dtype=np.float64)
    for i, paraid in enumerate( paragraph_vec):
        f=paragraph_father[i]
        c_p[f,i]=1.0
    print('building p_s matrix')
    p_s = csr_matrix((ps,ss), dtype=np.float64)
    for i, sentid in enumerate( sentence_vec):
        f=sentence_vec_father[i]
        p_s[f,i]=1.0

    print('building s_w matrix')
    s_k = csr_matrix((ss,ks), dtype=np.float64)

    for i, sentid in enumerate( sentence_vec):
        sxpnode = node_dict[sentid]
        if sxpnode.notde_type == 'sentence':
          vec = sentence_tfidf.vectorizer.transform([sxpnode.node_title])
          r,c = vec.shape
          for j in range(c):
             if vec[0,j]>0:
              s_k[i,j]=1


    print('save graph dict')
  #  sxpgraph.Save()
    graph_dict = {}
    graph_dict['node_dict']=node_dict
    graph_dict['sentence_tfidf']=sentence_tfidf
    graph_dict['sxpgraph']=sxpgraph
    graph_dict['id']=graphname
    graph_dict['sentence_dict']= sentence_dict
    matrix_dict={}
    print('save matrix dict')
    matrix_dict['section_vec']= section_vec
    matrix_dict['paragraph_father']= paragraph_father
    matrix_dict['paragraph_vec']= paragraph_vec
    matrix_dict['sentence_vec']= sentence_vec
    matrix_dict['sentence_vec_father']= sentence_vec_father
    matrix_dict['d_c']= d_c
    matrix_dict['c_c']= c_c
    matrix_dict['c_p']= c_p
    matrix_dict['p_s']= p_s
    matrix_dict['s_k']= s_k

    matrix_dict['word']=sentence_tfidf.word
    matrix_dict['id']=graphname

    return graph_dict,matrix_dict,sentence_data_dict

def ParseTree(jsdict,root):
    subnodes = []
    subnd = None
    txt_id =0
    if jsdict['kind'] == 'Chapter':
        if 'title' in jsdict:
            title = jsdict['title']
            subnd = sxpNode('Chapter')
            subnd.node_title=title
            root.AddSubNode(subnd)
        #    print('find sub node',title)
        if 'content' in jsdict:
            subnodes.append(jsdict['content'])
    if jsdict['kind']=='Paragraph':
        if 'content' in jsdict:
            txt = jsdict['content']
            txtnd = sxpNode('Paragraph')
            txtnd.node_title=txt
            txtnd.node_idx = txt_id
            txt_id = txt_id +1
            root.AddSubText(txtnd)
       #     print('find paragraph',txt)
    if len(subnodes)==1:
       content_body= subnodes[0]
       for eachdict in content_body:
        ParseTree(eachdict,subnd)
    return root
def GetGraphNodeByTitle(fid, graphnode_title):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_dict_list = []
    node_sel =[]
    for fname_dict in graph_fname_list:
      #  fname_dict = graph_fname_list[0]
        if fname_dict['fid']==fid:
            graph_dict, matrix_dict,sentence_data_dict=LoadFileDataByGraphFid(fname_dict['fid'])
            node_dict = graph_dict['node_dict']
            for k,graph_node in list(node_dict.items()):
                if graph_node.node_title == graphnode_title:
                    print(('find one',graphnode_title))
                    node_sel.append(graph_node)
    return node_sel

def GetAllSentOfSurvey():
    graph_dict, matrix_dict, sentence_data_dict = LoadFileDataByGraphFid('0000')
    return graph_dict, matrix_dict, sentence_data_dict
def GetGraphNodeByTitleParaSent(fid,graphnode_title,test_case='chapter_4'):
    graph_fname_list=LoadGraphFileName(pkdir,graph_dir)
    doc_dict_list = []
    node_sel =[]
    for fname_dict in graph_fname_list:
 #       fname_dict = graph_fname_list[0]
        if fname_dict['fid']==fid:
            graph_dict, matrix_dict,sentence_data_dict=LoadFileDataByGraphFid(fname_dict['fid'])
            node_dict = graph_dict['node_dict']
            for k,graph_node in list(node_dict.items()):
                if graph_node.node_title == graphnode_title:
                    print(('find one',graphnode_title))
                    node_sel.append(graph_node)
            break
    graph_name=test_case
    allsent,alltitle=GetSentenceTitleFromNodeList(node_sel,graph_name, graph_dir)
    print((len(allsent)))
    for eachsent in allsent:
        print(eachsent)
    for eachsent in alltitle:
        print(eachsent)
    sxpReadFileMan.StoreSxptext([allsent,alltitle],graph_dir + r'/all_sent_all_title_'+fid+'_'+test_case+".pk")
    return allsent,alltitle
def MakeDocModelBySentence(sentencelist,title,fid):
#    pkdir = r'./test/multipaper/papers_pk'
#    graph_dir = r'./test/multipaper/papers_graph'
#    data_dir = r'./test/multipaper'
    doc_model_sent_list =[]
    doc_dict ={}
    doc_dict['model']=[sentencelist]
    doc_dict['title']=title
    doc_dict['fid']=fid
    doc_model_sent_list.append(doc_dict)
    return doc_model_sent_list
def TraverseMakeSurvey(survgenmethod,testname):
    fid = '0000'
    graph_fname_list = LoadGraphFileName(pkdir, graph_dir)
    doc_dict_list = []
    node_sel = []
    graph_dict = None
    matrix_dict = None
    sentence_data_dict = None
    for fname_dict in graph_fname_list:
        #       fname_dict = graph_fname_list[0]
        if fname_dict['fid'] == fid:
            graph_dict, matrix_dict, sentence_data_dict = LoadFileDataByGraphFid(fname_dict['fid'])
            node_dict = graph_dict['node_dict']
            break
    graph_name = "allsection"
    for n,v in list(graph_dict['node_dict'].items()):
        print((n,v.notde_type))
        if v.notde_type == 'root':
            rootnode=v;
            break
    # self.node_text = []
    # self.node_title = ''
    # self.node_id = 0
    # self.node_idx = 0
    print((rootnode.node_title,rootnode.node_text))

    # allsent, alltitle = GetSentenceTitleFromNodeList([rootnode], graph_name, graph_dir)
    # for each in alltitle:
    #     print(each)
    # for each in allsent:
    #     print(each)
    chapter_sent_dict = {}
    chapter_title = []
    #TraverseNode(rootnode,chapter_sent_dict,chapter_title)

    chapter_sent_list = TraverseMakeNode(rootnode,chapter_sent_dict,chapter_title,survgenmethod,testname)
    fgensurvname = 'gen_survey_'+testname+'_'+survgenmethod + '.txt'
    fdir = data_dir
    pkname = fgensurvname + '.list'
    sxpReadFileMan.SaveObject(chapter_sent_list, pkname, fdir)

    reftxt = sxpReferMan.GetRefFidText()
    chapter_sent_list.append('REFERENCE')
    for each in reftxt:
        chapter_sent_list.append(each)

    stxt = ""
    for i,each in enumerate(chapter_sent_list):
        print(i,each)
        stxt = stxt + each + '\n'
    sxpReadFileMan.SaveTxtFile(fgensurvname,stxt,fdir)

def LoadGenSurveySentList(testname,survgenmethod):
    fgensurvname = 'gen_survey_'+testname+'_'+survgenmethod + '.txt'
    fdir = data_dir
    # stxt = ""
    # for i,each in enumerate(chapter_sent_list):
    #     print(i,each)
    #     stxt = stxt + each + '\n'

    stxt = sxpReadFileMan.ReadTextUTF(fgensurvname,fdir)
    fgensurvname = fgensurvname + '.list'
    chapter_sent_list=sxpReadFileMan.LoadObject( fgensurvname, fdir)
    return chapter_sent_list

def TraverseShowSurvey(survgenmethod,testname):
    # testname = 'wordquery_allv6'
    # testname = 'tfidf_all'
    # testname = 'wordquery_allv2'
    suverypaper = GetSuveryChapterSent()
    chapter_list = suverypaper['chapter_list']
    chapter_title = suverypaper['chapter_title']

    print('--------')
    #   sxpTestWordDistQuerySurvey.ShowAllChapter(testname)
    print(('--------', survgenmethod, testname))

    fname = testname + '_' + survgenmethod + 'chapter_gensurv_dict.dict'
    fullname = os.path.join(graph_dir, fname)
    chapter_gensurv_dict = sxpReadFileMan.LoadSxptext(fullname)
    for doc_dict in chapter_list:
        s = re.split(r'\-t|\-', doc_dict['title'])
        if len(s) <= 1:
            continue
        print(('====make surv for chapter', doc_dict['fid'], doc_dict['title']))
        print((s[0], s[1]))
        # testinfo ={'chname': '8.3', 'title': 'Asiya an evaluation toolkit\r', 'truth': [('CR6', 'Amigo et-al. 2005', '0074')], 'result': {'precision': 0.0, 'recall': 0.0, 'fscore': 0, 'jaccard': 0.0}, 'rankresult': [(59, '0059', 7.732764132345889, 'MEAD_ a platform for multidocument multilingual text summarization'), (44, '0044', 7.637370775510204, 'GraphSum: Discovering correlations among multiple terms for graph-based summarization'), (36, '0036', 7.482163455520166, 'Enhancing the Effectiveness of Clustering with Spectra Analysis'), (51, '0051', 7.480991840762236, 'Integrating importance, non-redundancy and coherence in graph-based extractive summarization'), (96, '0096', 7.434135479482766, 'Text summarization using a trainable summarizer and latent semantic analysis'), (31, '0031', 7.401016903103107, 'Document Summarization Based on Data Reconstruction'), (63, '0063', 7.389615629126119, 'Multi-document summarization based on two-level sparse representation model'), (41, '0041', 7.385117885951011, 'Fuzzy evolutionary optimization modeling and its applications to unsupervised categorization and extractive summarization'), (65, '0065', 7.366544230180594, 'Multi-document summarization exploiting frequent itemsets'), (16, '0016', 7.353331916250399, 'Automatic Detection of Opinion Bearing Words and Sentences'), (5, '0005', 7.33608024691358, 'A new sentence similarity measure and sentence based extractive technique for automatic text summarization'), (32, '0032', 7.319186179981635, 'Document summarization using conditional random fields'), (69, '0069', 7.292663262563827, 'NewsGist: A Multilingual Statistical News Summarizer'), (34, '0034', 7.279853379778249, 'Enhancing sentence-level clustering with ranking-based clustering framework for theme-based summarization'), (39, '0039', 7.265493119363532, 'FoDoSu: Multi-document summarization exploiting semantic analysis based on social Folksonomy'), (50, '0050', 7.263078512396694, 'Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis (PLSA) with sentence bases'), (106, '0106', 7.256840741583655, 'Using External Resources and Joint Learning for Bigram Weightingin ILP-Based Multi-Document Summarization'), (33, '0033', 7.250927194359985, 'Document summarization via guided sentence compression'), (73, '0073', 7.246243806276306, 'Predicting Salient Updates for Disaster Summarization'), (90, '0090', 7.244313743164474, 'Summarizing Email Conversations with Clue Words'), (110, '0110', 7.232675386444709, 'Weighted consensus multi-document summarization'), (107, '0107', 7.202208556503339, 'Using query expansion in graph-based approach for query-focused multi-document summarization'), (97, '0097', 7.160397907954664, 'TextRank_ bringing order into texts'), (42, '0042', 6.784758567810059, 'GA, MR, FFNN, PNN and GMM based models for automatic text summarization'), (14, '0014', 6.769455017301038, 'Assessing sentence scoring techniques for extractive text summarization'), (102, '0102', 6.68776397135337, 'Topic aspect-oriented summarization via group selection'), (68, '0068', 6.661811976809715, 'Multiple documents summarization based on evolutionary optimization algorithm'), (58, '0058', 6.643201410003675, 'MCMR: Maximum coverage and minimum redundant text summarization model'), (28, '0028', 6.63272679096454, 'Differential Evolution - A Simple and Efﬁcient Heuristic for Global Optimization over Continuous Spaces'), (71, '0071', 6.623505823546202, 'Opinion Mining and Sentiment Analysis'), (35, '0035', 6.6145224045968725, 'Enhancing the Effectiveness of Clustering with Spectra Analysi'), (38, '0038', 6.61011440339672, 'Fast and Robust Compressive Summarization with Dual Decomposition and Multi-Task Learning'), (7, '0007', 6.605081153161042, 'A text summarizer for Arabic'), (3, '0003', 6.56511080994898, 'A multi-document summarization system based on statistics and linguistic treatment'), (80, '0080', 6.555276920438957, 'ROUGE_ a package for automatic evaluation of summaries'), (0, '0000', 6.544226733780253, 'A complex network approach to text summarization'), (6, '0006', 6.5346093120129, 'A Survey of Text Summarization Extractive Techniques'), (2, '0002', 6.530537201953461, 'A language independent approach to multilingual text summarization'), (109, '0109', 6.522656323905023, 'WebInEssence_ a personalized web-based multidocument summarization and recommendation system'), (1, '0001', 6.501606596303195, 'A framework for multi-document abstractive summarization based on semantic role labelling'), (27, '0027', 6.499395833276237, 'Determinantal Point Processes for Machine Learning'), (104, '0104', 6.496924296982168, 'Topic Themes for Multi-Document Summarization'), (45, '0045', 6.494506640253359, 'Hybrid Algorithm for Multilingual Summarization of Hindi and Punjabi Documents'), (62, '0062', 6.4672666518155495, 'Multi-document abstractive summarization using ILP based multi-sentence compression.'), (94, '0094', 6.463662689448597, 'Syntactic Trimming of Extracted Sentences for Improving Extractive Multi-document Summarization'), (88, '0088', 6.461010179004967, 'Summarization of Multi-Document Topic Hierarchies using Submodular Mixtures'), (47, '0047', 6.456054854485141, 'Implementation and evaluation of evolutionary connectionist approaches to automated text summarization'), (66, '0066', 6.455924036281179, 'Multi-document summarization via budgeted maximization of submodular functions'), (4, '0004', 6.451603971361893, 'A neural attention model for abstractive sentence summarization'), (74, '0074', 6.4397378105390315, 'QARLA:A Framework for the Evaluation of Text Summarization Systems'), (72, '0072', 6.439102738184838, 'Opinosis: A Graph-Based Approach to Abstractive Summarization of Highly Redundant Opinions'), (21, '0021', 6.431331888019606, 'Building an Entity-Centric Stream Filtering Test Collection for TREC 2012'), (23, '0023', 6.421153630229971, 'Centroid-based summarization of multiple documents'), (64, '0064', 6.416658721229572, 'Multi-Document Summarization By Sentence Extraction'), (60, '0060', 6.405188590729969, 'Modeling Document Summarization as Multi-objective Optimization'), (43, '0043', 6.402147709840017, 'GistSumm_ a summarization tool based on a new extractive method'), (93, '0093', 6.401857638888889, 'SuPor: An Environment for AS of Texts in Brazilian Portuguese'), (67, '0067', 6.396924793849587, 'Multi-Sentence Compression: Finding Shortest Paths in Word Graphs'), (75, '0075', 6.376974482294494, 'QCS: A system for querying, clustering and summarizing documents'), (26, '0026', 6.375707205824305, 'Deriving concept hierarchies from text'), (95, '0095', 6.371048032208732, 'System Combination for Multi-document Summarization'), (85, '0085', 6.3710163392503585, 'Sentence extraction system asssembling multiple evidence'), (87, '0087', 6.362447970863684, 'Single-Document Summarization as a Tree Knapsack Problem'), (29, '0029', 6.361295776136093, 'Document clustering and text summarization'), (86, '0086', 6.360962524404375, 'Single-document and multi-document summarization techniques for email threads using sentence compression'), (56, '0056', 6.3486879561099325, 'Learning with Unlabeled Data for Text Categorization Using Bootstrapping and Feature Projection Techniques'), (99, '0099', 6.340772312129467, 'The anatomy of a large-scale hypertextual Web search engine'), (46, '0046', 6.340578803611267, 'Image collection summarization via dictionary learning for sparse representation'), (12, '0012', 6.340078125, 'Applying regression models to query-focused multi-document Summarization'), (8, '0008', 6.332982882340332, 'Abstractive Multi-Document Summarization via Phrase Selection and Merging'), (91, '0091', 6.332799286995087, 'Summarizing Emails with Conversational Cohesion and Subjectivity'), (70, '0070', 6.32318002676978, 'One Story, One Flow: Hidden Markov Story Models for Multilingual Multidocument Summarization'), (57, '0057', 6.322943286614498, 'Long story short - Global unsupervised models for keyphrase based meeting summarization'), (37, '0037', 6.320845582000113, 'Event graphs for information retrieval and multi-document summarization'), (15, '0015', 6.319254412056316, 'Automated Summarization Evaluation with Basic Elements'), (52, '0052', 6.314685547688463, 'Keyphrase Extraction for N-best Reranking in Multi-Sentence Compression'), (78, '0078', 6.314384765624999, 'Reader-aware multi-document summarization via sparse coding'), (53, '0053', 6.310630341880342, 'Large-margin learning of submodular summarization models'), (108, '0108', 6.307430844114923, 'Using Topic Themes for Multi-Document Summarization'), (17, '0017', 6.307106025819564, 'Automatic generic document summarization based on non-negative matrix factorization, Information Processing and Management'), (98, '0098', 6.290157229946054, 'TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages'), (19, '0019', 6.288075769578995, 'Biased LexRank_ Passage retrieval using random walks with question-based priors'), (11, '0011', 6.287489149305555, 'Analyzing the use of word graphs for abstractive text summarization'), (24, '0024', 6.277564482465407, 'Combining Syntax and Semantics for Automatic Extractive Single-document Summarization'), (76, '0076', 6.270711264898116, 'Ranking with Recursive Neural Networks and Its Application to Multi-document Summarization'), (100, '0100', 6.252403619568291, 'The automatic creation of literature abstracts'), (30, '0030', 6.248262524644623, 'Document concept lattice for text understanding and summarization'), (89, '0089', 6.237769371659604, 'Summarization System Evaluation Revisited: N-Gram Graphs'), (83, '0083', 6.230124457553925, 'Semantic graph reduction approach for abstractive Text Summarization'), (92, '0092', 6.2248052609866775, 'SUMMARIZING TEXT by RANKING TEXT UNITS ACCORDING to SHALLOW LINGUISTIC FEATURES'), (20, '0020', 6.219928146569073, 'Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory'), (54, '0054', 6.219269402279176, 'Learning Summary Prior Representation for Extractive Summarization'), (10, '0010', 6.217870218406767, 'An Extractive Text Summarizer Based on Significant Words'), (61, '0061', 6.18011836628512, 'Modeling Local Coherence: An Entity-based Approach'), (22, '0022', 6.169046977245687, 'Centering: A Framework for Modeling the Local Coherence of Discourse'), (84, '0084', 6.1125108131487895, 'Semantic Role Labelling with minimal resources: Experiments with French'), (49, '0049', 6.09940138626339, 'Information Extraction by an Abstractive Text Summarization for an Indian Regional Language'), (101, '0101', 6.059917355371901, 'The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries'), (48, '0048', 6.058926564875405, 'Improving the Estimation of Word Importance for News Multi-Document Summarization'), (40, '0040', 6.050426136363637, 'Framework for Abstractive Summarization using Text-to-Text Generation'), (25, '0025', 5.960007304601899, 'DEPEVAL(summ)_ dependency-based evaluation for automatic summaries'), (77, '0077', 5.7529218407596785, 'Re-evaluating Automatic Summarization with BLEU and 192 Shades of ROUGE'), (9, '0009', 5.642722117202268, 'Advances in Automatic Text Summarization'), (79, '0079', 4.744461540556365, 'Revisiting readability_ a unified framework for predicting text quality'), (82, '0082', 3.6746776323851797, 'Selecting a feature set to summarize texts in brazilian portuguese'), (55, '0055', 3.4094921514312095, 'Learning the parts of objects by non-negative matrix factorization'), (105, '0105', 3.0000438577255384, 'Unsupervised Clustering by k-medoids for Video Summarization'), (103, '0103', 2.9454761368522346, 'Topic keyword identification for text summarization using lexical clustering'), (81, '0081', 2.862244498394549, 'Scene Summarization for Online Image Collections'), (18, '0018', 2.816166428199792, 'Beyond keyword and cue-phrase matching: A sentence-based abstraction technique for information extraction'), (13, '0013', 1.8181818181818181, 'Aspects of sentence retrieval')]}
        chpater = s[0]
#        testinfo = sxpTestWordDistQuerySurvey.LoadChapterRankResult(testname, doc_dict['title'])

        topk=sxpTestWordDistQuerySurvey.LoadDualRankTopk(testname, survgenmethod, chpater)
        if topk is None:
            print(('no raw text for this chapter', doc_dict['title']))
            continue
        modelchapter = doc_dict['sent']
        src = ".".join(modelchapter)
        wordnum = len(src)
        sentlen = len(modelchapter)
        print('chapter model word len and sent len but in model para len',wordnum,'sentlen',sentlen)

        print("topk['chapter_gensum_topknum']", topk['chapter_gensum_topknum'])
        print("topk['true_citedoc_num']", topk['true_citedoc_num'])

        print("topk['chapter_gensum_sentnum']", topk['chapter_gensum_sentnum'])
        print("topk['survey_chapter_sent_len']", topk['survey_chapter_sent_len'])

        print("topk['chapter_gensum_word_len']", topk['chapter_gensum_word_len'])
        print("topk['survey_chapter_wd_len']", topk['survey_chapter_wd_len'])



#        print('begin to process chapter', (topk['title']))
        survey_sent = chapter_gensurv_dict[doc_dict['fid']]
        print('gensuv sentlen',len(survey_sent))
        s = '. '.join(survey_sent)
        print('gensurv wordlen',len(s))
        print(survey_sent)
def TraverseSurveyGraph():
    fid = '0000'
    graph_fname_list = LoadGraphFileName(pkdir, graph_dir)
    doc_dict_list = []
    node_sel = []
    graph_dict = None
    matrix_dict = None
    sentence_data_dict = None
    for fname_dict in graph_fname_list:
        #       fname_dict = graph_fname_list[0]
        if fname_dict['fid'] == fid:
            graph_dict, matrix_dict, sentence_data_dict = LoadFileDataByGraphFid(fname_dict['fid'])
            node_dict = graph_dict['node_dict']
            break
    graph_name = "allsection"
    for n,v in list(graph_dict['node_dict'].items()):
        print((n,v.notde_type))
        if v.notde_type == 'root':
            rootnode=v;
            break
    # self.node_text = []
    # self.node_title = ''
    # self.node_id = 0
    # self.node_idx = 0
    print((rootnode.node_title,rootnode.node_text))

    # allsent, alltitle = GetSentenceTitleFromNodeList([rootnode], graph_name, graph_dir)
    # for each in alltitle:
    #     print(each)
    # for each in allsent:
    #     print(each)
    chapter_sent_dict = {}
    chapter_title = []
    TraverseNode(rootnode,chapter_sent_dict,chapter_title)
    for title in chapter_title:
        print(title)
    chapter_list=[]
    chapter_fid_dict={}
    testname = 'wordquery_allv6'
    for i,chapter in enumerate(chapter_title):
        print(chapter)
        print((chapter_sent_dict[chapter]))
        testinfo = sxpTestWordDistQuerySurvey.LoadChapterRankResult(testname, chapter)
        if testinfo is None:
            continue
        chapter_dict = {}
        chapter_dict['fid']='{:0=4}'.format(i)
        chapter_fid_dict[chapter_dict['fid']]=chapter_sent_dict[chapter]
        chapter_dict['title']=chapter;
        chapter_dict['sent']=chapter_sent_dict[chapter]
        chapter_list.append(chapter_dict)
    suverypaper={}
    suverypaper['chapter_sent_dict']=chapter_sent_dict
    suverypaper['chapter_title'] = chapter_title
    suverypaper['rootnode'] = rootnode
    suverypaper['chapter_list']=chapter_list
    suverypaper['chapter_fid_dict']=chapter_fid_dict
    fname = os.path.join(graph_dir,graph_name +'.allchapter.dict')
    sxpReadFileMan.StoreSxptext(suverypaper,fname)
    chptertitle=GetAllChapterTitle()
    for t in chptertitle:
        print(t)
def MakeSurveyChapterID():
    suverypaper = GetSuveryChapterSent()
    chapter_list = suverypaper['chapter_list']
    chid_id_dict={}
    id_chid_dict={}
    for chapter_dict  in chapter_list:
        # chapter_dict = {}
        # chapter_dict['fid']='{:0=4}'.format(i)
        # chapter_fid_dict[chapter_dict['fid']]=chapter_sent_dict[chapter]
        # chapter_dict['title']=chapter;
        title = chapter_dict['title']
        s = re.split('\-t',title)
        if len(s)>=2:
            chid = s[0]
            ctitle = s[1]
            chapter_dict['keytile'] = s[1]
        else:
            chid = None
            print('no chid',title)
            chapter_dict['keytile'] = "None"
        fid = chapter_dict['fid']
        if chid:
            chid_id_dict[chid]=chapter_dict
            id_chid_dict[fid]=chapter_dict
    fname = 'survey_chid_id_dict.dict'
    survey_chid_id_dict = {}
    survey_chid_id_dict['chid_id_dict']=chid_id_dict
    survey_chid_id_dict['id_chid_dict'] = id_chid_dict
    for chid,iddict in chid_id_dict.items():
        print('chid',chid,iddict['fid'],iddict['title'])
    sxpReadFileMan.SaveObject(survey_chid_id_dict,fname,data_dir)
def GetSurveyChapterID():
    fname = 'survey_chid_id_dict.dict'
    return sxpReadFileMan.LoadObject(fname,data_dir)
def GetSuveryChapterSent():
    graph_name = "allsection"
    fname = os.path.join(graph_dir, graph_name + '.allchapter.dict')
    return sxpReadFileMan.LoadSxptext(fname)
def TraverseNode(rootnode,chapter_sent_dict,chapter_title):
    # print(rootnode.notde_type, rootnode.node_title, rootnode.node_text)

    if rootnode.node_title == 'Abstract':
        return []
    if rootnode.node_title == 'Keywords':
        return []

    if rootnode.node_title == 'Conclusion':
        return []
    st = re.split(r'\-t',rootnode.node_title)
    if len(st)==2:
        t = st[1]
    else:
        t = rootnode.node_title
    t = rootnode.node_title
    chapter_title.append(t)
    sentlist=[]
    for eachpara in rootnode.node_text:
        sentlist.append(eachpara.node_title)

    for each in rootnode.node_child:
        if each.notde_type == 'Chapter':
           subsent=TraverseNode(each,chapter_sent_dict,chapter_title)
           for eachsubsent in subsent:
               sentlist.append(eachsubsent)
    chapter_sent_dict[t] = sentlist
    return sentlist
    # print(len(allsent))
    # for eachsent in allsent:
    #     print(eachsent)
    # for eachsent in alltitle:
    #     print(eachsent)
    # sxpReadFileMan.StoreSxptext([allsent, alltitle],
    #                             graph_dir + r'/all_sent_all_title_' + fid + '_' + test_case + ".pk")
    # return allsent, alltitle
def TraverseMakeNode(rootnode,chapter_sent_dict,chapter_title,survgenmethod,testname,onlysub=False):
    # print(rootnode.notde_type, rootnode.node_title, rootnode.node_text)

    if rootnode.node_title == 'Abstract':
        return []
    if rootnode.node_title == 'Keywords':
        return []

    if rootnode.node_title == 'Conclusion':
        return []
    if rootnode.node_title == 'Reference':
        return []
    st = re.split(r'\-t',rootnode.node_title)
    if len(st)==2:
        chid = st[0]
        t = st[1]
    else:
        chid = None
        t = rootnode.node_title
    if len(rootnode.node_child)>0:
        haschild = True
    else:
        haschild = False
    t = rootnode.node_title
    chapter_title.append(t)
    sentlist=[]
    #add tilte to the section
    sentlist.append(t)
    if haschild == False and onlysub==False:
        if chid:
            survy = LoadGenSurveyByChid(chid,survgenmethod,testname)
            if survy is None:
                print('none survy for', chid,chapter_title)
            else:
                for s in survy:
                    sentlist.append(s)


    for each in rootnode.node_child:
        if each.notde_type == 'Chapter':
           subsent=TraverseMakeNode(each,chapter_sent_dict,chapter_title,survgenmethod,testname)
           for eachsubsent in subsent:
               sentlist.append(eachsubsent)

    chapter_sent_dict[t] = sentlist
    return sentlist
    # print(len(allsent))
    # for eachsent in allsent:
    #     print(eachsent)
    # for eachsent in alltitle:
    #     print(eachsent)
    # sxpReadFileMan.StoreSxptext([allsent, alltitle],
    #                             graph_dir + r'/all_sent_all_title_' + fid + '_' + test_case + ".pk")
    # return allsent, alltitle
def LoadAllChapterModelDoc():

    #    pkdir = r'./test/multipaper/papers_pk'
    #    graph_dir = r'./test/multipaper/papers_graph'
    #    data_dir = r'./test/multipaper'
    suverypaper = GetSuveryChapterSent()
    chapter_list =suverypaper['chapter_list']

    doc_model_sent_list = []
    for chapter_dict in chapter_list:
        doc_dict = {}

        doc_dict['model'] = [chapter_dict['sent']]
        doc_dict['title'] = chapter_dict['title']
        doc_dict['fid'] = chapter_dict['fid']
        doc_model_sent_list.append(doc_dict)
    return doc_model_sent_list
def TestLoadAllChapterModelDoc():
    surveypaper = GetSuveryChapterSent()
    chapter_list =surveypaper['chapter_list']
    print('----------TestLoadAllChapterModelDoc')
    for t in surveypaper['chapter_title']:
        print(t)
    print(surveypaper.keys())
    doc_model_sent_list = []
    doc_model_sent_dict={}
    for chapter_dict in chapter_list:
        doc_dict = {}

        doc_dict['model'] = [chapter_dict['sent']]
        doc_dict['title'] = chapter_dict['title']
        doc_dict['fid'] = chapter_dict['fid']
        print('--------chapter:')
        print(doc_dict['title'], doc_dict['fid'])
        cht=re.split('\-t',doc_dict['title'])
        if len(cht)>=2:
            chid = cht[0]
            chtitle = cht[1]
        else:
            chid = doc_dict['title']
            chtitle = doc_dict['title']
        doc_dict['chid']=chid
        doc_dict['chtitle']=chtitle

        doc_model_sent_list.append(doc_dict)
        doc_model_sent_dict[chid]=doc_dict
        for each in doc_dict['model']:
            print(each)
        print(doc_dict.keys())
    survey_sent=[]
    for t in surveypaper['chapter_title']:
        cht = re.split('\-t',t)

        if len(cht)>=2:
            chid = cht[0]
            chtitle = cht[1]
        else:
            chid = t
            chtitle = t
            if t == 'root':
                continue;
        if chid not in doc_model_sent_dict.keys():
            continue
        doc_dict = doc_model_sent_dict[chid]
        model = doc_dict['model']
        for m in model:
            for eachs in m:
                survey_sent.append(eachs)
    model_doc_list = []
    doc_dict ={}
    doc_dict['model']=[survey_sent]
    doc_dict['title']="automatic text survey generation"
    doc_dict['fid']="0000"
    model_doc_list.append(doc_dict)

    return model_doc_list

def GetAllChapterTitle():
    suverypaper = GetSuveryChapterSent()
    return suverypaper['chapter_title']
def GetChapterSentByFID(fid):
    suverypaper = GetSuveryChapterSent()
    return suverypaper['chapter_fid_dict'][fid]

def BuildSurveyChapterByRankResult(survgenmethod='abstract',testname = 'wordquery_allv6'):
    # testname = 'wordquery_allv6'
    # testname = 'tfidf_all'
    # testname = 'wordquery_allv2'
    suverypaper = GetSuveryChapterSent()
    chapter_list =suverypaper['chapter_list']
    chapter_title=suverypaper['chapter_title']

    print('--------')
 #   sxpTestWordDistQuerySurvey.ShowAllChapter(testname)
    print(('--------',survgenmethod,testname))
    chapter_gensurv_dict = {}
    for doc_dict in chapter_list:

        s = re.split(r'\-t|\-',doc_dict['title'])
        if len(s)<=1:
            continue
        print(doc_dict.keys())
        print(('====make surv for chapter',doc_dict['fid'], doc_dict['title']))
        print((s[0],s[1]))
        # testinfo ={'chname': '8.3', 'title': 'Asiya an evaluation toolkit\r', 'truth': [('CR6', 'Amigo et-al. 2005', '0074')], 'result': {'precision': 0.0, 'recall': 0.0, 'fscore': 0, 'jaccard': 0.0}, 'rankresult': [(59, '0059', 7.732764132345889, 'MEAD_ a platform for multidocument multilingual text summarization'), (44, '0044', 7.637370775510204, 'GraphSum: Discovering correlations among multiple terms for graph-based summarization'), (36, '0036', 7.482163455520166, 'Enhancing the Effectiveness of Clustering with Spectra Analysis'), (51, '0051', 7.480991840762236, 'Integrating importance, non-redundancy and coherence in graph-based extractive summarization'), (96, '0096', 7.434135479482766, 'Text summarization using a trainable summarizer and latent semantic analysis'), (31, '0031', 7.401016903103107, 'Document Summarization Based on Data Reconstruction'), (63, '0063', 7.389615629126119, 'Multi-document summarization based on two-level sparse representation model'), (41, '0041', 7.385117885951011, 'Fuzzy evolutionary optimization modeling and its applications to unsupervised categorization and extractive summarization'), (65, '0065', 7.366544230180594, 'Multi-document summarization exploiting frequent itemsets'), (16, '0016', 7.353331916250399, 'Automatic Detection of Opinion Bearing Words and Sentences'), (5, '0005', 7.33608024691358, 'A new sentence similarity measure and sentence based extractive technique for automatic text summarization'), (32, '0032', 7.319186179981635, 'Document summarization using conditional random fields'), (69, '0069', 7.292663262563827, 'NewsGist: A Multilingual Statistical News Summarizer'), (34, '0034', 7.279853379778249, 'Enhancing sentence-level clustering with ranking-based clustering framework for theme-based summarization'), (39, '0039', 7.265493119363532, 'FoDoSu: Multi-document summarization exploiting semantic analysis based on social Folksonomy'), (50, '0050', 7.263078512396694, 'Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis (PLSA) with sentence bases'), (106, '0106', 7.256840741583655, 'Using External Resources and Joint Learning for Bigram Weightingin ILP-Based Multi-Document Summarization'), (33, '0033', 7.250927194359985, 'Document summarization via guided sentence compression'), (73, '0073', 7.246243806276306, 'Predicting Salient Updates for Disaster Summarization'), (90, '0090', 7.244313743164474, 'Summarizing Email Conversations with Clue Words'), (110, '0110', 7.232675386444709, 'Weighted consensus multi-document summarization'), (107, '0107', 7.202208556503339, 'Using query expansion in graph-based approach for query-focused multi-document summarization'), (97, '0097', 7.160397907954664, 'TextRank_ bringing order into texts'), (42, '0042', 6.784758567810059, 'GA, MR, FFNN, PNN and GMM based models for automatic text summarization'), (14, '0014', 6.769455017301038, 'Assessing sentence scoring techniques for extractive text summarization'), (102, '0102', 6.68776397135337, 'Topic aspect-oriented summarization via group selection'), (68, '0068', 6.661811976809715, 'Multiple documents summarization based on evolutionary optimization algorithm'), (58, '0058', 6.643201410003675, 'MCMR: Maximum coverage and minimum redundant text summarization model'), (28, '0028', 6.63272679096454, 'Differential Evolution - A Simple and Efﬁcient Heuristic for Global Optimization over Continuous Spaces'), (71, '0071', 6.623505823546202, 'Opinion Mining and Sentiment Analysis'), (35, '0035', 6.6145224045968725, 'Enhancing the Effectiveness of Clustering with Spectra Analysi'), (38, '0038', 6.61011440339672, 'Fast and Robust Compressive Summarization with Dual Decomposition and Multi-Task Learning'), (7, '0007', 6.605081153161042, 'A text summarizer for Arabic'), (3, '0003', 6.56511080994898, 'A multi-document summarization system based on statistics and linguistic treatment'), (80, '0080', 6.555276920438957, 'ROUGE_ a package for automatic evaluation of summaries'), (0, '0000', 6.544226733780253, 'A complex network approach to text summarization'), (6, '0006', 6.5346093120129, 'A Survey of Text Summarization Extractive Techniques'), (2, '0002', 6.530537201953461, 'A language independent approach to multilingual text summarization'), (109, '0109', 6.522656323905023, 'WebInEssence_ a personalized web-based multidocument summarization and recommendation system'), (1, '0001', 6.501606596303195, 'A framework for multi-document abstractive summarization based on semantic role labelling'), (27, '0027', 6.499395833276237, 'Determinantal Point Processes for Machine Learning'), (104, '0104', 6.496924296982168, 'Topic Themes for Multi-Document Summarization'), (45, '0045', 6.494506640253359, 'Hybrid Algorithm for Multilingual Summarization of Hindi and Punjabi Documents'), (62, '0062', 6.4672666518155495, 'Multi-document abstractive summarization using ILP based multi-sentence compression.'), (94, '0094', 6.463662689448597, 'Syntactic Trimming of Extracted Sentences for Improving Extractive Multi-document Summarization'), (88, '0088', 6.461010179004967, 'Summarization of Multi-Document Topic Hierarchies using Submodular Mixtures'), (47, '0047', 6.456054854485141, 'Implementation and evaluation of evolutionary connectionist approaches to automated text summarization'), (66, '0066', 6.455924036281179, 'Multi-document summarization via budgeted maximization of submodular functions'), (4, '0004', 6.451603971361893, 'A neural attention model for abstractive sentence summarization'), (74, '0074', 6.4397378105390315, 'QARLA:A Framework for the Evaluation of Text Summarization Systems'), (72, '0072', 6.439102738184838, 'Opinosis: A Graph-Based Approach to Abstractive Summarization of Highly Redundant Opinions'), (21, '0021', 6.431331888019606, 'Building an Entity-Centric Stream Filtering Test Collection for TREC 2012'), (23, '0023', 6.421153630229971, 'Centroid-based summarization of multiple documents'), (64, '0064', 6.416658721229572, 'Multi-Document Summarization By Sentence Extraction'), (60, '0060', 6.405188590729969, 'Modeling Document Summarization as Multi-objective Optimization'), (43, '0043', 6.402147709840017, 'GistSumm_ a summarization tool based on a new extractive method'), (93, '0093', 6.401857638888889, 'SuPor: An Environment for AS of Texts in Brazilian Portuguese'), (67, '0067', 6.396924793849587, 'Multi-Sentence Compression: Finding Shortest Paths in Word Graphs'), (75, '0075', 6.376974482294494, 'QCS: A system for querying, clustering and summarizing documents'), (26, '0026', 6.375707205824305, 'Deriving concept hierarchies from text'), (95, '0095', 6.371048032208732, 'System Combination for Multi-document Summarization'), (85, '0085', 6.3710163392503585, 'Sentence extraction system asssembling multiple evidence'), (87, '0087', 6.362447970863684, 'Single-Document Summarization as a Tree Knapsack Problem'), (29, '0029', 6.361295776136093, 'Document clustering and text summarization'), (86, '0086', 6.360962524404375, 'Single-document and multi-document summarization techniques for email threads using sentence compression'), (56, '0056', 6.3486879561099325, 'Learning with Unlabeled Data for Text Categorization Using Bootstrapping and Feature Projection Techniques'), (99, '0099', 6.340772312129467, 'The anatomy of a large-scale hypertextual Web search engine'), (46, '0046', 6.340578803611267, 'Image collection summarization via dictionary learning for sparse representation'), (12, '0012', 6.340078125, 'Applying regression models to query-focused multi-document Summarization'), (8, '0008', 6.332982882340332, 'Abstractive Multi-Document Summarization via Phrase Selection and Merging'), (91, '0091', 6.332799286995087, 'Summarizing Emails with Conversational Cohesion and Subjectivity'), (70, '0070', 6.32318002676978, 'One Story, One Flow: Hidden Markov Story Models for Multilingual Multidocument Summarization'), (57, '0057', 6.322943286614498, 'Long story short - Global unsupervised models for keyphrase based meeting summarization'), (37, '0037', 6.320845582000113, 'Event graphs for information retrieval and multi-document summarization'), (15, '0015', 6.319254412056316, 'Automated Summarization Evaluation with Basic Elements'), (52, '0052', 6.314685547688463, 'Keyphrase Extraction for N-best Reranking in Multi-Sentence Compression'), (78, '0078', 6.314384765624999, 'Reader-aware multi-document summarization via sparse coding'), (53, '0053', 6.310630341880342, 'Large-margin learning of submodular summarization models'), (108, '0108', 6.307430844114923, 'Using Topic Themes for Multi-Document Summarization'), (17, '0017', 6.307106025819564, 'Automatic generic document summarization based on non-negative matrix factorization, Information Processing and Management'), (98, '0098', 6.290157229946054, 'TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages'), (19, '0019', 6.288075769578995, 'Biased LexRank_ Passage retrieval using random walks with question-based priors'), (11, '0011', 6.287489149305555, 'Analyzing the use of word graphs for abstractive text summarization'), (24, '0024', 6.277564482465407, 'Combining Syntax and Semantics for Automatic Extractive Single-document Summarization'), (76, '0076', 6.270711264898116, 'Ranking with Recursive Neural Networks and Its Application to Multi-document Summarization'), (100, '0100', 6.252403619568291, 'The automatic creation of literature abstracts'), (30, '0030', 6.248262524644623, 'Document concept lattice for text understanding and summarization'), (89, '0089', 6.237769371659604, 'Summarization System Evaluation Revisited: N-Gram Graphs'), (83, '0083', 6.230124457553925, 'Semantic graph reduction approach for abstractive Text Summarization'), (92, '0092', 6.2248052609866775, 'SUMMARIZING TEXT by RANKING TEXT UNITS ACCORDING to SHALLOW LINGUISTIC FEATURES'), (20, '0020', 6.219928146569073, 'Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory'), (54, '0054', 6.219269402279176, 'Learning Summary Prior Representation for Extractive Summarization'), (10, '0010', 6.217870218406767, 'An Extractive Text Summarizer Based on Significant Words'), (61, '0061', 6.18011836628512, 'Modeling Local Coherence: An Entity-based Approach'), (22, '0022', 6.169046977245687, 'Centering: A Framework for Modeling the Local Coherence of Discourse'), (84, '0084', 6.1125108131487895, 'Semantic Role Labelling with minimal resources: Experiments with French'), (49, '0049', 6.09940138626339, 'Information Extraction by an Abstractive Text Summarization for an Indian Regional Language'), (101, '0101', 6.059917355371901, 'The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries'), (48, '0048', 6.058926564875405, 'Improving the Estimation of Word Importance for News Multi-Document Summarization'), (40, '0040', 6.050426136363637, 'Framework for Abstractive Summarization using Text-to-Text Generation'), (25, '0025', 5.960007304601899, 'DEPEVAL(summ)_ dependency-based evaluation for automatic summaries'), (77, '0077', 5.7529218407596785, 'Re-evaluating Automatic Summarization with BLEU and 192 Shades of ROUGE'), (9, '0009', 5.642722117202268, 'Advances in Automatic Text Summarization'), (79, '0079', 4.744461540556365, 'Revisiting readability_ a unified framework for predicting text quality'), (82, '0082', 3.6746776323851797, 'Selecting a feature set to summarize texts in brazilian portuguese'), (55, '0055', 3.4094921514312095, 'Learning the parts of objects by non-negative matrix factorization'), (105, '0105', 3.0000438577255384, 'Unsupervised Clustering by k-medoids for Video Summarization'), (103, '0103', 2.9454761368522346, 'Topic keyword identification for text summarization using lexical clustering'), (81, '0081', 2.862244498394549, 'Scene Summarization for Online Image Collections'), (18, '0018', 2.816166428199792, 'Beyond keyword and cue-phrase matching: A sentence-based abstraction technique for information extraction'), (13, '0013', 1.8181818181818181, 'Aspects of sentence retrieval')]}
        testinfo = sxpTestWordDistQuerySurvey.LoadChapterRankResult(testname,doc_dict['title'])
        print(testinfo.keys())
        if testinfo is None:
            print(('no raw text for this chapter',doc_dict['title']))
            continue
        print('begin to process chapter', (testinfo['title']))
        survey_sent=MakeChapterSurvey(testname, doc_dict,testinfo,survgenmethod)
        print(survey_sent)
        chapter_gensurv_dict[doc_dict['fid']]=survey_sent
    fname = testname+'_'+ survgenmethod + 'chapter_gensurv_dict.dict'
    fullname = os.path.join(graph_dir,fname)
    sxpReadFileMan.StoreSxptext(chapter_gensurv_dict,fullname)
def MakeSurveyByRankTopkResult(survgenmethod,testname):
    # testname = 'wordquery_allv6'
    # testname = 'tfidf_all'
    # testname = 'wordquery_allv2'
    suverypaper = GetSuveryChapterSent()
    chapter_list = suverypaper['chapter_list']
    chapter_title = suverypaper['chapter_title']

    print('--------')
    #   sxpTestWordDistQuerySurvey.ShowAllChapter(testname)
    print(('--------', survgenmethod, testname))
    chapter_gensurv_dict = {}
    for doc_dict in chapter_list:
        s = re.split(r'\-t|\-', doc_dict['title'])
        if len(s) <= 1:
            continue
        print(('====make surv for chapter', doc_dict['fid'], doc_dict['title']))
        print((s[0], s[1]))
        chpater = s[0]
        if topkkword(survgenmethod):
            loaddata = 'LR'
        else:
            loaddata = survgenmethod
        topk=sxpTestWordDistQuerySurvey.LoadDualRankTopk(testname, loaddata, chpater)
        print('begin to process chapter', (doc_dict['title']))
        #survey_sent = MakeChapterSurvey(testname, doc_dict,testinfo,survgenmethod)
        survey_sent = MakeChapterSurveyFromTopk(topk, doc_dict, testname, survgenmethod)
        print(survey_sent)
        chapter_gensurv_dict[doc_dict['fid']]=survey_sent
    fname = testname+'_'+ survgenmethod + 'chapter_gensurv_dict.dict'
    fullname = os.path.join(graph_dir,fname)
    sxpReadFileMan.StoreSxptext(chapter_gensurv_dict,fullname)
def ShowTopkChid(testname,topkmethod,chpater):
    return sxpTestWordDistQuerySurvey.ShowTopkChid(testname,topkmethod,chpater)
def MakeSurveyByOriginResult(survgenmethod,testname):
    # testname = 'wordquery_allv6'
    # testname = 'tfidf_all'
    # testname = 'wordquery_allv2'
    suverypaper = GetSuveryChapterSent()
    chapter_list = suverypaper['chapter_list']
    chapter_title = suverypaper['chapter_title']

    print('--------')
    #   sxpTestWordDistQuerySurvey.ShowAllChapter(testname)
    print(('--------', survgenmethod, testname))
    chapter_gensurv_dict = {}
    for doc_dict in chapter_list:
        s = re.split(r'\-t|\-', doc_dict['title'])
        if len(s) <= 1:
            continue
        print(('====make surv for chapter', doc_dict['fid'], doc_dict['title']))
        print((s[0], s[1]))
        chpater = s[0]
       # topk=sxpTestWordDistQuerySurvey.LoadDualRankTopk(testname, survgenmethod, chpater)
        print('begin to process chapter', (doc_dict['title']))
        #survey_sent = MakeChapterSurvey(testname, doc_dict,testinfo,survgenmethod)
       # survey_sent = MakeChapterSurveyFromTopk(topk, doc_dict, testname, survgenmethod)
        survey_sent = LoadChapterOriginRefAbs(doc_dict['fid'], survgenmethod, testname)
        print(survey_sent)
        chapter_gensurv_dict[doc_dict['fid']]=survey_sent
    fname = testname+'_'+ survgenmethod + 'chapter_gensurv_dict.dict'
    fullname = os.path.join(graph_dir,fname)
    sxpReadFileMan.StoreSxptext(chapter_gensurv_dict,fullname)
def MakeSurveyPaperDocDict():
    suverypaper = GetSuveryChapterSent()
    chapter_list = suverypaper['chapter_list']
    chapter_title = suverypaper['chapter_title']

    print('-------- making survey chapter doc dict object')
    #   sxpTestWordDistQuerySurvey.ShowAllChapter(testname)

    chapter_fid_title_dict = {}
    for doc_dict in chapter_list:
        s = re.split(r'\-t|\-', doc_dict['title'])
        if len(s) <= 1:
            continue
        print(doc_dict)
        print(('====save dict for chapter', doc_dict['fid'], doc_dict['title']))
        print((s[0], s[1]))
        chpater = s[0]

        chapter_fid_title_dict[chpater]=doc_dict
    fname = 'chapter_fid_title_dict.dict'
    fullname = os.path.join(graph_dir,fname)
    sxpReadFileMan.StoreSxptext(chapter_fid_title_dict,fullname)
def LoadSurveyDocDict():
    fname = 'chapter_fid_title_dict.dict'
    fullname = os.path.join(graph_dir,fname)
    return sxpReadFileMan.LoadSxptext(fullname)

def GenDocGenSurveByChiID(chid,survgenmethod='abstract',testname='wordquery_allv6'):
    survey_chid_id_dict= GetSurveyChapterID()

    chapter_fid_dict = survey_chid_id_dict['chid_id_dict']

    if chid in chapter_fid_dict.keys():
        chapter_content_dict = chapter_fid_dict[chid]
        fid = chapter_content_dict['fid']
        gensurvsent = LoadGenSurvey(fid, survgenmethod, testname)
    else:
        fid = None
        return None
    chapter_fid_title_dict = LoadSurveyDocDict()
    doc_dict = chapter_fid_title_dict[chid]
    chapter_org_sent = doc_dict['sent']
    print(('====save dict for chapter', doc_dict['fid'], doc_dict['title']))
    print('origin chapter',chapter_org_sent)
    print('----gen surv',gensurvsent)
    topk = sxpTestWordDistQuerySurvey.LoadDualRankTopk(testname, survgenmethod, chid)
    refpaper_abstract = []
    for eachpaper in topk['chapter_gensum_topk']:
        fid = eachpaper['fid']
        title = eachpaper['title']

        refpaperlist = sxpMultiPaperData.LoadGraphMatrixSentence([fid])
        if not refpaperlist:
            return None;
        print((fid,title))
        sentence_data_dict = refpaperlist[0]['sentence_data_dict']
        abstract =sentence_data_dict['abstract']
        print(abstract)
        if survgenmethod == 'abstract':
            refpaper_abstract.append(abstract)

    testinfo = sxpTestWordDistQuerySurvey.GetChapterTestInfo(testname, chid)
    fulltxt_fid_list = testinfo['truth']
    for each in fulltxt_fid_list:
        print(each)
    chapter_doc_dict ={}
    chapter_doc_dict['gensurvsent']=gensurvsent
    chapter_doc_dict['doc_dict'] = doc_dict
    chapter_doc_dict['refpaper_abstract'] = refpaper_abstract
    chapter_doc_dict['chid'] = chid
    chapter_doc_dict['topk']= topk
    chapter_doc_dict['origreflist']=fulltxt_fid_list
    fname = 'chapter_doc_dict_'+chid + '_'+testname + '_'+survgenmethod + '.dict'
    fullname = os.path.join(pkdir,fname)
    sxpReadFileMan.SaveObject(chapter_doc_dict,fullname)
    return chapter_doc_dict
def GenChpaterOrig(chid,testname='wordquery_allv6ks_dual_sentrank'):
    survey_chid_id_dict= GetSurveyChapterID()

    chapter_fid_dict = survey_chid_id_dict['chid_id_dict']

    if chid in chapter_fid_dict.keys():
        chapter_content_dict = chapter_fid_dict[chid]
        fid = chapter_content_dict['fid']
    else:
        fid = None
        return None
    chapter_fid_title_dict = LoadSurveyDocDict()
    doc_dict = chapter_fid_title_dict[chid]
    chapter_org_sent = doc_dict['sent']
    print(('====save dict for chapter', doc_dict['fid'], doc_dict['title']))
    print('origin chapter',chapter_org_sent)
    title = doc_dict['title']
    chapter_refid_dict = sxpReferMan.GetRefFid()
    testinfo = sxpTestWordDistQuerySurvey.GetChapterTestInfo(testname, chid)

    fulltxt_fid_list = testinfo['truth']
    originrefpaper_abstract = {}
    for eachpaper in fulltxt_fid_list:
        fid = eachpaper[2]
        if fid in chapter_refid_dict.keys():
            refdict = chapter_refid_dict[fid]
            refname = refdict['refname']
        else:
            refname = fid

        refpaperlist = sxpMultiPaperData.LoadGraphMatrixSentence([fid])
        if not refpaperlist:
            return None;
        sentence_data_dict = refpaperlist[0]['sentence_data_dict']
        abstract =sentence_data_dict['abstract']
        print(abstract)
        originrefpaper_abstract[fid]=[refname,abstract]
    print('there are total refs num:---',len(fulltxt_fid_list))
    print('there are total refs num:---', len(originrefpaper_abstract))

    chapter_doc_dict ={}

    chapter_doc_dict['doc_dict'] = doc_dict
    chapter_doc_dict['originrefpaper_abstract'] = originrefpaper_abstract
    chapter_doc_dict['chid'] = chid
    chapter_doc_dict['title'] = title

    chapter_doc_dict['origreflist']=fulltxt_fid_list
    fname = 'chapter_origin_doc_dict_'+chid +'_'+testname+ '.dict'
    fullname = os.path.join(pkdir,fname)
    sxpReadFileMan.SaveObject(chapter_doc_dict,fullname)
    return chapter_doc_dict
def LoadChpaterOrig(chid,testname='wordquery_allv6ks_dual_sentrank'):

    fname = 'chapter_origin_doc_dict_'+chid +'_'+testname+ '.dict'
    fullname = os.path.join(pkdir,fname)
    return sxpReadFileMan.LoadObject(fullname)

def MakeChapterOriginDocDict(testname):
    surveypaper = GetSuveryChapterSent()
    chapter_list =surveypaper['chapter_list']
    print('----------TestLoadAllChapterModelDoc')
    for t in surveypaper['chapter_title']:
        print(t)
    print(surveypaper.keys())
    doc_model_sent_list = []
    doc_model_sent_dict={}
    for chapter_dict in chapter_list:
        doc_dict = {}

        doc_dict['model'] = [chapter_dict['sent']]
        doc_dict['title'] = chapter_dict['title']
        doc_dict['fid'] = chapter_dict['fid']
        print('--------chapter:')
        print(doc_dict['title'], doc_dict['fid'])
        cht=re.split('\-t',doc_dict['title'])
        if len(cht)>=2:
            chid = cht[0]
            chtitle = cht[1]
        else:
            chid = doc_dict['title']
            chtitle = doc_dict['title']
        doc_dict['chid']=chid
        doc_dict['chtitle']=chtitle

        doc_model_sent_list.append(doc_dict)
        doc_model_sent_dict[chid]=doc_dict
        for each in doc_dict['model']:
            print(each)
        print(doc_dict.keys())
        GenChpaterOrig(chid, testname)


def MakeChapterOriginRefAbs(survgenmethod='origin_abs', testname='test_origin'):
    surveypaper = GetSuveryChapterSent()
    chapter_list =surveypaper['chapter_list']
    print('----------TestLoadAllChapterModelDoc')
    for t in surveypaper['chapter_title']:
        print(t)
    print(surveypaper.keys())
    doc_model_sent_list = []
    doc_model_sent_dict={}
    chapter_gensurv_dict={}
    for chapter_dict in chapter_list:
        doc_dict = {}

        doc_dict['model'] = [chapter_dict['sent']]
        doc_dict['title'] = chapter_dict['title']
        doc_dict['fid'] = chapter_dict['fid']
        print('--------chapter:')
        print(doc_dict['title'], doc_dict['fid'])
        cht=re.split('\-t',doc_dict['title'])
        if len(cht)>=2:
            chid = cht[0]
            chtitle = cht[1]
        else:
            chid = doc_dict['title']
            chtitle = doc_dict['title']
        doc_dict['chid']=chid
        doc_dict['chtitle']=chtitle

        doc_model_sent_list.append(doc_dict)
        doc_model_sent_dict[chid]=doc_dict
        for each in doc_dict['model']:
            print(each)
        print(doc_dict.keys())
        chapter_doc_dict=LoadChpaterOrig(chid)
        surv_sent = []
        for refid,(refname, abstract) in chapter_doc_dict['originrefpaper_abstract'].items():
            #refname, abstract = abstractinfo
            if len(abstract)==0:
                continue
            surv_sent.append("In this work {0}, the authors proposed contributions".format(refname))
            for s in abstract:
                surv_sent.append(s[1])
        print('abstract as survy',surv_sent)
        chapter_gensurv_dict[doc_dict['fid']] = surv_sent
    #fname = testname + '_' + survgenmethod + 'chapter_gensurv_dict.dict'
    fname = testname + '_' + survgenmethod + 'chapter_gensurv_dict.dict'
    fullname = os.path.join(graph_dir, fname)
    sxpReadFileMan.SaveObject(chapter_gensurv_dict,fullname)
def MakeDiffSimSurvByAbs(survgenmethod='diff_abs', testname='test_origin'):
    surveypaper = GetSuveryChapterSent()
    chapter_list =surveypaper['chapter_list']
    print('----------TestLoadAllChapterModelDoc')
    for t in surveypaper['chapter_title']:
        print(t)
    print(surveypaper.keys())
    doc_model_sent_list = []
    doc_model_sent_dict={}
    chapter_gensurv_dict={}
    for chapter_dict in chapter_list:
        doc_dict = {}

        doc_dict['model'] = [chapter_dict['sent']]
        doc_dict['title'] = chapter_dict['title']
        doc_dict['fid'] = chapter_dict['fid']
        print('--------chapter:')
        print(doc_dict['title'], doc_dict['fid'])
        cht=re.split('\-t',doc_dict['title'])
        if len(cht)>=2:
            chid = cht[0]
            chtitle = cht[1]
        else:
            chid = doc_dict['title']
            chtitle = doc_dict['title']
        doc_dict['chid']=chid
        doc_dict['chtitle']=chtitle

        doc_model_sent_list.append(doc_dict)
        doc_model_sent_dict[chid]=doc_dict
        for each in doc_dict['model']:
            print(each)
        print(doc_dict.keys())
        chapter_doc_dict=LoadChpaterOrig(chid)
        surv_sent = []
        abstract_list=[]
        for refid,(refname, abstract) in chapter_doc_dict['originrefpaper_abstract'].items():
            if len(abstract)==0:
                continue
            doc =[]
            for s in abstract:
                doc.append(s[1])
            abstract_list.append([refname,doc])
        diffsentdoc,simsentdoc = sxpRemoveDup.RankSelTopByDiffImp(abstract_list)

        if survgenmethod == 'diff_abs':
            useddoc = diffsentdoc
        if survgenmethod == 'sim_abs':
            useddoc = simsentdoc
        for eachdoc in useddoc:
            for s in eachdoc:
                surv_sent.append(s)
        print('abstract as survy', surv_sent)
        chapter_gensurv_dict[doc_dict['fid']] = surv_sent
    #fname = testname + '_' + survgenmethod + 'chapter_gensurv_dict.dict'
    fname = testname + '_' + survgenmethod + 'chapter_gensurv_dict.dict'
    fullname = os.path.join(graph_dir, fname)
    sxpReadFileMan.SaveObject(chapter_gensurv_dict,fullname)
def LoadDocGenSurveByChiID(chid,survgenmethod='abstract',testname='wordquery_allv6'):
    fname = 'chapter_doc_dict_'+chid + '_'+testname + '_'+survgenmethod + '.dict'
    fullname = os.path.join(pkdir,fname)
    chapter_doc_dict = sxpReadFileMan.LoadObject(fullname)
    return chapter_doc_dict

def LoadGenSurveyByChid(chid,survgenmethod='abstract',testname='wordquery_allv6'):
    # print('----------chapter_refid_dict----------')
    # for ch,chapter_content_dict in chapter_refid_dict.items():
    #     print(ch,chapter_content_dict['ref_idlist'],chapter_content_dict['fulltxt_fid'])
    survey_chid_id_dict= GetSurveyChapterID()

    chapter_fid_dict = survey_chid_id_dict['chid_id_dict']
    if chid in chapter_fid_dict.keys():
        chapter_content_dict = chapter_fid_dict[chid]
        fid = chapter_content_dict['fid']
    else:
        fid = None
    if fid:
        return LoadGenSurvey(fid,survgenmethod,testname)
    return None

def LoadGenSurvey(fid,survgenmethod='abstract',testname='wordquery_allv6'):
    fname = testname+'_'+ survgenmethod + 'chapter_gensurv_dict.dict'
    fullname = os.path.join(graph_dir,fname)
    chapter_gensurv_dict = sxpReadFileMan.LoadSxptext(fullname)
    if fid not in list(chapter_gensurv_dict.keys()):
        return None
    return chapter_gensurv_dict[fid]
def LoadChapterOriginRefAbs(fid, survgenmethod='origin_abs', testname='test_origin'):
    fname = testname+'_'+ survgenmethod + 'chapter_gensurv_dict.dict'
    fullname = os.path.join(graph_dir,fname)
    chapter_gensurv_dict = sxpReadFileMan.LoadObject(fullname)
    if fid not in list(chapter_gensurv_dict.keys()):
        return None
    return chapter_gensurv_dict[fid]
def topkkword(survgenmethod):
    pt = 'topk(\d+)'
    g= re.match(pt,survgenmethod)
    if g:
        wordtopnum = int(g.groups()[0])
        return wordtopnum
    else:
        return None

def MakeChapterSurveyFromTopk(topk,chapter_dict,testname,survgenmethod):
    modelchapter=chapter_dict['sent']
    src = ".".join(modelchapter)
    model_wordnum = len(src)
    model_sentlen = len(modelchapter)
    chtitle = chapter_dict['title']
    # testinfo['chname']=chname
    # testinfo['title'] = ch_title
    # testinfo['truth'] = fulltxt_fid_list
    # testinfo['result']= result
    # testinfo['rankresult']=rankresult
    # testinfo ={'chname': '8.3', 'title': 'Asiya an evaluation toolkit\r', 'truth': [('CR6', 'Amigo et-al. 2005', '0074')], 'result': {'precision': 0.0, 'recall': 0.0, 'fscore': 0, 'jaccard': 0.0}, 'rankresult': [(59, '0059', 7.732764132345889, 'MEAD_ a platform for multidocument multilingual text summarization'), (44, '0044', 7.637370775510204, 'GraphSum: Discovering correlations among multiple terms for graph-based summarization'), (36, '0036', 7.482163455520166, 'Enhancing the Effectiveness of Clustering with Spectra Analysis'), (51, '0051', 7.480991840762236, 'Integrating importance, non-redundancy and coherence in graph-based extractive summarization'), (96, '0096', 7.434135479482766, 'Text summarization using a trainable summarizer and latent semantic analysis'), (31, '0031', 7.401016903103107, 'Document Summarization Based on Data Reconstruction'), (63, '0063', 7.389615629126119, 'Multi-document summarization based on two-level sparse representation model'), (41, '0041', 7.385117885951011, 'Fuzzy evolutionary optimization modeling and its applications to unsupervised categorization and extractive summarization'), (65, '0065', 7.366544230180594, 'Multi-document summarization exploiting frequent itemsets'), (16, '0016', 7.353331916250399, 'Automatic Detection of Opinion Bearing Words and Sentences'), (5, '0005', 7.33608024691358, 'A new sentence similarity measure and sentence based extractive technique for automatic text summarization'), (32, '0032', 7.319186179981635, 'Document summarization using conditional random fields'), (69, '0069', 7.292663262563827, 'NewsGist: A Multilingual Statistical News Summarizer'), (34, '0034', 7.279853379778249, 'Enhancing sentence-level clustering with ranking-based clustering framework for theme-based summarization'), (39, '0039', 7.265493119363532, 'FoDoSu: Multi-document summarization exploiting semantic analysis based on social Folksonomy'), (50, '0050', 7.263078512396694, 'Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis (PLSA) with sentence bases'), (106, '0106', 7.256840741583655, 'Using External Resources and Joint Learning for Bigram Weightingin ILP-Based Multi-Document Summarization'), (33, '0033', 7.250927194359985, 'Document summarization via guided sentence compression'), (73, '0073', 7.246243806276306, 'Predicting Salient Updates for Disaster Summarization'), (90, '0090', 7.244313743164474, 'Summarizing Email Conversations with Clue Words'), (110, '0110', 7.232675386444709, 'Weighted consensus multi-document summarization'), (107, '0107', 7.202208556503339, 'Using query expansion in graph-based approach for query-focused multi-document summarization'), (97, '0097', 7.160397907954664, 'TextRank_ bringing order into texts'), (42, '0042', 6.784758567810059, 'GA, MR, FFNN, PNN and GMM based models for automatic text summarization'), (14, '0014', 6.769455017301038, 'Assessing sentence scoring techniques for extractive text summarization'), (102, '0102', 6.68776397135337, 'Topic aspect-oriented summarization via group selection'), (68, '0068', 6.661811976809715, 'Multiple documents summarization based on evolutionary optimization algorithm'), (58, '0058', 6.643201410003675, 'MCMR: Maximum coverage and minimum redundant text summarization model'), (28, '0028', 6.63272679096454, 'Differential Evolution - A Simple and Efﬁcient Heuristic for Global Optimization over Continuous Spaces'), (71, '0071', 6.623505823546202, 'Opinion Mining and Sentiment Analysis'), (35, '0035', 6.6145224045968725, 'Enhancing the Effectiveness of Clustering with Spectra Analysi'), (38, '0038', 6.61011440339672, 'Fast and Robust Compressive Summarization with Dual Decomposition and Multi-Task Learning'), (7, '0007', 6.605081153161042, 'A text summarizer for Arabic'), (3, '0003', 6.56511080994898, 'A multi-document summarization system based on statistics and linguistic treatment'), (80, '0080', 6.555276920438957, 'ROUGE_ a package for automatic evaluation of summaries'), (0, '0000', 6.544226733780253, 'A complex network approach to text summarization'), (6, '0006', 6.5346093120129, 'A Survey of Text Summarization Extractive Techniques'), (2, '0002', 6.530537201953461, 'A language independent approach to multilingual text summarization'), (109, '0109', 6.522656323905023, 'WebInEssence_ a personalized web-based multidocument summarization and recommendation system'), (1, '0001', 6.501606596303195, 'A framework for multi-document abstractive summarization based on semantic role labelling'), (27, '0027', 6.499395833276237, 'Determinantal Point Processes for Machine Learning'), (104, '0104', 6.496924296982168, 'Topic Themes for Multi-Document Summarization'), (45, '0045', 6.494506640253359, 'Hybrid Algorithm for Multilingual Summarization of Hindi and Punjabi Documents'), (62, '0062', 6.4672666518155495, 'Multi-document abstractive summarization using ILP based multi-sentence compression.'), (94, '0094', 6.463662689448597, 'Syntactic Trimming of Extracted Sentences for Improving Extractive Multi-document Summarization'), (88, '0088', 6.461010179004967, 'Summarization of Multi-Document Topic Hierarchies using Submodular Mixtures'), (47, '0047', 6.456054854485141, 'Implementation and evaluation of evolutionary connectionist approaches to automated text summarization'), (66, '0066', 6.455924036281179, 'Multi-document summarization via budgeted maximization of submodular functions'), (4, '0004', 6.451603971361893, 'A neural attention model for abstractive sentence summarization'), (74, '0074', 6.4397378105390315, 'QARLA:A Framework for the Evaluation of Text Summarization Systems'), (72, '0072', 6.439102738184838, 'Opinosis: A Graph-Based Approach to Abstractive Summarization of Highly Redundant Opinions'), (21, '0021', 6.431331888019606, 'Building an Entity-Centric Stream Filtering Test Collection for TREC 2012'), (23, '0023', 6.421153630229971, 'Centroid-based summarization of multiple documents'), (64, '0064', 6.416658721229572, 'Multi-Document Summarization By Sentence Extraction'), (60, '0060', 6.405188590729969, 'Modeling Document Summarization as Multi-objective Optimization'), (43, '0043', 6.402147709840017, 'GistSumm_ a summarization tool based on a new extractive method'), (93, '0093', 6.401857638888889, 'SuPor: An Environment for AS of Texts in Brazilian Portuguese'), (67, '0067', 6.396924793849587, 'Multi-Sentence Compression: Finding Shortest Paths in Word Graphs'), (75, '0075', 6.376974482294494, 'QCS: A system for querying, clustering and summarizing documents'), (26, '0026', 6.375707205824305, 'Deriving concept hierarchies from text'), (95, '0095', 6.371048032208732, 'System Combination for Multi-document Summarization'), (85, '0085', 6.3710163392503585, 'Sentence extraction system asssembling multiple evidence'), (87, '0087', 6.362447970863684, 'Single-Document Summarization as a Tree Knapsack Problem'), (29, '0029', 6.361295776136093, 'Document clustering and text summarization'), (86, '0086', 6.360962524404375, 'Single-document and multi-document summarization techniques for email threads using sentence compression'), (56, '0056', 6.3486879561099325, 'Learning with Unlabeled Data for Text Categorization Using Bootstrapping and Feature Projection Techniques'), (99, '0099', 6.340772312129467, 'The anatomy of a large-scale hypertextual Web search engine'), (46, '0046', 6.340578803611267, 'Image collection summarization via dictionary learning for sparse representation'), (12, '0012', 6.340078125, 'Applying regression models to query-focused multi-document Summarization'), (8, '0008', 6.332982882340332, 'Abstractive Multi-Document Summarization via Phrase Selection and Merging'), (91, '0091', 6.332799286995087, 'Summarizing Emails with Conversational Cohesion and Subjectivity'), (70, '0070', 6.32318002676978, 'One Story, One Flow: Hidden Markov Story Models for Multilingual Multidocument Summarization'), (57, '0057', 6.322943286614498, 'Long story short - Global unsupervised models for keyphrase based meeting summarization'), (37, '0037', 6.320845582000113, 'Event graphs for information retrieval and multi-document summarization'), (15, '0015', 6.319254412056316, 'Automated Summarization Evaluation with Basic Elements'), (52, '0052', 6.314685547688463, 'Keyphrase Extraction for N-best Reranking in Multi-Sentence Compression'), (78, '0078', 6.314384765624999, 'Reader-aware multi-document summarization via sparse coding'), (53, '0053', 6.310630341880342, 'Large-margin learning of submodular summarization models'), (108, '0108', 6.307430844114923, 'Using Topic Themes for Multi-Document Summarization'), (17, '0017', 6.307106025819564, 'Automatic generic document summarization based on non-negative matrix factorization, Information Processing and Management'), (98, '0098', 6.290157229946054, 'TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages'), (19, '0019', 6.288075769578995, 'Biased LexRank_ Passage retrieval using random walks with question-based priors'), (11, '0011', 6.287489149305555, 'Analyzing the use of word graphs for abstractive text summarization'), (24, '0024', 6.277564482465407, 'Combining Syntax and Semantics for Automatic Extractive Single-document Summarization'), (76, '0076', 6.270711264898116, 'Ranking with Recursive Neural Networks and Its Application to Multi-document Summarization'), (100, '0100', 6.252403619568291, 'The automatic creation of literature abstracts'), (30, '0030', 6.248262524644623, 'Document concept lattice for text understanding and summarization'), (89, '0089', 6.237769371659604, 'Summarization System Evaluation Revisited: N-Gram Graphs'), (83, '0083', 6.230124457553925, 'Semantic graph reduction approach for abstractive Text Summarization'), (92, '0092', 6.2248052609866775, 'SUMMARIZING TEXT by RANKING TEXT UNITS ACCORDING to SHALLOW LINGUISTIC FEATURES'), (20, '0020', 6.219928146569073, 'Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory'), (54, '0054', 6.219269402279176, 'Learning Summary Prior Representation for Extractive Summarization'), (10, '0010', 6.217870218406767, 'An Extractive Text Summarizer Based on Significant Words'), (61, '0061', 6.18011836628512, 'Modeling Local Coherence: An Entity-based Approach'), (22, '0022', 6.169046977245687, 'Centering: A Framework for Modeling the Local Coherence of Discourse'), (84, '0084', 6.1125108131487895, 'Semantic Role Labelling with minimal resources: Experiments with French'), (49, '0049', 6.09940138626339, 'Information Extraction by an Abstractive Text Summarization for an Indian Regional Language'), (101, '0101', 6.059917355371901, 'The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries'), (48, '0048', 6.058926564875405, 'Improving the Estimation of Word Importance for News Multi-Document Summarization'), (40, '0040', 6.050426136363637, 'Framework for Abstractive Summarization using Text-to-Text Generation'), (25, '0025', 5.960007304601899, 'DEPEVAL(summ)_ dependency-based evaluation for automatic summaries'), (77, '0077', 5.7529218407596785, 'Re-evaluating Automatic Summarization with BLEU and 192 Shades of ROUGE'), (9, '0009', 5.642722117202268, 'Advances in Automatic Text Summarization'), (79, '0079', 4.744461540556365, 'Revisiting readability_ a unified framework for predicting text quality'), (82, '0082', 3.6746776323851797, 'Selecting a feature set to summarize texts in brazilian portuguese'), (55, '0055', 3.4094921514312095, 'Learning the parts of objects by non-negative matrix factorization'), (105, '0105', 3.0000438577255384, 'Unsupervised Clustering by k-medoids for Video Summarization'), (103, '0103', 2.9454761368522346, 'Topic keyword identification for text summarization using lexical clustering'), (81, '0081', 2.862244498394549, 'Scene Summarization for Online Image Collections'), (18, '0018', 2.816166428199792, 'Beyond keyword and cue-phrase matching: A sentence-based abstraction technique for information extraction'), (13, '0013', 1.8181818181818181, 'Aspects of sentence retrieval')]}

    # for (id,fid, score, title) in rankresult:
    #     predict.append(fid)
    chid = topk['chapter']
    print("topk['chapter']",topk['chapter'])
    print("topk['chapter_gensum_topknum']", topk['chapter_gensum_topknum'])
    print("topk['true_citedoc_num']", topk['true_citedoc_num'])

    print("topk['chapter_gensum_sentnum']", topk['chapter_gensum_sentnum'])
    print("topk['survey_chapter_sent_len']", topk['survey_chapter_sent_len'])

    print("topk['chapter_gensum_word_len']", topk['chapter_gensum_word_len'])
    print("topk['survey_chapter_wd_len']", topk['survey_chapter_wd_len'])
    survsent = []
    wordlen = 0
    print(('making survey for paper',chtitle))
    wordtopnum= topkkword(survgenmethod)
    if wordtopnum:
        loaddata = 'LR'
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, loaddata, chid)
        wordnum = wordtopnum
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'opt':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, survgenmethod, chid)
        wordnum = topk['chapter_gensum_word_len']
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'opt_num':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, survgenmethod, chid)
        wordnum = topk['chapter_gensum_word_len']
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'LR':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, "LR", chid)
        wordnum = topk['chapter_gensum_word_len']
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'TP':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, "LR", chid)
        wordnum = topk['chapter_gensum_word_len']
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'maxseg':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, "LR", chid)
        wordnum = topk['chapter_gensum_word_len']
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'TPLR':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, "LR", chid)
        wordnum = topk['chapter_gensum_word_len']
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'orig':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, survgenmethod, chid)
        wordnum = topk['chapter_gensum_word_len']
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent

    wordnum = model_wordnum

    for eachpaper in topk['chapter_gensum_topk']:
        if wordlen > wordnum:
            break;
        fid = eachpaper['fid']
        title = eachpaper['title']
        print((fid,title))

        refpaperlist = sxpMultiPaperData.LoadGraphMatrixSentence([fid])
        if not refpaperlist:
            return None;
        sentence_data_dict = refpaperlist[0]['sentence_data_dict']
        abstract =sentence_data_dict['abstract']
        if survgenmethod == 'abstract':
            for id,sent in abstract:
                if wordlen<wordnum:
                    survsent.append(sent)
                    wordlen = wordlen + len(sent)
        if survgenmethod == 'abstract_top2':
            survlen = 100
            sl =0
            for id, sent in abstract:
                if wordlen < wordnum:
                    survsent.append(sent)
                if sl >= survlen:
                    break
                wordlen = wordlen + len(sent)
                sl = sl +  len(sent)
        if survgenmethod == 'title_sim':
           top_sents=sxpTestWordDistQuerySurvey.LoadChapterSentenceRank(fid,chid,survgenmethod)
           for id, sent in top_sents:
               if wordlen < wordnum:
                   survsent.append(sent)
                   wordlen = wordlen + len(sent)


    return survsent
def MakeChapterSurvey(testname,chapter_dict,testinfo,survgenmethod='abstract'):
    modelchapter=chapter_dict['sent']
    src = ".".join(modelchapter)
    wordnum = len(src)
    sentlen = len(modelchapter)
    chtitle = testinfo['title']
    # testinfo['chname']=chname
    # testinfo['title'] = ch_title
    # testinfo['truth'] = fulltxt_fid_list
    # testinfo['result']= result
    # testinfo['rankresult']=rankresult
    # testinfo ={'chname': '8.3', 'title': 'Asiya an evaluation toolkit\r', 'truth': [('CR6', 'Amigo et-al. 2005', '0074')], 'result': {'precision': 0.0, 'recall': 0.0, 'fscore': 0, 'jaccard': 0.0}, 'rankresult': [(59, '0059', 7.732764132345889, 'MEAD_ a platform for multidocument multilingual text summarization'), (44, '0044', 7.637370775510204, 'GraphSum: Discovering correlations among multiple terms for graph-based summarization'), (36, '0036', 7.482163455520166, 'Enhancing the Effectiveness of Clustering with Spectra Analysis'), (51, '0051', 7.480991840762236, 'Integrating importance, non-redundancy and coherence in graph-based extractive summarization'), (96, '0096', 7.434135479482766, 'Text summarization using a trainable summarizer and latent semantic analysis'), (31, '0031', 7.401016903103107, 'Document Summarization Based on Data Reconstruction'), (63, '0063', 7.389615629126119, 'Multi-document summarization based on two-level sparse representation model'), (41, '0041', 7.385117885951011, 'Fuzzy evolutionary optimization modeling and its applications to unsupervised categorization and extractive summarization'), (65, '0065', 7.366544230180594, 'Multi-document summarization exploiting frequent itemsets'), (16, '0016', 7.353331916250399, 'Automatic Detection of Opinion Bearing Words and Sentences'), (5, '0005', 7.33608024691358, 'A new sentence similarity measure and sentence based extractive technique for automatic text summarization'), (32, '0032', 7.319186179981635, 'Document summarization using conditional random fields'), (69, '0069', 7.292663262563827, 'NewsGist: A Multilingual Statistical News Summarizer'), (34, '0034', 7.279853379778249, 'Enhancing sentence-level clustering with ranking-based clustering framework for theme-based summarization'), (39, '0039', 7.265493119363532, 'FoDoSu: Multi-document summarization exploiting semantic analysis based on social Folksonomy'), (50, '0050', 7.263078512396694, 'Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis (PLSA) with sentence bases'), (106, '0106', 7.256840741583655, 'Using External Resources and Joint Learning for Bigram Weightingin ILP-Based Multi-Document Summarization'), (33, '0033', 7.250927194359985, 'Document summarization via guided sentence compression'), (73, '0073', 7.246243806276306, 'Predicting Salient Updates for Disaster Summarization'), (90, '0090', 7.244313743164474, 'Summarizing Email Conversations with Clue Words'), (110, '0110', 7.232675386444709, 'Weighted consensus multi-document summarization'), (107, '0107', 7.202208556503339, 'Using query expansion in graph-based approach for query-focused multi-document summarization'), (97, '0097', 7.160397907954664, 'TextRank_ bringing order into texts'), (42, '0042', 6.784758567810059, 'GA, MR, FFNN, PNN and GMM based models for automatic text summarization'), (14, '0014', 6.769455017301038, 'Assessing sentence scoring techniques for extractive text summarization'), (102, '0102', 6.68776397135337, 'Topic aspect-oriented summarization via group selection'), (68, '0068', 6.661811976809715, 'Multiple documents summarization based on evolutionary optimization algorithm'), (58, '0058', 6.643201410003675, 'MCMR: Maximum coverage and minimum redundant text summarization model'), (28, '0028', 6.63272679096454, 'Differential Evolution - A Simple and Efﬁcient Heuristic for Global Optimization over Continuous Spaces'), (71, '0071', 6.623505823546202, 'Opinion Mining and Sentiment Analysis'), (35, '0035', 6.6145224045968725, 'Enhancing the Effectiveness of Clustering with Spectra Analysi'), (38, '0038', 6.61011440339672, 'Fast and Robust Compressive Summarization with Dual Decomposition and Multi-Task Learning'), (7, '0007', 6.605081153161042, 'A text summarizer for Arabic'), (3, '0003', 6.56511080994898, 'A multi-document summarization system based on statistics and linguistic treatment'), (80, '0080', 6.555276920438957, 'ROUGE_ a package for automatic evaluation of summaries'), (0, '0000', 6.544226733780253, 'A complex network approach to text summarization'), (6, '0006', 6.5346093120129, 'A Survey of Text Summarization Extractive Techniques'), (2, '0002', 6.530537201953461, 'A language independent approach to multilingual text summarization'), (109, '0109', 6.522656323905023, 'WebInEssence_ a personalized web-based multidocument summarization and recommendation system'), (1, '0001', 6.501606596303195, 'A framework for multi-document abstractive summarization based on semantic role labelling'), (27, '0027', 6.499395833276237, 'Determinantal Point Processes for Machine Learning'), (104, '0104', 6.496924296982168, 'Topic Themes for Multi-Document Summarization'), (45, '0045', 6.494506640253359, 'Hybrid Algorithm for Multilingual Summarization of Hindi and Punjabi Documents'), (62, '0062', 6.4672666518155495, 'Multi-document abstractive summarization using ILP based multi-sentence compression.'), (94, '0094', 6.463662689448597, 'Syntactic Trimming of Extracted Sentences for Improving Extractive Multi-document Summarization'), (88, '0088', 6.461010179004967, 'Summarization of Multi-Document Topic Hierarchies using Submodular Mixtures'), (47, '0047', 6.456054854485141, 'Implementation and evaluation of evolutionary connectionist approaches to automated text summarization'), (66, '0066', 6.455924036281179, 'Multi-document summarization via budgeted maximization of submodular functions'), (4, '0004', 6.451603971361893, 'A neural attention model for abstractive sentence summarization'), (74, '0074', 6.4397378105390315, 'QARLA:A Framework for the Evaluation of Text Summarization Systems'), (72, '0072', 6.439102738184838, 'Opinosis: A Graph-Based Approach to Abstractive Summarization of Highly Redundant Opinions'), (21, '0021', 6.431331888019606, 'Building an Entity-Centric Stream Filtering Test Collection for TREC 2012'), (23, '0023', 6.421153630229971, 'Centroid-based summarization of multiple documents'), (64, '0064', 6.416658721229572, 'Multi-Document Summarization By Sentence Extraction'), (60, '0060', 6.405188590729969, 'Modeling Document Summarization as Multi-objective Optimization'), (43, '0043', 6.402147709840017, 'GistSumm_ a summarization tool based on a new extractive method'), (93, '0093', 6.401857638888889, 'SuPor: An Environment for AS of Texts in Brazilian Portuguese'), (67, '0067', 6.396924793849587, 'Multi-Sentence Compression: Finding Shortest Paths in Word Graphs'), (75, '0075', 6.376974482294494, 'QCS: A system for querying, clustering and summarizing documents'), (26, '0026', 6.375707205824305, 'Deriving concept hierarchies from text'), (95, '0095', 6.371048032208732, 'System Combination for Multi-document Summarization'), (85, '0085', 6.3710163392503585, 'Sentence extraction system asssembling multiple evidence'), (87, '0087', 6.362447970863684, 'Single-Document Summarization as a Tree Knapsack Problem'), (29, '0029', 6.361295776136093, 'Document clustering and text summarization'), (86, '0086', 6.360962524404375, 'Single-document and multi-document summarization techniques for email threads using sentence compression'), (56, '0056', 6.3486879561099325, 'Learning with Unlabeled Data for Text Categorization Using Bootstrapping and Feature Projection Techniques'), (99, '0099', 6.340772312129467, 'The anatomy of a large-scale hypertextual Web search engine'), (46, '0046', 6.340578803611267, 'Image collection summarization via dictionary learning for sparse representation'), (12, '0012', 6.340078125, 'Applying regression models to query-focused multi-document Summarization'), (8, '0008', 6.332982882340332, 'Abstractive Multi-Document Summarization via Phrase Selection and Merging'), (91, '0091', 6.332799286995087, 'Summarizing Emails with Conversational Cohesion and Subjectivity'), (70, '0070', 6.32318002676978, 'One Story, One Flow: Hidden Markov Story Models for Multilingual Multidocument Summarization'), (57, '0057', 6.322943286614498, 'Long story short - Global unsupervised models for keyphrase based meeting summarization'), (37, '0037', 6.320845582000113, 'Event graphs for information retrieval and multi-document summarization'), (15, '0015', 6.319254412056316, 'Automated Summarization Evaluation with Basic Elements'), (52, '0052', 6.314685547688463, 'Keyphrase Extraction for N-best Reranking in Multi-Sentence Compression'), (78, '0078', 6.314384765624999, 'Reader-aware multi-document summarization via sparse coding'), (53, '0053', 6.310630341880342, 'Large-margin learning of submodular summarization models'), (108, '0108', 6.307430844114923, 'Using Topic Themes for Multi-Document Summarization'), (17, '0017', 6.307106025819564, 'Automatic generic document summarization based on non-negative matrix factorization, Information Processing and Management'), (98, '0098', 6.290157229946054, 'TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages'), (19, '0019', 6.288075769578995, 'Biased LexRank_ Passage retrieval using random walks with question-based priors'), (11, '0011', 6.287489149305555, 'Analyzing the use of word graphs for abstractive text summarization'), (24, '0024', 6.277564482465407, 'Combining Syntax and Semantics for Automatic Extractive Single-document Summarization'), (76, '0076', 6.270711264898116, 'Ranking with Recursive Neural Networks and Its Application to Multi-document Summarization'), (100, '0100', 6.252403619568291, 'The automatic creation of literature abstracts'), (30, '0030', 6.248262524644623, 'Document concept lattice for text understanding and summarization'), (89, '0089', 6.237769371659604, 'Summarization System Evaluation Revisited: N-Gram Graphs'), (83, '0083', 6.230124457553925, 'Semantic graph reduction approach for abstractive Text Summarization'), (92, '0092', 6.2248052609866775, 'SUMMARIZING TEXT by RANKING TEXT UNITS ACCORDING to SHALLOW LINGUISTIC FEATURES'), (20, '0020', 6.219928146569073, 'Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory'), (54, '0054', 6.219269402279176, 'Learning Summary Prior Representation for Extractive Summarization'), (10, '0010', 6.217870218406767, 'An Extractive Text Summarizer Based on Significant Words'), (61, '0061', 6.18011836628512, 'Modeling Local Coherence: An Entity-based Approach'), (22, '0022', 6.169046977245687, 'Centering: A Framework for Modeling the Local Coherence of Discourse'), (84, '0084', 6.1125108131487895, 'Semantic Role Labelling with minimal resources: Experiments with French'), (49, '0049', 6.09940138626339, 'Information Extraction by an Abstractive Text Summarization for an Indian Regional Language'), (101, '0101', 6.059917355371901, 'The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries'), (48, '0048', 6.058926564875405, 'Improving the Estimation of Word Importance for News Multi-Document Summarization'), (40, '0040', 6.050426136363637, 'Framework for Abstractive Summarization using Text-to-Text Generation'), (25, '0025', 5.960007304601899, 'DEPEVAL(summ)_ dependency-based evaluation for automatic summaries'), (77, '0077', 5.7529218407596785, 'Re-evaluating Automatic Summarization with BLEU and 192 Shades of ROUGE'), (9, '0009', 5.642722117202268, 'Advances in Automatic Text Summarization'), (79, '0079', 4.744461540556365, 'Revisiting readability_ a unified framework for predicting text quality'), (82, '0082', 3.6746776323851797, 'Selecting a feature set to summarize texts in brazilian portuguese'), (55, '0055', 3.4094921514312095, 'Learning the parts of objects by non-negative matrix factorization'), (105, '0105', 3.0000438577255384, 'Unsupervised Clustering by k-medoids for Video Summarization'), (103, '0103', 2.9454761368522346, 'Topic keyword identification for text summarization using lexical clustering'), (81, '0081', 2.862244498394549, 'Scene Summarization for Online Image Collections'), (18, '0018', 2.816166428199792, 'Beyond keyword and cue-phrase matching: A sentence-based abstraction technique for information extraction'), (13, '0013', 1.8181818181818181, 'Aspects of sentence retrieval')]}
    refnum = len(testinfo['truth'])
    # for (id,fid, score, title) in rankresult:
    #     predict.append(fid)
    chid = testinfo['chname']
    survsent = []
    wordlen = 0
    print(('making survey for paper',chtitle))
    if survgenmethod == 'opt':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, survgenmethod, chid)
        wordnum = np.inf
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'opt_num':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, survgenmethod, chid)
     #   wordnum = np.inf
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    if survgenmethod == 'LR':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, "LR", chid)
     #   wordnum = np.inf
        for sent in top_sents:
            survsent.append(sent)

        return survsent
    if survgenmethod == 'orig':
        top_sents = sxpTestWordDistQuerySurvey.LoadDualRankSent(testname, survgenmethod, chid)
        #   wordnum = np.inf
        for sent in top_sents:
            if wordlen < wordnum:
                survsent.append(sent)
                wordlen = wordlen + len(sent)
        return survsent
    for (id,fid, score, title) in testinfo['rankresult']:
        if wordlen > wordnum:
            break;
        print((fid,title))
        refpaperlist = sxpMultiPaperData.LoadGraphMatrixSentence([fid])
        if not refpaperlist:
            return None;
        sentence_data_dict = refpaperlist[0]['sentence_data_dict']
        abstract =sentence_data_dict['abstract']
        if survgenmethod == 'abstract':
            for id,sent in abstract:
                if wordlen<wordnum:
                    survsent.append(sent)
                    wordlen = wordlen + len(sent)
        if survgenmethod == 'abstract_top2':
            survlen = 100
            sl =0
            for id, sent in abstract:
                if wordlen < wordnum:
                    survsent.append(sent)
                if sl >= survlen:
                    break
                wordlen = wordlen + len(sent)
                sl = sl +  len(sent)
        if survgenmethod == 'title_sim':
           top_sents=sxpTestWordDistQuerySurvey.LoadChapterSentenceRank(fid,chid,survgenmethod)
           for id, sent in top_sents:
               if wordlen < wordnum:
                   survsent.append(sent)
                   wordlen = wordlen + len(sent)


    return survsent
def TestSent():

    fid = '0003'
    print('-----fid',fid)
    refpaperlist = sxpMultiPaperData.LoadGraphMatrixSentence([fid])
    # doc_dict['sentence_data_dict'] = sentence_data_dict
    # doc_dict['title'] = fname_dict['title']
    # doc_dict['fid'] = fname_dict['fid']
    # doc_dict['graph_dict'] = graph_dict
    # doc_dict['matrix_dict'] = matrix_dict
    # doc_model_sent_list.append(doc_dict)
    doc_dict = refpaperlist[0]
    sentence_data_dict = doc_dict['sentence_data_dict']
    print('--title',doc_dict['title'])
    abstract = sentence_data_dict['abstract']
    print('---abstract',abstract)
    for k,v in list(sentence_data_dict.items()):
        print(('-----',k,v))
    print((list(sentence_data_dict.keys())))
if __name__ == '__main__':
    main()
