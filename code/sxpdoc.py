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

import sxpMultiPaperData
import sxpJudgeCharacter
from sxpMultiPaperData import sxpNode

class sxpDoc:
    def __init__(self):
        self.title="test doc"
        self.idx= 0
        self.sent=[]
        self.author=[]
    def test(self):
        print((self.idx,self.title))
def GetTestDoc():
    doc1 = sxpDoc()
    doc1.title = "extractive summarization"
    doc1.idx=0
    doc1.sent=['hello this is  a survey on extractive summarization',
              'an unsupervised model is proposed in this paper']
    doc2 = sxpDoc()
    doc2.idx=1
    doc2.title = "abstractive summarization"
    doc2.sent=['hello this is  a survey on abstractive summarization',
              'an supervised model is proposed in this paper']
    paperlist =[]
    paperlist.append(doc1)
    paperlist.append(doc2)
    return paperlist



def skipsent(sent):
    if sxpJudgeCharacter.haspattern(r'\[\d+\]',sent):
        return ""
    return sxpJudgeCharacter.remsymdig(sent) #skip ref
def SelectSent(sentlist):
    newsent = []
    for sent in sentlist:
        ns= skipsent(sent)
        if len(ns) ==0:
            continue
        newsent.append(sent)
    return newsent
def GetSurveyAllRefDocs():
    paperlist=sxpMultiPaperData.LoadDocData()
    doclist=[]
    for doc_dict in paperlist:
        doc = sxpDoc()
        doc.title = doc_dict['title']
        doc.idx = doc_dict['fid']

        doc.sent=SelectSent(doc_dict['sent_list'])
        doclist.append(doc)
    return doclist
def GetRefDocByfid(fid):
    paperlist=sxpMultiPaperData.LoadDocData()

    doc = None
    for doc_dict in paperlist:
        doc = sxpDoc()
        doc.title = doc_dict['title']
        doc.idx = doc_dict['fid']

        doc.sent=SelectSent(doc_dict['sent_list'])
        if doc.idx == fid:
            break
    return doc

def TestAllPaper():
    paperlist=GetSurveyAllRefDocs()
    for each in paperlist:
        print(('doc:--------', each.title,each.idx))
def TestSingle():
    paper = GetRefDocByfid('0000')
    print((paper.title))
    for i,s in enumerate( paper.sent):
        print((i, s))
def main():
   # TestAllPaper()
   TestSingle()
if __name__ == '__main__':
    main()
