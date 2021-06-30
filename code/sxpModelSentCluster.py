#coding=UTF-8
#-------------------------------------------------------------------------------
# Name:        sxpDataDucMultSum.py
# Purpose:
#
# Author:      sunxp
#
# Created:     23/10/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sxpReadFileMan


import sxpFenciMakeTFIDF
import sxpJudgeCharacter

from scipy.sparse import csr_matrix
from scipy import *
import sxpDataDucMultSum
import sxpClusterModels
import numpy as np

graph_dir = sxpDataDucMultSum.graph_dir


def Test():
    cmd = "TestSentCluster"
    if cmd == 'TestSentCluster':
        TestSentCluster()
    if cmd == "BuildSubSentences":
        doc_sent_dict= sxpDataDucMultSum.LoadDocAllSent()
        BuildSubSentences(doc_sent_dict)
    if cmd =='MakeSentList':
        MakeSentList()

def BuildSubSentences(doc_sent_dict):
    doc_sent={}
    sxp_dict={}
    for docid,sentlist in list(doc_sent_dict.items()):
        sv = []
        txtv =[]
        for (i,k,id,sent) in sentlist:
            subsents = sxpJudgeCharacter.SplitSubSent(sent)
            for j,ss in enumerate( subsents):
                sv.append([docid,i,k,j,ss])
                txtv.append(ss)
                print((docid,i,k,j,ss))
        doc_sent[docid]=sv
        sxptxt = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(txtv)
        sxp_dict[docid]=sxptxt
    return doc_sent,sxp_dict

def MakeSentList():
    #here model_raw_src_dict_fname is for each dir, there are several raw texts for this docid
    model_raw_src_dict_fname= graph_dir +'/'+'model_raw_src_dict.dict'
    model_raw_src_dict=sxpReadFileMan.LoadObject(model_raw_src_dict_fname)
    doc_sent_dict ={}
    all_sent_list=[]
    all_sent_txt=[]
    for docid, doc_raw_list in list(model_raw_src_dict.items()):
        print((docid, len(doc_raw_list)))
        doc_sent_list = []
        for i, rawdict in enumerate( doc_raw_list):
            sxptxt= rawdict['sxptxt']
            for k,eachsent in enumerate( sxptxt.sentence_textset):
                doc_sent_list.append((i,k,rawdict['file_name'],eachsent))
                all_sent_list.append((i,k,rawdict['file_name'],eachsent))
                all_sent_txt.append(eachsent)
        doc_sent_dict[docid]=doc_sent_list
    doc_all_doc_sent_list_name= graph_dir +'/'+'doc_all_doc_sent_list.dict'
    sxpReadFileMan.SaveObject(doc_sent_dict,doc_all_doc_sent_list_name)
    doc_sub_sent,doc_sub_sxptxt = BuildSubSentences(doc_sent_dict)
    all_sent_sxptxt=sxpFenciMakeTFIDF.MakeTFIDFForCorpus(all_sent_txt)

    fname = graph_dir +'/'+'doc_all_doc_sub_sent.dict'
    sxpReadFileMan.SaveObject(doc_sub_sent,fname)
    fname = graph_dir +'/'+'doc_all_doc_sub_sxptxt.dict'
    sxpReadFileMan.SaveObject(doc_sub_sxptxt,fname)
    fname = graph_dir + '/' + 'all_sent_sxptxt.dict'
    sxpReadFileMan.SaveObject(all_sent_sxptxt,fname)

def TestSubSentCluster():
    fname = graph_dir +'/'+'doc_all_doc_sub_sent.dict'
    doc_sub_sent=sxpReadFileMan.LoadObject(fname)
    fname = graph_dir +'/'+'doc_all_doc_sub_sxptxt.dict'
    doc_sub_sxptxt=sxpReadFileMan.LoadObject(fname)

    docid,doc_sent_list = list(doc_sub_sent.items())[0]
    print((docid,doc_sent_list))
    sxptxt=doc_sub_sxptxt[docid]
    print((sxptxt.word))
def TestSentCluster():
    fname= graph_dir +'/'+'doc_all_doc_sent_list.dict'
    doc_sent_dict=sxpReadFileMan.LoadObject(fname)
    docid,doc_sent_list = list(doc_sent_dict.items())[0]
    print((docid,doc_sent_list))
    #doc_sent_list.append((i, k, rawdict['file_name'], eachsent))
    st = GetDocSentList(doc_sent_list)
    nc =2
    #kmeans, SpectralClustering,can be candidate
    # clustering_algorithms ={}
    # clustering_algorithms['MiniBatchKMeans']=two_means
    # clustering_algorithms['AffinityPropagation']=affinity_propagation
    # clustering_algorithms['MeanShift']=ms
    # clustering_algorithms['SpectralClustering']=spectral
    # clustering_algorithms['Ward']=ward
    # clustering_algorithms['AgglomerativeClustering']=average_linkage
    # clustering_algorithms['DBSCAN']=dbscan
    # clustering_algorithms['Birch'] = birch
    # clustering_algorithms['GaussianMixture']=gmm
    #clustering_algorithms['sxpkmeans'] = sxpkmeans
    y = ClusterSentenceList(st,nc,mode='tfidf',algorithm="sxpkmeans")
    print((len(y)))
    OutputClusterSentence(y,st,nc)
def GetDocSentList(doc_sent_list):
    st=[]
    for (i, k, fid, eachsent) in doc_sent_list:
        st.append(eachsent)
    return st
def ClusterSentenceList(sentence_list,nc=2,mode='tfidf',algorithm="MiniBatchKMeans"):
    txt_ft=ComputeTFIDF(sentence_list,mode)
    print((type(txt_ft),txt_ft.shape))
    x = txt_ft.toarray()
    print((type(x), x.shape))
    y = sxpClusterModels.clusterby(x,nc,algorithm)
    print((y.shape))
    print(y)
    return y.tolist()
def OutputClusterSentence(y,sentences,n_clusters):
    for i in range(n_clusters):
        print(('cluster:',i,'---------'))
        for j,s in enumerate(sentences):
            if y[j]==i:
                print(('---',i,j,s))
def ComputeTFIDF(sv,mode='tfidf'):
    sxptfidf=sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sv)
    if mode=='tfidf':
        return sxptfidf.tfidf
    if mode=='count':
        return sxptfidf.ct
    if mode == 'word':
        return sxptfidf.word


def ComputeJaccardMatrix(sv):
    n = len(sv)
    print(n)
    mt = csr_matrix((n, n), dtype=float64)
    for i in range(n):
        for j in range(i,n):
            mt[i,j]=   sxpJudgeCharacter.jaccard_similarity(sv[i][4],sv[j][4])
            mt[j,i]= mt[i,j]
    return mt

if __name__ == '__main__':
    Test()
