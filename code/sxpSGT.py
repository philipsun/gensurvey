#-------------------------------------------------------------------------------
# Name:        sxpSGT.py
# Purpose:
#
# Author:      sunxp
#
# Created:     11/31/2019
# Copyright:   (c) sunxp 2019
# Licence:     <MIT>
#-------------------------------------------------------------------------------
#coding=UTF-8

class sxpTreeNode:
    def __init__(self,keyword,ntype='dim'):
        self.keyword=keyword
        self.nodetype=ntype
        self.dim=[]
        self.topic=[]
    def addchild(self,nd,ntype='dim'):
        if ntype=='dim':
            self.dim.append(nd)
        if ntype=='topic':
            self.topic.append(nd)
class sxpTempTree:
    def __init__(self,title):
        self.title=title
        self.root= None
    def test(self):
        print((self.title))
def GetTestTemp():
    r = sxpTempTree('test')
    n1=sxpTreeNode('summarization',ntype='dim')
    n2 = sxpTreeNode('method', ntype='dim')
    n3 = sxpTreeNode('abstractive', ntype='topic')
    n4 = sxpTreeNode('extractive', ntype='topic')
    n1.addchild(n2)
    n2.addchild(n3,'topic')
    n2.addchild(n4,'topic')
    r.root=n1
    return r
def GetTreeByName(treename):
    if treename=='test':
        return GetTestTemp1(treename)
    if treename =='extractive':
        return GetTestTemp2(treename)
    if treename == 'extractivedim':
        return GetTestTemp3(treename)
    return None
def GetTestTemp1(treename='test'):
    r = sxpTempTree(treename)
    n1=sxpTreeNode('summarization',ntype='dim')
    n2 = sxpTreeNode('method', ntype='dim')
    n3 = sxpTreeNode('abstractive', ntype='topic')
    n4 = sxpTreeNode('extractive', ntype='topic')
    n1.addchild(n2)
    n1.addchild(n3,'topic')
    n1.addchild(n4,'topic')
    r.root=n1
    return r
def GetTestTemp2(treename='extractive'):
    r = sxpTempTree(treename)
    n1=sxpTreeNode('summarization',ntype='dim')
    n2 = sxpTreeNode('method', ntype='dim')
    n3 = sxpTreeNode('extractive', ntype='dim')
    n4 = sxpTreeNode('supervised', ntype='topic')
    n5 = sxpTreeNode('unsupervised', ntype='topic')
    n1.addchild(n2)
    n2.addchild(n3,'dim')
    n3.addchild(n4,'topic')
    n3.addchild(n5,'topic')
    r.root=n1
    return r
def GetTestTemp3(treename="extractivedim"):
    r = sxpTempTree(treename)
    n1=sxpTreeNode('summarization',ntype='dim')
    n2 = sxpTreeNode('method', ntype='dim')
    n3 = sxpTreeNode('extractive', ntype='dim')
    n4 = sxpTreeNode('supervised', ntype='dim')
    n5 = sxpTreeNode('unsupervised', ntype='dim')
    n1.addchild(n2)
    n2.addchild(n3,'dim')
    n3.addchild(n4,'dim')
    n3.addchild(n5,'dim')
    r.root=n1
    return r
def main():
    pass
if __name__ == '__main__':
    main()
