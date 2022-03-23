# Boolean Information Retrieval System

This is a Boolean Query Model for Information Retrieval. 
The Boolean model of information retrieval(BIR) is a classical information retrieval model and, at the same time, the first and most-adopted one. It is used by many IR systems to this day. The BIR is based on Boolean logic and classical set theory in that both the documents to be searched and the user's query are conceived as sets of terms. Retrieval is based on whether or not the documents contain the query terms. 
Information retrieval is the activity of obtaining information system resources relevant to an information need from a collection of information resources. Searches can be based on full-text or other content-based indexing. We use a Boolean Query Model to retrieve relevant information from our documents.

The document corpus consists of documents, provided by our Professor N.L.Bhanu Murthy, IC of course CS F469. 

## Getting Started

- Install Python 3.6+

You need to install nltk for tokenization and stemming. You can do it via pip:

```bash
pip3 install -U nltk
```

- To download NLTK data used for the model, open your terminal or command prompt and enter following commands:

```bash
$ python3
>>> import nltk
>>> nltk.download()
```

Skip this section if you already have NLTK installed and NLTK Data downloaded

### Queries

Use &,~,| as boolean operators.

Precedence order: NOT (~) > AND (&) > OR (|)

- Single term => `brutus`
- AND => `richard & henry`
- OR => `brutus | richard`
- Parenthesis => `( brutus | richard ) & henry`
                 `( ~brutus | henry ) & richard`

## Procedure

a. Stopword Removal - self.stopword = set(stopwords.words("english")). 
                      Implemented in BooleanIRModel class of Model file.
                      
b. Stemming -   words = [self.PorterStemmer().stem(word) for word in words]. 
                        Implemented in preprocess method. 
                        
c. Building Index - for term in terms:
                        self.postings[term].append(i)
                    self.dictionary = self.postings.keys()
                    Implemented in preprocess method. 
                    
d. Querying - Implemented in query.py where we enter the query. The operations on query is done in model.py in query,find,bits,solve methods

Preprocess method does preprocessing to build standard inverted index
1. Remove special characters
2. Remove digits
3. Tokenize
4. Lowercasing
5. Stemming using PorterStemmer
6. Add unique words and their postings to the index
