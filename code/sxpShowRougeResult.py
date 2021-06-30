#-------------------------------------------------------------------------------
# Name:        sxpShowRougeResult
# Purpose:
#
# Author:      sunxp
#
# Created:     28-10-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sxpPackage
import os
import re
def GetDirFileList(filedir, suff):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
    filelist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      if os.path.isdir(os.path.join(filedir, f)):
         continue
      else:
        tf = f.split('.')
        if tf[-1] == suff:
            filelist.append(f)
    return filelist
def GetDict(strdict):
    patstr = r"\{(\w*)\}"
    pattern = re.compile(patstr)
    g = pattern.findall(strdict)
    print(g)
def GetThreeScore(scorename,rdict):
    pname = scorename + '_precision'
    rname = scorename + '_recall'
    fname = scorename + '_f_score'
    return [rdict[pname],rdict[rname],rdict[fname]]

def ShowData(pkdir, suff):

    scoretype = ['rouge_1','rouge_2','rouge_3','rouge_4','rouge_l','rouge_w_1.2','rouge_s*','rouge_su*']
    f1 = GetDirFileList(pkdir, suff)
    score_set = {}
    for eachf in f1:
        fn = pkdir + '\\'+ eachf
        d = sxpPackage.LoadSxptext(fn)

        print(d[0])
        print(d[1])
        score = d[1]
        for eachscore in scoretype:
            tscore = GetThreeScore(eachscore,score)
            print(tscore)
            if eachscore in score_set:
                score_list = score_set[eachscore]
                score_list.append([eachf,tscore])
            else:
                score_list = []
                score_list.append([eachf,tscore])
                score_set[eachscore] = score_list
    for eachscore in scoretype:
        print(eachscore)
        methodscore = score_set[eachscore]
        for eachitem in methodscore:
            print(eachitem[0],eachitem[1][0],eachitem[1][1],eachitem[1][2])
##            for eachone in eachitem[1]:
##                print eachone,
##            print '\n'
def ShowMyPyrougeData(fn):
    scoretype = ['rouge_1','rouge_2','rouge_3','rouge_4','rouge_l','rouge_w_1.2','rouge_s_u']
    score_list = sxpPackage.LoadSxptext(fn)
    score_set = {}
    i = 0
    for eachtest in score_list:
        eachf = 't'+str(i)
        i = i + 1
      #  print eachtest
        for eachscore in scoretype:
            tscore = GetThreeScore(eachscore,eachtest)
       #     print tscore
            if eachscore in score_set:
                score_list = score_set[eachscore]
                score_list.append([eachf,tscore])
            else:
                score_list = []
                score_list.append([eachf,tscore])
                score_set[eachscore] = score_list
    for eachscore in scoretype:
        print(eachscore)
        methodscore = score_set[eachscore]
        for eachitem in methodscore:
            print(eachitem[0],eachitem[1][0],eachitem[1][1],eachitem[1][2])
def TestMyRougeTest():
    ducscore = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\system_html\output_set.pk'
 #   ShowMyPyrougeData(ducscore)
    paperscore = r'D:\pythonwork\code\paperparse\paper\papers\system_html\output_set.pk'
    ShowMyPyrougeData(paperscore)

def main():
    dir= r'D:\pythonwork\code\tjrank_sentences\fgcs\data\cmydata\PAPER_NEW\PAPER_NEW'
    suff = 'pk'
    ShowData(dir,suff)

if __name__ == '__main__':
    TestMyRougeTest()
