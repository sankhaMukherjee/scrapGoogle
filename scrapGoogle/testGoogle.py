import google
import urllib2 
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import pandas as pd 
import numpy as np
from time import time

def getTextFromURL(url, verbose=False):
    '''
        Given a URL, this function is going to return
        the text portion of the webpage for the URL. It
        will return an empty string if there is some
        sort of error ...
    '''
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    
    html = ''
    
    # This is going to attempt to read the 
    # data if it is possible
    req = urllib2.Request(url, headers=hdr)
    try: 
        html = urllib2.urlopen(req).read()
    except urllib2.URLError as e:
        if verbose:
            print 'Problem with extracting the HTML'
            print e.reason
    # print html

    soup = BeautifulSoup(html)
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    html = soup.get_text()  
    html = filter( lambda m: m < 128 , map(ord, html))
    html = ''.join(map(chr, html))

    return html

def stats(words):
    '''
        Some simple statistics for the wods
    '''
    return nltk.FreqDist(words).most_common(50)

def allStatsURL(url, numURLs=10):

    totalWords = 0
    allStats   = []
    urls       = google.search(url)
    i = 0
    for url in urls:

        if url.endswith('.pdf'): continue
        i += 1
        if i > numURLs: break
        print '*'*10,'\n*', i, url, '\n', '*'*10

        html   = getTextFromURL(url, verbose=False)
        tokens = nltk.wordpunct_tokenize( html )
        text   = nltk.Text( tokens )

        if len(tokens) == 0:
            print 'No text here'
            continue
            
        # print tokens[:10]
        # print text.collocations()

        words = [ w.lower() for w in tokens]
        words = [ w for w in words  if w not in string.punctuation ]

        totalWords += len(words)
        
        words = [ w for w in words if w not in stopwords.words('english') ]
        # words = [ nltk.WordNetLemmatizer().lemmatize(w) for w in words ]
        
        allStats += [(a,b,i) for a, b in stats( words )]

        # print nltk.pos_tag( tokens )

    allStatsDf = pd.DataFrame(allStats, columns=['word', 'number', 'document'])
    # allStats = allStats.pivot_table(index='word', 
    #     columns=['document'], 
    #     values='number', 
    #     aggfunc=np.mean).reset_index()

    # print allStats.dropna().sort(0, ascending=False)
    return allStatsDf, totalWords

def gutenbergWordFrequency(words):
    '''
    Given a group of words, this comptes the
    probability of finding the word within the
    corpus ...
    '''

    words      = [w.lower() for w in words]
    resultDict = { word:0 for word in words }
    times = {}

    totalWords = 0
    for story in nltk.corpus.gutenberg.fileids():
        
        toSkip = ['bible', 'moby_dick', 'parents', 'emma']
        if any([(k in story) for k in toSkip]): continue


        initTime = time()
        print 'Now computing for: [%s]'%story
        gWords = nltk.corpus.gutenberg.words(story)
        totalWords += len(gWords)
        for word in words:
            resultDict[word] += len([1 for w in gWords if w.lower() == word])

        times[ story ] = time()-initTime

    for word in resultDict:
        resultDict[word] = 1.0*resultDict[word]/totalWords

    times = pd.Series( times )
    times.sort()
    resultDictSeries = pd.Series(resultDict)
    resultDictSeries.sort(ascending=False)
    print
    print times
    print
    print resultDictSeries 

    return resultDict


if __name__ == '__main__':
    
    allStatsDf, N = allStatsURL('Abilify 10mg QD', 20)
    df = allStatsDf[['word', 'number']].groupby('word').agg(sum).reset_index().sort('number', ascending=False)
    df = df[ df.word.str.isalpha() & (df.word.str.len() > 2) ]
    df['freq'] = df.number / N
    print df

    gWords = gutenbergWordFrequency(list(df.word)[:15])
    print gWords


    print 'done'