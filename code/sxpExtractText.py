#-------------------------------------------------------------------------------
# Name:        sxpExtractText
# Purpose:
#
# Author:      sunxp
#
# Created:     16/04/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding: utf-8
import re
from nltk.tokenize import sent_tokenize
import sxpTextEncode

class sxpSentence:
    src = ''
    keylist =[]
def isabstract(st,strict=True,stricttitle='Abstract'):
    if not strict:
        return hasstr(st.lower(),['abstract'])
    if strict:
        return st == stricttitle
def isconclusion(st,strict=False,stricttitle='Conclusion'):
    if not strict:
        return hasstr(st.lower(),['conclusion','conclusions','final'])
    if strict:
        return st == stricttitle
def isreference(st):
    return hasstr(st.lower(),['reference','references'])
def isacknolwedge(st):
    return hasstr(st.lower(),['acknolwedge'])
def hasstr(stra, substr_list):
    us = sxpTextEncode.GetPrintUTFStrA(stra)
  #  sus = str(us.decode('utf-8').encode('utf-8'))
    pat = '(' + '|'.join(substr_list) + ')'

    pt = re.compile(pat)
    m = pt.findall(us)
    if len(m)>0:
        return True
    print((stra,pat,m))
    return False
#    pat='(ab|cd)'
#    pt = re.compile(pat)
#
#    s = 'abefb'
#    print(pt.findall(s))
#    s = 'efcd'
#    print(pt.findall(s))
#    s = 'dfdfdd'
#    print(pt.findall(s))
def ExtractEnglishWord(textstr):
    p = r'([A-Za-z0-9]+)([,\'\"\(\)\[\]\{\}\.\-\+\:\?\\]*)\s*'
    if isinstance(textstr, str):
        ustr = textstr.encode('utf-8')
    else:
        ustr = textstr.decode('utf-8')
    g = re.findall(p,textstr)
    return g
def ExtractEnglishWordA(textstr):
    p = r'([A-Za-z0-9\.]+)([,\'\"\(\)\[\]\{\}\-\+\:\?\\]*)\s*'
    if isinstance(textstr, str):
        ustr = textstr.encode('utf-8')
    else:
        ustr = textstr.decode('utf-8')
    g = re.findall(p,textstr)
    keylist = []
    if g is not None:
        for w in g:
            s = w[0]
            s = s.strip()
            s = s.lower()
            if len(s)==0:
                continue
            if s[-1]=='.':
                s = s[0:len(s)-1]
            if len(s) == 0:
                continue;
            if s[0] == '(':
                s = s[1:len(s)]
            if len(s) == 0:
                continue
            if s[len(s)-1] == ')':
                s = s[0:len(s)-1]
            if len(s) == 0:
                continue
            keylist.append(s)
        return keylist
    else:
        return []
def ExtractSentenceA(textstr):
#    p = r'([^,^\.^\?]+)([,\.\?])'
#    p = r'([^\:^\.^\?]+)([\:\.\?!])'
#    p = r'([^\.^\?]+)([\.\?!])'
#    p = r'([^\.^\?]+)([\.\?!])'
    p = r'\.\s+(?P<sentence>.*?)\.'
    match = re.search(p,textstr)
    sentencset = []
    if match is not None:
        ms = match.group('sentence')
        for s in ms:
            sxps = sxpSentence()
            sxps.src = s;
            sxps.keylist = []
            ws =ExtractEnglishWord(s)
            if len(ws)>0:
                for w in ws:
                    sxps.keylist.append(w[0])
##                print ws
                sentencset.append(sxps)
    return sentencset
def ExtractSentence(textstr):
    p = r'[\.\?\!][\s\n\t\r]'
    sp = re.compile(p)
    ss = sp.split(textstr)
    sentencset = []
    if ss is not None:
        for s in ss:
            sxps = sxpSentence()
            sxps.src = s;
            sxps.keylist = []
            ws =ExtractEnglishWord(s)
            if len(ws)>0:
                for w in ws:
                    sxps.keylist.append(w[0])
##                print ws
                sentencset.append(sxps)
    return sentencset
def ExtractSentenceOld(textstr):
#    p = r'([^,^\.^\?]+)([,\.\?])'
#    p = r'([^\:^\.^\?]+)([\:\.\?!])'
#    p = r'([^\.^\?]+)([\.\?!])'
    p = r'([^\.^\?][^\s][^\.^\?]*)([\.\?!][\s\n\t\r]+)'
    ss = re.findall(p,textstr)
    sentencset = []
    if ss is not None:
        for s in ss:
            sxps = sxpSentence()
            sxps.src = s[0];
            sxps.keylist = []
            ws =ExtractEnglishWord(s[0])
            if len(ws)>0:
                for w in ws:
                    sxps.keylist.append(w[0])
##                print ws
                sentencset.append(sxps)
    return sentencset
def TestExtractSentence():
    textstr = r'''
    Before describing the, i.e. algorithm, 4.5 we define some notation:
    An input morpheme lattice is a triple ⟨ns,𝒩,ℰ⟩,
    where 𝒩 is a set of nodes, ℰ is a set of (edges), and ns∈𝒩 is the  start node that begins each path through the lattice.
    Each edge e∈ℰ is a 4-tuple ⟨𝑓𝑟𝑜𝑚,𝑡𝑜,𝑙𝑒𝑥,w⟩,
    where 𝑓𝑟𝑜𝑚, 𝑡𝑜∈𝒩 are head and tail nodes, 𝑙𝑒𝑥 is a single token accepted by this edge, and w is the (potentially vector-valued) edge weight.
    Tokens are drawn from one of three non-overlapping morpho-syntactic sets: 𝑙𝑒𝑥∈𝑃𝑟𝑒𝑓𝑖𝑥∪𝑆𝑡𝑒𝑚∪𝑆𝑢𝑓𝑓𝑖𝑥, where tokens that do not require desegmentation,
    such as complete words, punctuation and numbers, are considered to be in 𝑆𝑡𝑒𝑚.
    It is also useful to consider the set of all outgoing edges for a node n.𝑜𝑢𝑡={e∈ℰ|e.𝑓𝑟𝑜𝑚=n}.
    '''
    senteceset = ExtractSentence(textstr)
    for ss in senteceset:
        print(ss.keylist)
def NLTKSentence(text):
    sent_tokenize_list = sent_tokenize(text.decode('utf-8'))
    print(sent_tokenize_list)
def PreprocessText(text):
    text = text + ' '
    text = text.replace('i.e.', 'i.e.,')
    text = text.replace('e.g.','e.g.,')
    text = text.replace('et al.','et al')
    text = text.replace('Fig.','Figure')
    text = text.replace('Figure.','Figure ')
    text = text.replace('etc.','etc')
    text = text.replace('No.','No')
    text = text.replace('no.','no')
    return text
#******This is a current latest work version
def MySentence(text):
    text = PreprocessText(text)
##    pattern = r"(?P<sentence>.*?)[.\?!]\s"
##    pattern = r"(?P<sentence>.*?)(?(sentence)[.\?!])"
##    pattern = u"(?P<sentence>.*?)(?(sentence)(?P<dot>[.\?!])(?(dot)\s))"
    pattern = "(?P<sentence>.*?)(?(sentence)((?P<dot>[\.\?!:])|(?P<cdot>[。|？！]))(?(dot)\s))"
    sentence = []
    match = re.findall(pattern, text)
    if match != None:
        for sent in match:
            sentence.append(sent[0].strip())
    return sentence
def isMark(s):
    #return s in ['.','?',',','!',')','(','=',':']
    return s in ['.','?',',','!','=',':']
def RemoveBracketContent(sentstr):
    pattern = "[\(](.+?)[\)]"
    repl = " "
    sentstr=re.sub(pattern, repl, sentstr)
    return sentstr
def RemoveBracket(sentstr):
    pattern = "[\(\)\{\}\[\]]"
    repl = " "
    sentstr=re.sub(pattern, repl, sentstr)
    return sentstr

def StripMark(sentstr):
    ns = sentstr
    n = len(sentstr)
    if n == 0:
        return ''
    if ns[0]=='(' and ns[-1]==')':
        ns = ns[1:n-1]
    p = 0
    n = len(ns)
    if n== 0:
        return ''
    for s in ns:
        if isMark(s) == True:
            p = p + 1
        else:
            break;
    ns = ns[p:n]
    n = len(ns)
    if n==0:
        return ''
    i = n-1
    while i>=0:
        if isMark(ns[i])==True:
            ns = ns[0:i]
            i = i - 1
        else:
            break
    ns = ns[0:n]
    return ns.strip()
def MySegSent(text):
    text = PreprocessText(text)
  #  pt = '(,\s|\.\s|\?\s)'
    pt = '(\:\s|!\s|\.\s|\?\s|\[|\])'
    subsent = re.split(pt,text)
    #g = re.findall(pt,s)
    segs = []
    for each in subsent:
        s = each.strip()
        if s == ',' or s =="." or s=='?':
            continue
        if len(s)<=1:
            continue
        segs.append(s + '. ')
    return segs

def MySentenceA(text):
    text = PreprocessText(text)
    text = RemoveBracket(text)
    stext = text + '.'
    sentset = MySentence(stext)
    ns = len(sentset)
    if ns == 0:
        return [text]
    newset =[]
    i = 0
    newsent = StripMark(sentset[i])
    while len(newsent)==0:
        i = i + 1
        if i>=ns:
            print('no text',text)
            break
        newsent = StripMark(sentset[i])
    i = i + 1
    while i<ns:
        s = StripMark(sentset[i])
        if len(s)==0:
            i = i + 1
            continue
        if s[0].islower()==True:
            newsent = newsent + ' ' + s
            i = i + 1
        else:
            newset.append(newsent)
            newsent = s
            i = i + 1
    newset.append(newsent)
    return newset
##    n = len(newset)
##    i = 1
##    newstr = newset[0]
##    mergset = []
##    while i < n:
##        s = newset[i]
##        if i == 71:
##            print i, s[0], s
##        if s[0].islower() == True:
##            newstr = newstr + ' ' + s
##            if i == n - 1:
##                mergset.append(newstr)
##        else:
##            mergset.append(newstr)
##            newstr = s
##            if i == n -1:
##                mergset.append(newstr)
##        i = i + 1
##    i = 0
##    for sent in mergset:
##        print i, sent
##        i = i +1
##    return mergset

def MySenteceInReuter(rawstr):
    patstr = r'[\.|\"|\'|\?|\:|\(|\)]\s+'
    pt = re.compile(patstr)
    sents = pt.split(rawstr)
    return sents
def TestExtr():
   # text = u"4.5 is muffins are good, i.e. cookies are bad, sauce is www.com.cn awesome. Veggies too. Fmooo mfasss, fdssaaaa. "
    text = '''
Yeh et al. (2005) proposed two new techniques for automatic summarization of text: Modified Corpus Based Approach (MCBA) and Latent Semantic Analysis-based TRM technique (LSA + TRM). MCBA, being a trainable summarizer depends on a score function and analyzes important features for generating summaries like Position (Pos), +ve keyword, (ve) keyword, Resemblance to the Title (R2T) and Centrality (Cen). For improving this corpus-based approach, two new ideas are utilized: (a) in order to denote the importance of various sentence positions, these sentence positions are ranked, (b) Genetic Algorithm (GA) (Russell and Norvig 1995) trains the score function for obtaining an appropriate combination of feature weights. LSA + TRM approach uses LSA (Landauer et al. 1998; Deerwester et al. 1990) to obtain a document’s semantic matrix and builds a relationship map for semantic text by employing a sentence’s semantic representation. LSA is used to extract latent structures from a document. The entire process of LSA + TRM approach shown above in Fig. 2 is divided in four phases. MCBA and LSA + TRM approach focus on summarizing single documents and produce indicative, extract based summaries.
'''
##    Before describing the, i.e. algorithm, 4.5 we define some notation:
##    An input morpheme lattice is a triple ⟨ns,𝒩,ℰ⟩,
##    where 𝒩 is a set of nodes, ℰ is a set of (edges), and ns∈𝒩 is the  start node that begins each path through the lattice.
##    Each edge e∈ℰ is a 4-tuple ⟨𝑓𝑟𝑜𝑚,𝑡𝑜,𝑙𝑒𝑥,w⟩,
##    where 𝑓𝑟𝑜𝑚, 𝑡𝑜∈𝒩 are head and tail nodes, 𝑙𝑒𝑥 is a single token accepted by this edge, and w is the (potentially vector-valued) edge weight.
##    Tokens are drawn from one of three non-overlapping morpho-syntactic sets: 𝑙𝑒𝑥∈𝑃𝑟𝑒𝑓𝑖𝑥∪𝑆𝑡𝑒𝑚∪𝑆𝑢𝑓𝑓𝑖𝑥, where tokens that do not require desegmentation,
##    such as complete words, punctuation and numbers, are considered to be in 𝑆𝑡𝑒𝑚.
##    It is also useful to consider the set of all outgoing edges for a node n.𝑜𝑢𝑡={e∈ℰ|e.𝑓𝑟𝑜𝑚=n}.
##    '''
##    text= '中国人民终于站起来了，如果没有历史就没有未来。'
    sentence = MySentenceA(text)

    for sent in sentence:
        print('----',sent)
    sentence = MySenteceInReuter(text)

    for sent in sentence:
        print(sent)

##    pattern = "(?P<sentence>.*?)\."
##    match = re.findall(pattern, text)
##    if match != None:
##        print match
##    sent_tokenize_list = sent_tokenize(text.decode('utf-8'))
##    print sent_tokenize_list
def testStripMark():
    st = '.* hel.lo.).'
    print(StripMark(st))
    n = 5
    for i in range(n):
        if i>2:
            i = i + 1

        print(i)
def testseg():
    txt = '''
    The novelty of our gist-based method, em-bedded in the so-called GistSumm (GIST SUMMarizer) system, consists of both the way gist is identified and used to produce the extract. It has long been common sense that gist should guide information selection to produce a summary or extract [1] [2] [3] [4] [5]. Deep-based approaches, e.g., those based on the rhetorical structuring of source texts, address nuclearity to select relevant information [4] [6].
    '''
    segs = MySegSent(txt)
    for each in segs:
        print(each)
def main():
    testseg()
 #    print(hasstr(u'abstract',['abstract']))
if __name__ == '__main__':
    main()
