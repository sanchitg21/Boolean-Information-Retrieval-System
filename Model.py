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
import sys
import time
from Edit_distance import minEditDistance

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
        """ Function to find all the unique words in the document
        passed as a parameter.Set ensures we get unique elements. 
        We then typecast a set to a list to return a list of unique words """ 
        return list(set(words))
    
    def punctuationMarks(self, text):
        """Removes punctuation marks/ special characters"""
        
        # Regular expressions are a powerful language for matching text patterns.
        regex = re.compile(r'[^a-zA-Z\s]')

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
        """ Iterate through the list of documents in the folder to find
        all the unique words present after deleting numbers and
        special characters. Ignore the stopwords while finding the
        unique words. """
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
    
    def rot(str,n):

        """ Function to rotate the string passed as a parameter
        by n places and then return it. It is used to
        calculate all the permuterm combinations possible
        of the string that is passed as a parameter. """
    
        return str[n:]+str[:n]
    
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
                if token[0] == "~":
                    token = token[1:]
                
                """ Performing a spell check and correction on all the query
                words if the spelling is wrong. This is done by comparing
                the edit distance between the query words with all the
                unique words across all the documents. The word is then
                replaced by the word which has the minimum edit distance and 
                among those, the one having the largest posting list.
                If the query word exists in the documents, the minimum edit
                distance is zero and the word remains unchanged. """
                count=0
                for key in self.dictionary:
                    distance= minEditDistance(key,token,len(key),len(token))
                    if distance <= threshold:
                        count=count+1
                        for term in self.reverse_stem[key]:
                            if(threshold >= minEditDistance(term,token,len(term),len(token))):
                                keys.append(term)
                if count == 0:            
                    print( token," is not found in the corpus!" )
                    return np.zeros(len(self.doc), dtype=bool)
                
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
        if token[0] == "~":  
            # unary not operator(~)
            negation = True

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
                """ Applies the unary not operator on the relevant query term.
                This is used to invert the values present in the list for that term."""
                length = len(binary_list)
                for i in range(length):
                    if binary_list[i] == True :
                        binary_list[i] = False
                    else:
                        binary_list[i] = True
                
            # Return bit list of the word
            return binary_list

        else:
            # Word is not present in the corpus
            if token[0]=="~":
                print(token[1:] ," is not found in the corpus!" )
            else:
                print(token," is not found in the corpus!")
            
            
            if(len(other_words)):
                print("Did you mean these ? : ")
            other_words = list((set(other_words) - set(self.dictionary)))
            #Printing all the words under the threshold value for mispelt tokens
            maxLength = 0
            min_word = ""
            if token[0]=="~":
                token=token[1:]
            for key in other_words:
                if maxLength < len(self.postings[self.ps.stem(key.lower())]):
                    maxLength = len(self.postings[self.ps.stem(key.lower())])
                    min_word = key
                elif maxLength == len(self.postings[self.ps.stem(key.lower())]):
                    if minEditDistance(key,token,len(key),len(token)) < minEditDistance(min_word,token,len(min_word),len(token)):
                        min_word = key
                     
            print("Giving results based on: ",min_word)
            binary_list = np.zeros(totalDoc, dtype=bool)
            posting = self.postings[self.ps.stem(min_word)]
            for doc_id in posting:
                binary_list[doc_id-1] = True
            if negation:
                length = len(binary_list)
                for i in range(length):
                    if binary_list[i] == True :
                        binary_list[i] = False
                    else:
                        binary_list[i] = True
            return binary_list


    def solve(self, left_word, right_word, b):
        """
        :b: binary operation to perform
         The final result is calculated and returned. 
         This list is then iterated through
         and whenever the value is true, it implies that the document
         satisfies the given boolean query and its name is displayed.
         If the value is false, it skips to the value of the next document
         in the resultant list. "
        """
        if b == "&":
            #searching for documents with both left and right query words
            return left_word & right_word
        elif b == "|":
            #searching for documents containing either left or right or both query words
            return left_word | right_word
        else:
            return 0
