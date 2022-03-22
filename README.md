# Boolean Information Retrieval System

This is a Boolean Query Model for Information Retrieval. 
The Boolean model of information retrieval(BIR) is a classical information retrieval model and, at the same time, the first and most-adopted one. It is used by many IR systems to this day. The BIR is based on Boolean logic and classical set theory in that both the documents to be searched and the user's query are conceived as sets of terms. Retrieval is based on whether or not the documents contain the query terms. 
Information retrieval is the activity of obtaining information system resources relevant to an information need from a collection of information resources. Searches can be based on full-text or other content-based indexing. We use a Boolean Query Model to retrieve relevant information from our documents.

The document corpus consists of documents, provided by our Professor N.L.Bhanu Murthy, IC of course CS F469. 

## Getting Started

- Install Python 3.6+

You need to install nltk for tokenization and stemming. You can do it via pip:

sudo pip3 install -U nltk

- To download NLTK data used for the model, open your terminal or command prompt and enter following commands:

```bash
$ python3
>>> import nltk
>>> nltk.download('stopwords')
```

Skip this section if you already have NLTK installed and NLTK Data downloaded

### Queries

Precedence order: NOT (~) > AND (&) > OR (|)

- Single term => `brutus`
- AND => `richard & henry`
- OR => `brutus | richard`
- Parenthesis => `( brutus | richard ) & henry`
                 `( ~brutus | henry ) & richard`

## Methodology

1. Preprocessing to build standard inverted index
   - Remove special characters and digits
   - Tokenize
   - Lowercasing
   - Stemming using `PorterStemmer`
   - Add unique words and their postings to the index
   - WildCard Queries