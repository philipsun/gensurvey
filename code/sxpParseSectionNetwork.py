#-------------------------------------------------------------------------------
# Name:        sxpParseSectionNetwork
# Purpose:
#
# Author:      sunxp
#
# Created:     16-11-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from sxpPackage import *
import sxpReadFileMan
import numpy as np
from scipy.sparse import csr_matrix
from scipy import *
def ParseSectionNetworkSinglePaper(sxptxt):
    cs = len(sxptxt.section_id_dict)
    cs1 = len(sxptxt.section_list)
    print(cs,cs1)
    c_c = csr_matrix(np.zeros((cs,cs), dtype=np.float))
##    for sxpsec1 in sxptxt.section_list:
##        print sxpsec1.id,sxpsec1.id_set

    for sxpsec1 in sxptxt.section_list:
        int_id1 = sxpsec1.id
        if len(sxpsec1.id_set) == 0:
            continue
        for sxpsec2 in sxptxt.section_list:
            int_id2 = sxpsec2.id
            if len(sxpsec2.id_set[1]) == 0 and int_id1 == 0:
                c_c[0,int_id2] = 1# the last section is an unknown section with no title and section id
##                print 1
##                print int_id2, 'unknown'
##                print int_id1, sxpsec2.id_set
                continue
            if int_id2 == int_id1:
                continue
            sec_id1 =[]
            sec1 = sxpsec1.id_set
            sec2 = sxpsec2.id_set
            for eachid in sec1:
                if len(eachid)>0:
                    sec_id1.append(eachid)
            sec_id2 = []
            for eachid in sec2:
                if len(eachid)>0:
                    sec_id2.append(eachid)

            prefix_len = CompareTwoIDsSinglePaper(sec_id1,sec_id2)
            if prefix_len == len(sec_id1) and len(sec_id2)==len(sec_id1) + 1:
                c_c[int_id2,int_id1] = 1
            else:
                if prefix_len == len(sec_id1) and len(sec_id2)==len(sec_id1):
                  c_c[int_id2,int_id1] = 1
##            if c_c[int_id2,int_id1] > 0:
##                print 1
##                print int_id2, sxpsec1.id_set
##                print int_id1, sxpsec2.id_set
    c_c = c_c + c_c.T
    return c_c
def ParseSectionNetwork(sxptxt):
    cs = len(sxptxt.section_id_dict)
    c_c = csr_matrix(np.zeros((cs,cs), dtype=np.float))
##    for sxpsec1 in sxptxt.section_list:
##        print sxpsec1.id,sxpsec1.id_set

    for sxpsec1 in sxptxt.section_list:
        int_id1 = sxpsec1.id
        if len(sxpsec1.id_set) == 0:
            continue
        for sxpsec2 in sxptxt.section_list:
            int_id2 = sxpsec2.id
            if len(sxpsec2.id_set) == 0 and int_id1 == 0:
                c_c[0,int_id2] = 1# the last section is an unknown section with no title and section id
##                print 1
##                print int_id2, 'unknown'
##                print int_id1, sxpsec2.id_set
                continue
            if int_id2 == int_id1:
                continue
            prefix_len = CompareTwoIDs(sxpsec1.id_set,sxpsec2.id_set)
            if prefix_len == len(sxpsec1.id_set) and len(sxpsec2.id_set)==len(sxpsec1.id_set) + 1:
                c_c[int_id2,int_id1] = 1
            else:
                if prefix_len == len(sxpsec1.id_set) and len(sxpsec2.id_set)==len(sxpsec1.id_set):
                  c_c[int_id2,int_id1] = 1
##            if c_c[int_id2,int_id1] > 0:
##                print 1
##                print int_id2, sxpsec1.id_set
##                print int_id1, sxpsec2.id_set
    c_c = c_c + c_c.T
    return c_c
def ComputePrefixSingle(sec_id1, sec_id2):
    n1=len(sec_id1)
    n2 = len(sec_id2)
    cl = 0
    if n2 >= n1:
        cl = 0
        for i in range(n1):
            s1 = sec_id1[i]
            s2 = sec_id2[i]
            if s1==s2:
                cl = cl + 1
            else:
                break
    if n2 < n1:
        cl = 0
        for i in range(n2):
            s1 = sec_id1[i]
            s2 = sec_id2[i]
            if s1==s2:
                cl = cl + 1
            else:
                break
    return cl

def ComputePrefix(sec_id1, sec_id2):
    n1=len(sec_id1)
    n2 = len(sec_id2)
    cl = 0
    if n2 >= n1:
        cl = 0
        for i in range(n1):
            s1 = sec_id1[i]
            s2 = sec_id2[i]
            if s1[0]==s2[0] and s1[1] == s2[1]:
                cl = cl + 1
            else:
                break
    if n2 < n1:
        cl = 0
        for i in range(n2):
            s1 = sec_id1[i]
            s2 = sec_id2[i]
            if s1[0]==s2[0] and s1[1] == s2[1]:
                cl = cl + 1
            else:
                break
    return cl

def CompareTwoIDsSinglePaper(sec1,sec2):
    sec_id1 =[]
    for eachid in sec1:
        if eachid is not empty:
            sec_id1.append(eachid)
    sec_id2 = []
    for eachid in sec2:
        if eachid is not empty:
            sec_id2.append(eachid)

    n1=len(sec_id1)
    n2 = len(sec_id2)
    if sec_id1[0]=='0':
        return 0 #means no coverage and no direct child relation because it is the abstract section
    else:
        if n2<n1:
            return 0
        else:
            if n2 == n1:
                if sec_id1[0] == 'top':
                    return 1 #means that the top section belongs to the root of the document, which is section 0
                else:
                    return 0 #means that two sections are both top, so they do not belong to each other
            else:
                dist = ComputePrefixSingle(sec_id1, sec_id2)
                return dist

def CompareTwoIDs(sec_id1,sec_id2):
    n1=len(sec_id1)
    n2 = len(sec_id2)
    if sec_id1[0][0]=='abstract':
        return 0 #means no coverage and no direct child relation because it is the abstract section
    else:
        if n2<n1:
            return 0
        else:
            if n2 == n1:
                if sec_id1[0][0] == 'top':
                    return 1 #means that the top section belongs to the root of the document, which is section 0
                else:
                    return 0 #means that two sections are both top, so they do not belong to each other
            else:
                dist = ComputePrefix(sec_id1, sec_id2)
                return dist

def TestSection():
    path = r'D:\pythonwork\code\paperparse\paper'
    paper_path = path + '\\papers\\'
    pickle_dir = path + '\\papers\\\pickle\\'
    #get the original filename list in the path variable
    file_list = sxpReadFileMan.GetDirFileList(paper_path)
    i = 0
    for file_name in file_list:
        if sxpReadFileMan.IsType(file_name,'xhtml') == False:
            continue
        print(i, file_name)
        pickle_path = pickle_dir + file_name + '_3.pickle'
        sxptxt = sxpReadFileMan.LoadSxptext(pickle_path)
        print(sxptxt.d_c.shape)
        print(sxptxt.c_p.shape)
        ParseSectionNetwork(sxptxt)
        i = i + 1
def ListSection():
    path = r'D:\pythonwork\code\paperparse\paper'
    paper_path = path + '\\papers\\'
    pickle_dir = path + '\\papers\\\pickle\\'
    #get the original filename list in the path variable
    file_list = sxpReadFileMan.GetDirFileList(paper_path)
    i = 0
    for file_name in file_list:
        if sxpReadFileMan.IsType(file_name,'xhtml') == False:
            continue
        print(i, file_name)
        pickle_path = pickle_dir + file_name + '_2.pickle'
        sxptxt = sxpReadFileMan.LoadSxptext(pickle_path)
        print(sxptxt.d_c.shape)
        print(sxptxt.c_p.shape)
        print(sxptxt.c_c.shape)
        for eachsec in sxptxt.section_list:
            print(eachsec.id, eachsec.id_set, eachsec.id_str)

        i = i + 1
def TestSinglePaperSection():
    pkpath = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_2.txt.pk'
    sxptxt = sxpReadFileMan.LoadSxptext(pkpath)

##    fname = r'testdimension_2.txt'
##    sxptxt = ProcessSectionPara(fname)

   # sxptxt.c_c = sxpParseSectionNetwork.ParseSectionNetwork(sxptxt)
    for eachsect in sxptxt.section_list:
        print(eachsect.title,eachsect.id,eachsect.id_str,eachsect.id_set)

    c_c = ParseSectionNetworkSinglePaper(sxptxt)
    StoreSxptext(sxptxt, pkpath)
    sxptxt = LoadSxptext(pkpath)
    n = c_c.shape[0]
    for i in range(n):
        for j in range(n):
            if c_c[i,j]>0.0:
                print(c_c[i,j])
                print(sxptxt.section_list[i].title,sxptxt.section_list[i].id_str)
                print(sxptxt.section_list[j].title,sxptxt.section_list[j].id_str)
def main():
    #TestSection()
   # ListSection()
    TestSinglePaperSection()
if __name__ == '__main__':
    main()
