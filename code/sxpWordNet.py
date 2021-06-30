# coding=UTF-8
#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      sunxp
#
# Created:     31/03/2017
# Copyright:   (c) sunxp 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from nltk.corpus import wordnet as wn
import nltk
import re
import enchant
global_d = enchant.Dict("en_US")
def Test1():
    dog= wn.synsets('dog')
    print('dog synsets: ', dog)
    dog = wn.synset('dog.n.01')
    print('dog name', dog.name())
    print('dog definition:', dog.definition())
    print('dog synsets of dog.n.01 : ',dog)
    print('dog hypernyms shangweici: ',dog.hypernyms()) #shangweici
    print('dog hyponyms more specific—the (immediate) hyponyms. 下位词: ',dog.hyponyms()) #xiaweici
    print('dog member_holonyms 成员组成的上位词，如树和森林: ',dog.member_holonyms())
    m=wn.synsets('male')
    print('male dog',m)
    for eachm in m:
        s = wn.synset(eachm.name())
        print('eachm:',eachm.name(),s.definition())
    good = wn.synset('good.a.01')
    print('good lemmas(),good.lemmas()[0]: ',good.lemmas(),good.lemmas()[0])
    print('good.lemmas()[0].antonyms(): ',good.lemmas()[0].antonyms())
    wn.synset('walk.v.01').entailments()
    notes = r'''
    meronyms: 成员
    holonyms: 整体
    part_meronyms：部分-整体关系
    member_holonyms
    '''
    print(r'good,noun的名词', wn.synsets('good',wn.NOUN))
    good_noun = wn.synsets('good',wn.NOUN)
    for eachm in good_noun:
        s = wn.synset(eachm.name())
        print('eachm:',eachm.name(),s.definition())

    print(r'good.entailments(): 蕴含 ',good.entailments())
    print(r'wn.synsets(car) 同义词集', wn.synsets('motorcar')) #找到同义词集
    print(r"wn.synset('tree.n.01').lemma_names() 同义词集的字符串", wn.synset('car.n.01').lemma_names())
    print(r"wn.synset('tree.n.01').part_meronyms() 部分整体：树-树干、树冠、树根", wn.synset('tree.n.01').part_meronyms())
    print(r"wn.synset('tree.n.01').member_holonyms() ：成员整体：树-森林", wn.synset('tree.n.01').member_holonyms())
    print(r"wn.synset('tree.n.01').part_holonyms()：成员", wn.synset('tree.n.01').part_holonyms())
    print(r"wn.synset('tree.n.01').substance_meronyms() :实质，The substance（实质） a tree is made of includes heartwood（心材） and sapwood（边材）, i.e., the substance_meronyms(). ", wn.synset('tree.n.01').substance_meronyms())
    synonyms = []
    antonyms = []

    for syn in wn.synsets("good"):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    notes = '''
    Each synset contains one or more lemmas, which represent a specific sense of a specific word.
    Note that some relations are defined by WordNet only over Lemmas:
    '''
    print(('synonyms of good',set(synonyms)))
    print(('antonyms of good',set(antonyms)))
def AddMarkSpace(txt):
    pt = r'(?P<W1>\w)(?P<MARK>[\.\,])(?P<W2>\w)'
    txt = re.sub(pt, "\g<W1>\g<MARK> \g<W2>",txt)
    return txt
def RemoveHyphenMark(txt):
    pt = r'(?P<W1>\w)(?P<MARK>[\-])(?P<W2>\w)'
    txt = re.sub(pt, "\g<W1>\g<W2>",txt)
    return txt

def IsWordNetWordComposition(word):
    word = re.sub('\s+', '', word)
    pt = '([a-zA-Z]+)'#add $ to the end of string will
    g = re.findall(pt, word)
    if not g:
        return [word]
    subword = []
    for w in g:
        ps=nltk.pos_tag([w])
        dog = wn.synsets(w)
        if dog:
            subword.append(w)
            continue
        n = len(w)

        subsub = []
        if ps[0][1] in ['NN','NNS']:
            bnotfind = True;
            for i in range(1,n):
                s1 = w[0:i]
                s2 = w[i:n]

                if IsWord(s1) and IsWord(s2):
                    subword.append(s1)
                    subword.append(s2)
                    bnotfind = False;
            if bnotfind:
                subword.append(w)
            continue
        if ps[0][1] in ['RB']:
            bnotfind = True;
            for i in range(1,n):
                s1 = w[0:i]
                s2 = w[i:n]

                if IsWord(s1) and IsWord(s2):
                    subword.append(s1)
                    subword.append(s2)
                    bnotfind = False;
            if bnotfind:
                subword.append(w)
            continue;
        subword.append(w)

    return subword
def IsCapital(word):
    pt = '[A-Z]'
    g = re.findall(pt,word)
    if len(g)>=2:
        return True
    else:
        return False
def CheckWordComposition(word):
    if IsCapital(word):
        return [word]
    word = re.sub('\s+','',word)
    pt = '([A-Za-z]+)'#add $ to the end of string will
    g = re.findall(pt, word)
  #  print(g)
    if not g:
        return [word]
    subword = []
    for w in g:
        bnotfind = True
        n = len(w)
        if IsWord(w):
            subword.append(w)
            continue

        for i in range(1, n):
            s1 = w[0:i]
            s2 = w[i:n]

            if IsWord(s1) and IsWord(s2):
                subword.append(s1)
                subword.append(s2)
                bnotfind = False;
        if bnotfind:
            subword.append(w)
    return subword
def IsWord(w):
    if len(w)==1:
        return False;
    return global_d.check(w)
def checkword(txt):
    txt = " "+txt +" "
    pt = '([\s\,\.\:\(\[](\w+)\-(\w+[\.\,\?\:\!\s\)\]]))+?'
    g= re.findall(pt,txt)
 #   print(g)
    for each in g:
        spt = each[0]
        s = each[1]+each[2]
        txt = re.sub(spt,s,txt)
    return txt
def splitbymark(txt):
    s = re.split(r'(\,|\.\s|\?|\:|\"|\'|\)|\(|\!)',txt)
    return s
def correctjsontxt(txt):
   # txt1 = AddMarkSpace(txt)
    txt2 = RemoveHyphenMark(txt)
    txt2list = splitbymark(txt2)
    pt =re.compile( r'(\,|\.\s|\?|\:|\"|\'|\)|\(|\!)')
    origins = ""
    for subtxt in txt2list:
        g=pt.match(subtxt)
        if g:
            origins = origins+ g.groups()[0]
            continue
        sw = re.split('\s+',subtxt)
        ntxt= " "
        for wd in sw:
            sw = wd.lower().strip()
            if len(sw)==0:
                continue

            wdlist = CheckWordComposition(wd);#IsWordNetWordComposition(sw)
            for w in wdlist:
                ntxt = ntxt + ' ' + w
        origins = origins + ntxt
    return origins;
def test2():
    dog = wn.synsets('added')
    print(('dog synsets: ', dog))
    txt = 'hello-word, hello-word, hello-my'
    print((RemoveHyphenMark(txt)))
    inputStr = "this is to hello crifan, nihao crifan"
    replacedStr = re.sub(r"hello (?P<name>\w+), nihao (?P=name)", "\g<name> \g<name>", inputStr);
    print(replacedStr)
    inputStr = "thistree.wer, and we have.tere but as we know,that we a.re going to make this ok"
    print((AddMarkSpace(inputStr)))
    word = '“te xt sur ﬁng”'
    print(('pos',nltk.pos_tag([word])))
    pt = '([a-zA-Z]+)'#add $ to the end of string will
    g = re.findall(pt, word)
    print(g)

    print(('IsWordNetWordComposition',IsWordNetWordComposition(word)))
    print(('CheckWordComposition',CheckWordComposition(word)))
    print(('correctjsontxt',correctjsontxt(inputStr)))
    word = 'ﬁng”'.decode('utf-8').encode('utf-8')
    pt = '([A-Za-z]+)'#add $ to the end of string will
    g = re.findall(pt, word,re.U)
    print(g)
    if g:
        print((g[0]))
    print(g)
def main():
    test2()

if __name__ == '__main__':
    main()
