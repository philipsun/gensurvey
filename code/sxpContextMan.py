#-------------------------------------------------------------------------------
# Name:        sxpContext
# Purpose:
#
# Author:      sunxp
#
# Created:     26/10/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import nltk
import numpy as np
def Similarity(sentence, s):
    #if sentence is a tf-idf vector, then use cosine similarity
    #if sentence is a string, use jaccard similarity
    if re.match('.+', s):
        return jaccard_similarity(sentence, s)
    else:
        return cosine_similarity(sentence, s)


def jaccard_similarity(sentence, s):
    stopwords = open('stopwords.txt','r').readlines()
    word_list1 = []
    word_list2 = []
    for word in nltk.word_tokenize(sentence):
        if word not in stopwords:
            word_list1.append(word)
    for word in nltk.word_tokenize(s):
        if word not in stopwords:
            word_list2.append(word)
##    print word_list2
##    print word_list1
    s1 = set(word_list2).intersection(set(word_list1))
    s2 = set(word_list2).union(set(word_list1))
##    print s1
##    print s2
    return float(len(s1))/float(len(s2))



def cosine_similarity(sentence, s):
    x = np.array(sentence)
    y = np.array(s)
    Lx = np.sqrt(x.dot(x))
    Ly = np.sqrt(y.dot(y))
    cos_angle = x.dot(y)/(Lx * Ly)
    return cos_angle

def TestJac():
    s = 'hello this is a text'
    s1 = 'this is is a test'
    print(jaccard_similarity(s,s1))

def main():
    TestJac()

if __name__ == '__main__':
    main()
