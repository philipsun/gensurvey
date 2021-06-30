#-------------------------------------------------------------------------------
# Name:        sxpCh4Ranking.py
# Purpose:
#
# Author:      sunxp
#
# Created:     09/01/2019
# Copyright:   (c) sunxp 2019
# Licence:     <MIT>
#-------------------------------------------------------------------------------
#coding=UTF-8

import numpy as np
import sxpReadFileMan
from sxpSurveyData import sxpNode
import sxpSurveyData
import sxpMultiPaperData
import os
import sxpSGTree
basedir = os.path.abspath(os.path.dirname(__file__))
#this is to replace the host url

fdir = './test/survey/papers_json'
pkdir = r'./test/survey/papers_pk'
graph_dir =   './test/survey/papers_graph'
data_dir =r'./test/survey'

def ProduceRanomRank():

    ch4_sentence_data_dict=sxpSurveyData.LoadChapter4AllSentTitleSent() #this is only sentences of the survey paper
    lenallch4sent = len(ch4_sentence_data_dict['allch4sent'])
    lenallch4title =len(ch4_sentence_data_dict['allch4title'])
    print(('len of chapter 4',lenallch4sent,lenallch4title))
    paper_dict_list = sxpMultiPaperData.LoadGraphMatrixSentence()
    allpapersent=[]
    allpapertitle = []
    headtop_sent =[]
    headtop = 4
    for doc_dict in paper_dict_list:
        title = doc_dict['title']
        allpapertitle.append(title)
        sentence_data_dict = doc_dict['sentence_data_dict']
        sentlist=sentence_data_dict['sent_list']
        i = 0
        for sent in sentlist:
            if len(sent.lower().strip())<30:
                continue
            allpapersent.append(sent)
            if i < headtop:
                headtop_sent.append(sent)
            i = i + 1
      #  p_abstract = p_sentence_data_dict['abstract']
      #  allsent.extend(p_abstract)
      #  allch4sent = ch4_sentence_data_dict['allch4sent']
    n = len(allpapersent)
    print(('sent num of all paper',n))
    rd = np.random.choice(n,lenallch4sent)
    selected=[]
    for i in rd:
        selected.append(allpapersent[i])
    sentence_data_dict = {}
    sentence_data_dict['abstract']=sxpSurveyData.GetAbs()
    sentence_data_dict['conclusion'] = sxpSurveyData.GetCon()
    sentence_data_dict['abscon'] = sxpSurveyData.GetAbsCon()
    sentence_data_dict['randomfromall']=selected
    sentence_data_dict['allch4sent']=ch4_sentence_data_dict['allch4sent']
    sentence_data_dict['allch4title']=ch4_sentence_data_dict['allch4title']
    sentence_data_dict['head2'] = headtop_sent
    fname = graph_dir + r'/sentence_data_dict_random.dict.pk'
    sxpReadFileMan.SaveObject(sentence_data_dict,fname)
    return sentence_data_dict
def LoadRandomRankSent():
    fname = graph_dir + r'/sentence_data_dict_random.dict.pk'
    sentence_data_dict= sxpReadFileMan.LoadObject(fname)
    return sentence_data_dict
def Test():
    sent_dict = LoadRandomRankSent()
    randomfromall = sent_dict['randomfromall']
    print((list(sent_dict.keys())))
    print('print randomfromall')
    for i,s in enumerate(randomfromall):
     #   print(s)
        print(s)
    print('print allch4sent')
    sentlist = sent_dict['allch4sent']
    print('print allch4title')
    for i, s in enumerate(sentlist):
        #   print(s)
        print(s)
    sentlist = sent_dict['allch4title']
    print('print allch4title')
    for i, s in enumerate(sentlist):
        #   print(s)
        print(s)
    print('print sgt')
    sentlist,paperidx_dict = sxpSGTree.LoadTreeSurvey('sgt')

    for i, s in enumerate(sentlist):
        #   print(s)
        print(s)
def main():
    ProduceRanomRank()
    Test()

if __name__ == '__main__':
    main()
