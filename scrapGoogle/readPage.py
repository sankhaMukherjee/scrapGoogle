import urllib2
import logging
from bs4 import BeautifulSoup

module_logger = logging.getLogger("findMeds.readData")

def readPage(url):
    '''
    Returns the page read from the specified url
    
    This is a function that takes a url and 
    returns the contents of the url in the 
    form of a BeautifulSoup object. In case
    there is an error in reading data from 
    the web, this program is going to return
    None

    Parameters
    ----------
    url : str
        URL that we want to get the source of

    Returns
    -------
    BeautifulSoup object or None
        A None will be returned if the data from
        the website cannot be read for whatever 
        reason
    
    '''

    logger = logging.getLogger("findMeds.readData.readPage")
    logger.info( 'Attempting to read URL[%s]'%url )

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    # This is going to attempt to read the 
    # data if it is possible
    req = urllib2.Request(url, headers=hdr)
    try: 
        html = urllib2.urlopen(req).read()
    except urllib2.URLError as e:
        logger.error('Unable to read from the url[%s]: [%s]'%( url, e.reason ))
        return None

    logger.info( 'Able to read data.' )
    soup = BeautifulSoup(html)

    return soup
