from sklearn.feature_extraction.text import CountVectorizer
from pprint import pprint
import operator
 
 
 
def encode_sen(sen,corpus):
    """
    input: sentence and corpus 
    output :  bag of words vector of sentence 
    """
    cv = CountVectorizer()
    cv = cv.fit(corpus)
    vec = cv.transform([sen]).toarray()
    return vec[0]
 
def cosin_distance(vector1, vector2):
    """
    input: two bag of words vectors of sentence  
    output :  the similarity between the sentence
   
    """
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)
 
 
def doc_list2str(doc_list):
    """
    transform the doc_list to str 
    """
    docu_str = ""
    for wordlist in doc_list:
        docu_str += " ".join(wordlist)
    return docu_str
 
 
def MMR(doc_list,corpus):
    """
    input ：corpus and the docment you want to extract 
    output :the abstract of the docment 
    """
    Corpus = corpus
    docu = doc_list2str(doc_list)
    doc_vec = encode_sen(docu,Corpus)
    QDScore = {}
    ###calculate the  similarity of every sentence with the whole corpus
    for sen in doc_list:
        sen = " ".join(sen)
 
        sen_vec = encode_sen(sen,corpus)
        score = cosin_distance(sen_vec,doc_vec)
        QDScore[sen] = score
 
  
    n = 2
    alpha = 0.7
    Summary_set = []
    while n > 0:
        MMRScore = {}
        ### select the first sentence of abstract
        if Summary_set == []:
            selected = max(QDScore.items(), key=operator.itemgetter(1))[0]
            Summary_set.append(selected)
 
        Summary_set_str = " ".join(Summary_set)
 
        for sentence in QDScore.keys():
             #calculate MMR  
            if sentence not in Summary_set:
                sum_vec = encode_sen(Summary_set_str, corpus)
                sentence_vec = encode_sen(sentence,corpus)
                MMRScore[sentence] = alpha * QDScore[sentence] - (1 - alpha) * cosin_distance(sentence_vec,sum_vec)
        selected = max(MMRScore.items(), key=operator.itemgetter(1))[0]
        Summary_set.append(selected)
        n -= 1
    # print(len(Summary_set))
    return  Summary_set
