from nltk.corpus import stopwords
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.tokenize import word_tokenize

import pandas as pd
import numpy as np

from fquery import is_binaryoperator
from fquery import convert
from fquery import is_Rparanthesis
from fquery import is_Lparanthesis

from collections import defaultdict
import glob
import os
import re
import time
from Edit_distance import minEditDistance

class Node:
    def __init__(self ,DocID, freq = None):
        self.freq = freq
        self.doc = DocID
        self.nextval = None
    
class LinkedList:
    def __init__(self ,head = None):
        self.head = head

class BooleanIRSystem(object):

    # Self represents the instance of the class. 
    # By using the “self” keyword we can access the attributes and methods of the class in python. 
    # It binds the attributes with the given arguments.
    
    def __init__(self, path):
        #body of a constructor
       
        # Path to corpus of documents
        self.corpus = path

        # Set of all unique terms in the corpus. We use a set to retrieve unique terms.
        self.dictionary = set()
        
        #Stopwords
        self.stopword = set(stopwords.words("english"))
        
        #Stemming
        self.reverse_stem = defaultdict(list)
        self.ps = PorterStemmer()

        # Documents is a dictionary from key:documents to value:document_name
        self.doc = dict()
        
        # A posting list is a list of document identifiers (or document IDs) containing the term.
        self.postings = defaultdict(list)

        #Preprocessing: Producing a list of normalized token.
        self.preprocess()

    def unique(self, words):
        # Set ensures we get unique elements. We then typecast a set to a list to return a list of unique words
        return list(set(words))

    def punctuationMarks(self, text):
        """Removes punctuation marks/ special characters"""
        
        # Regular expressions are a powerful language for matching text patterns.
        regex = re.compile(r'[^0-9a-zA-Z\s]')

        # Replace
        text = re.sub(regex,'',text)
        return text
    
    def is_binaryoperator(token):
        if token == "&" or token == "|":
            return True
        return False
    
    def preprocess(self):
        start_time = time.time()
        """Preprocess the corpus"""

        # Document Index/ID created to process every document one by one
        i = 1

        # Loop for every document in the corpus
        for filename in glob.glob(self.corpus):
            
            # Reading document
            with open(filename, "r") as file:
                text = file.read()

            # Removes all the punctutation marks/special characters from the text
            text = self.punctuationMarks(text)

            # Tokenize text into words
            words = word_tokenize(text)

            # Remove stopwords
            # convert remaining words to lowercase
            words = [word.lower() for word in words if word not in self.stopword]
            
            #Stemming
            for word in words:
                self.reverse_stem[self.ps.stem(word)].append(word)
            for key in self.reverse_stem.keys():
                self.reverse_stem[key] = self.unique(self.reverse_stem[key])
            words = [self.ps.stem(word) for word in words]
            
            terms = self.unique(words)

            # Add posting to Final Posting List
            for term in terms:
                self.postings[term].append(i)

            # Make a list of indexed documents
            self.doc[i] = os.path.basename(filename)

            i = i + 1

        # Making inverted index out of final posting list.
        self.dictionary = self.postings.keys()
        end_time = time.time()
        total_time = end_time - start_time
        print("Preprocessing + Indexing Time: ", total_time)
        return start_time

    def query(self, query):
        start_time = time.time()
        """Query the indexed documents using a boolean model
        :query: valid boolean expression to search for
        :returns: list of matching document names
        """
        # Tokenize query
        q = word_tokenize(query)
        
        # Convert infix query to postfix query
        q = convert(q)
        
        # Evaluate query against already processed documents
        docs = self.find(q)
        
        end_time = time.time()
        total_time = end_time - start_time
        print("Searching Time: ", ("{0:.14f}".format(total_time)))
        
        return docs

    def find(self, q):
        """Evaluates the query
        returns names of matching document 
        """
        word = []
        # q: list of query tokens in postfix form
        for token in q:
            searched_token = token
            # Token is an operator,
            # Pop two elements from stack and apply it.
            if is_binaryoperator(token):
                # Pop right operand
                if len(word)==0:
                    raise ValueError("Query is not correctly formed!")
                right_word = word.pop()

                # Pop left operand
                if len(word)==0:
                    raise ValueError("Query is not correctly formed!")
                left_word = word.pop()

                # Perform task
                doc_list = self.solve(left_word, right_word, token)

                word.append(doc_list)

            # Token is an operand, push it to the word
            else:        
                # Lowercasing and stemming query term
                token = self.ps.stem(token.lower())
                
                # Edit distance
                threshold =2;
                keys = []
                for key in self.dictionary:
                    distance= minEditDistance(key,token,len(key),len(token))
                    if distance <= threshold:
                        for term in self.reverse_stem[key]:
                            keys.append(term)
                # Push it's bit vector into operand stack
                word.append(self.bits(searched_token,token,keys))
        
        if len(word) != 1:
            print("Wrong query!")
            return list()

        # Find out documents corresponding to set bits in the list
        docs = [self.doc[i + 1] for i in np.where(word[-1])[0]]

        return docs

    def bits(self, token, word, other_words):
        """Make bit list out of a word
        :returns: bit list of word with bits set when it appears in the particular documents
        """
        # Size of bit list
        totalDoc = len(self.doc)

        negation = False

        if word[0] == "~":
            negation = True
            word = word[1:]

        if word in self.dictionary:
            # Intialize a binary list for the word
            binary_list = np.zeros(totalDoc, dtype=bool)

            # Locate query token in the dictionary and retrieve its posting list
            posting = self.postings[word]

            # Set bit=True for doc_id in which query token is present
            for doc_id in posting:
                binary_list[doc_id-1] = True

            if negation:
                # Instance of NOT operator token,
                # bit list is supposed to be negated
                for bit in binary_list:
                    if bit == True:
                        bit= False
                    else:
                        bit= True

            # Return bit list of the word
            return binary_list

        else:
            # Word is not present in the corpus
            print( token,"was not found in the corpus!" )
            print("Did you mean these ? : ")
            other_words = list((set(other_words) - set(self.dictionary)))
            for key in other_words:
                print(key)
            return np.zeros(totalDoc, dtype=bool)

    def solve(self, left_word, right_word, b):
        """
        :b: binary operation to perform
        :returns: result of the operation
        """

        if b == "&":
            #searching for documents with both left and right query words
            return left_word & right_word

        elif b == "|":
            #searching for documents containing either left or right or both query words
            return left_word | right_word

        else:
            return 0
