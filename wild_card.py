import pickle
import os
from typing import final
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
ps=PorterStemmer()
wnl=WordNetLemmatizer()
from Model import BooleanIRSystem

from nltk import ngrams


filename='bigramindex'
infile = open(filename,'rb')
bigramindex = pickle.load(infile)
infile.close()

'''dictionary and bigramindex are unpickled'''


def AND(lst1, lst2):
    return list(set(lst1) & set(lst2))

def matchwildcard(str1):
    obj=BooleanIRSystem("./corpus/*")
    inverted_index=obj.postings

    str1=str1.lower()
    str1="$"+str1+"$"
    query=list(ngrams(str1, 2))
    '''bigrams of query terms are claculated using ngram method of nltk'''
    for bigram in query:
        temp=[]
        if('*' in bigram):
            if((bigram[0]=='*') and (bigram[1]=='*')):
                continue
            elif(bigram[0]=='*'):
                for word in bigramindex.keys():
                    for bigramlist in bigramindex[word]:
                        if(bigram[1]==bigramlist[1]):
                            temp.append(word)
            elif(bigram[1]=='*'):
                for word in bigramindex.keys():
                    for bigramlist in bigramindex[word]:
                        if(bigram[0]==bigramlist[0]):
                            temp.append(word)
        else:
            for word in bigramindex.keys():
                if(bigram in bigramindex[word]):
                    temp.append(word)
        inverted_index=AND(inverted_index, temp)
    '''the bigrams of query term are matched with that of all unique words in dataset'''
    
    print('matching words:')
    print(inverted_index)
    '''matching words are printed'''
    model = BooleanIRSystem("./corpus/*")
    for word in inverted_index:
        print(model.query(word))
    # ret=[]
    # for word in inverted_index:
    #     temp=inverted_index[ps.stem(wnl.lemmatize(word.lower()))]
    #     for inverted_index in temp:
    #         ret.append(inverted_index)
    # model = BooleanIRSystem("./corpus/*")
    # list1=set(ret)
    # print(list1)
    # for word in list1:
    #     print(model.query(word))

    return set(inverted_index)   
'''set of files having words that match with the wildcard query term are returned'''