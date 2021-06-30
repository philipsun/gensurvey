#-------------------------------------------------------------------------------
# Name:        sxpProcessParaText
# Purpose:
#
# Author:      sunxp
#
# Created:     01/04/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding: utf-8
import re
import numpy as np
from scipy.sparse import csr_matrix
from collections import Counter
import sxpExtractText
class sxpKeyCount:
    keystr = ''
    keypos = []
    keycount = []

class sxpTextCount:
    keylist =[]
    keycount =[]
    sxpkeyset = []
    total_keywordsize = 0
    total_words = 0
class sxpKeyMatrix:
    keyset =[]
    voc =[]
    kk_matrix_sparse = None

def ExtractKeyCount(textstr):
    keyset = sxpExtractText.ExtractEnglishWord(textstr)
    sxptextcount = sxpTextCount()
    keylist = []
    for k in keyset:
        keylist.append(k[0])
    for k in keylist:
        if k in sxptextcount.keylist:
            continue;
        keysxp = sxpKeyCount()
        keysxp.keystr = k
        keysxp.keycount = keylist.count(keysxp.keystr)
        keysxp.keypos = find_all_index(keylist,keysxp.keystr)
        sxptextcount.keylist.append(keysxp.keystr)
        sxptextcount.sxpkeyset.append(keysxp)
    sxptextcount.total_words = len(keylist)
    sxptextcount.total_keywordsize = len(sxptextcount.keylist)
    sxptextcount.keycount = Counter(sxptextcount.keylist)

    return sxptextcount

def ExtractWordAdjcentMatrix(textstr):
    keyset = sxpExtractText.ExtractEnglishWord(textstr)
    sxpkm = sxpKeyMatrix()
    keylist = []
    for k in keyset:
        keylist.append(k[0])
    n = len(keylist)
    voc = []
    nv= 0
    edge = []
    e1 = []
    e2 = []
    data = []
    for i in range(n-1):
        k1 = keylist[i]
        if k1 in voc:
            ik1 = voc.index(k1)
        else:
            voc.append(k1)
            ik1 = nv
            nv = nv + 1

        k2 = keylist[i+1]
        if k2 in voc:
            ik2 = voc.index(k2)
        else:
            voc.append(k2)
            ik2 = nv
            nv= nv + 1
        #e = [ik1,ik2]
        e1.append(ik1)
        e2.append(ik2)
        data.append(1)
        e1.append(ik2)
        e2.append(ik1)
        data.append(1)
    kk = csr_matrix((data,(e1,e2)),shape =(nv,nv))
    sxpkm.keyset = keyset;
    sxpkm.voc = voc
    sxpkm.kk_matrix_sparse = kk
    return sxpkm

def find_all_index(arr,item):
    return [i for i,a in enumerate(arr) if a==item]
def GetDocKeyCount(docset):
    return len(docset)
def PrintKeyset(sxpkeyset):
    for sxpkey in sxpkeyset:
        print(sxpkey.keystr, sxpkey.keycount)
def TestCounter():
    a = ['a', 'b','a']
    print(a.count('a'))
    kt = Counter(a)
    print(kt)
    print(find_all_index(a,'a'))
def TestParseCount():
    textstr = r'''
    Before describing the algorithm, we define some notation:
    An input morpheme lattice is a triple ⟨ns,𝒩,ℰ⟩,
    where 𝒩 is a set of nodes, ℰ is a set of (edges), and ns∈𝒩 is the start node that begins each path through the lattice.
    Each edge e∈ℰ is a 4-tuple ⟨𝑓𝑟𝑜𝑚,𝑡𝑜,𝑙𝑒𝑥,w⟩,
    where 𝑓𝑟𝑜𝑚, 𝑡𝑜∈𝒩 are head and tail nodes, 𝑙𝑒𝑥 is a single token accepted by this edge, and w is the (potentially vector-valued) edge weight.
    Tokens are drawn from one of three non-overlapping morpho-syntactic sets: 𝑙𝑒𝑥∈𝑃𝑟𝑒𝑓𝑖𝑥∪𝑆𝑡𝑒𝑚∪𝑆𝑢𝑓𝑓𝑖𝑥, where tokens that do not require desegmentation,
    such as complete words, punctuation and numbers, are considered to be in 𝑆𝑡𝑒𝑚.
    It is also useful to consider the set of all outgoing edges for a node n.𝑜𝑢𝑡={e∈ℰ|e.𝑓𝑟𝑜𝑚=n}.
    '''
    sxptxt = ExtractKeyCount(textstr)
    print(sxptxt.keycount)
    print(sxptxt.keylist)
    PrintKeyset(sxptxt.sxpkeyset)

    sp = ExtractWordAdjcentMatrix(textstr)
    print(sp.voc)
    print(sp.kk_matrix_sparse)

def TestKeywordMatrix():
    textstr = r'''
    Before describing the algorithm, we define some notation:
    An input morpheme lattice is a triple ⟨ns,𝒩,ℰ⟩,
    where 𝒩 is a set of nodes, ℰ is a set of (edges), and ns∈𝒩 is the start node that begins each path through the lattice.
    Each edge e∈ℰ is a 4-tuple ⟨𝑓𝑟𝑜𝑚,𝑡𝑜,𝑙𝑒𝑥,w⟩,
    where 𝑓𝑟𝑜𝑚, 𝑡𝑜∈𝒩 are head and tail nodes, 𝑙𝑒𝑥 is a single token accepted by this edge, and w is the (potentially vector-valued) edge weight.
    Tokens are drawn from one of three non-overlapping morpho-syntactic sets: 𝑙𝑒𝑥∈𝑃𝑟𝑒𝑓𝑖𝑥∪𝑆𝑡𝑒𝑚∪𝑆𝑢𝑓𝑓𝑖𝑥, where tokens that do not require desegmentation,
    such as complete words, punctuation and numbers, are considered to be in 𝑆𝑡𝑒𝑚.
    It is also useful to consider the set of all outgoing edges for a node n.𝑜𝑢𝑡={e∈ℰ|e.𝑓𝑟𝑜𝑚=n}.
    '''
    sp = ExtractWordAdjcentMatrix(textstr)
    print(sp.voc)
    print(sp.kk_matrix_sparse)
def main():
    #TestParseCount()
    TestKeywordMatrix()
    pass



if __name__ == '__main__':
    main()
