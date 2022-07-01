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

**Test Case ( Mispelt Words)---Tackled by editdistance**
Preprocessing + Indexing Time:  23.633147954940796
Search Query: **henny | (~shakepeare)**
henny  is not found in the corpus!
Did you mean these ? : 
denis
meiny
heady
dennis
hence
henry
herby
envied
heavy
mentis
sennois
tennis
penny
henrys
fenny
bonny
envies
herne
senis
deny
hens
finny
envys
hernes
heaviness
envy
denies
nonny
sunny
ginnys
denied
envying
ninnys
hewhy
denying
hannibal
thenby
denny
Giving results based on:  henry
shakepear  is not found in the corpus!
Did you mean these ? : 
shakespeare
Giving results based on:  shakespeare
Searching Time:  1.53685951232910
['henry-iv-part-1_TXT_FolgerShakespeare.txt', 'henry-iv-part-2_TXT_FolgerShakespeare.txt', 'henry-vi-part-1_TXT_FolgerShakespeare.txt', 'henry-vi-part-2_TXT_FolgerShakespeare.txt', 'henry-vi-part-3_TXT_FolgerShakespeare.txt', 'henry-viii_TXT_FolgerShakespeare.txt', 'henry-v_TXT_FolgerShakespeare.txt', 'king-john_TXT_FolgerShakespeare.txt', 'lucrece_TXT_FolgerShakespeare.txt', 'richard-iii_TXT_FolgerShakespeare.txt', 'richard-ii_TXT_FolgerShakespeare.txt', 'the-taming-of-the-shrew_TXT_FolgerShakespeare.txt', 'venus-and-adonis_TXT_FolgerShakespeare.txt']
Entering Query + Searching Time:  12.86674427986145

**Test Case (Correctly spelt words)**
Preprocessing + Indexing Time:  29.037702798843384
**Search Query:(richard & henry) | romeo**
Searching Time:  2.70437240600586
['henry-iv-part-1_TXT_FolgerShakespeare.txt', 'henry-iv-part-2_TXT_FolgerShakespeare.txt', 'henry-vi-part-1_TXT_FolgerShakespeare.txt', 'henry-vi-part-2_TXT_FolgerShakespeare.txt', 'henry-vi-part-3_TXT_FolgerShakespeare.txt', 'henry-viii_TXT_FolgerShakespeare.txt', 'henry-v_TXT_FolgerShakespeare.txt', 'king-john_TXT_FolgerShakespeare.txt', 'richard-iii_TXT_FolgerShakespeare.txt', 'richard-ii_TXT_FolgerShakespeare.txt', 'romeo-and-juliet_TXT_FolgerShakespeare.txt', 'the-taming-of-the-shrew_TXT_FolgerShakespeare.txt']
Entering Query + Searching Time:  20.63770055770874

**Test Case(Combination of correct and mispelled word)**
Preprocessing + Indexing Time:  29.323376893997192
**Search Query:juliet | ~shakepeare**
shakepear  is not found in the corpus!
Did you mean these ? : 
shakespeare
Giving results based on:  shakespeare
Searching Time:  2.12913131713867
['measure-for-measure_TXT_FolgerShakespeare.txt', 'romeo-and-juliet_TXT_FolgerShakespeare.txt']
Entering Query + Searching Time:  15.994519710540771
