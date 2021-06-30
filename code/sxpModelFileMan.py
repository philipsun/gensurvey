#-------------------------------------------------------------------------------
# Name:        sxpModelFileMan.py
# Purpose:
#
# Author:      sunxp
#
# Created:     22/11/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=UTF-8
import sxpMultiPaperData
import sxpSurveyData

def LoadDemo():
    doc_model_sent_file_list = [
                                {'model':[
                                [(1,'doc1 another top1 sent'),(2,'doc1 another top2 hello world')],
                                [(1,'doc1 top1 sent'),(2,'doc1 top2 sent')]],
                                'title':'p1'
                                },  #doc, two model, each has two sentences
                                {'model':[[(1,'doc2  top1 sent'),(2,'doc2 top2 hello world')],
                                 [(1,'doc2 another top1 sent'),(2,'doc2 another top2 hello world')]],
                                'title':'p2'
                                }
                                ]
    return doc_model_sent_file_list
def LoadMultiPaperModel():
    return sxpMultiPaperData.LoadDocModelSentence()
def LoadSurveryPaperModel():
    return sxpSurveyData.LoadDocModelSentence()

def main():
    print((LoadDemo()))

if __name__ == '__main__':
    main()
