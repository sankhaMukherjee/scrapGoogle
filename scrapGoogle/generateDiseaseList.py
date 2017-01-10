import os, re, string
import logging
import readPage

module_logger = logging.getLogger("findMeds.generateDiseaseList")

def getAlphabeticList(character):
    '''
    Returns the list of problems corresponding to a 
    particular character. This should not be used for
    obtaining the medical conditions for 0-9

    Parameters
    ----------
    character : str
        this is the character whose list will be returned

    Returns
    -------
    list
        The list of strings that comprise of the medications
    '''

    logger = logging.getLogger("findMeds.generateDiseaseList.getAlphabeticList")
    logger.info('Obtaining Medications for the character [%s]'%character)
    url = 'https://en.wikipedia.org/wiki/List_of_diseases_(%s)'%character

    page = readPage.readPage(url)

    if page is None:
        logger.info('Returning an empty list')
        return []

    result = []
    for l in page.findAll('li'):
        ls = ''.join([c for c in l.text if ord(c)<128 ])
        ls = ''.join([c for c in ls if c != '\n' ])
        if re.compile('^[A-Z]$').search(ls) is not None: continue
        if ls.strip() == '': continue
        if ls.lower()[0] != character.lower(): continue
        result.append( ls )

    logger.info('Returning Medications for the character [%s]'%character)
    return result

def getMedicationList(verbose=False):
    '''
    Returns the list of problems corresponding to a 
    particular character. This should not be used for
    obtaining the medical conditions for 0-9

    Parameters
    ----------
    
    Returns
    -------
    list
        The list of strings that comprise of the medications
    '''

    logger = logging.getLogger("findMeds.generateDiseaseList.getMedicationList")
    logger.info('Obtaining diseases for all characters')
    
    allDiseases = []
    for s in string.ascii_uppercase:
        if verbose:
            print 'Generating disease list for :[%s]'%s
        allDiseases += getAlphabeticList(s)

    logger.info('Returning disease list')
    return allDiseases

def saveDiseaseList(listToSave, fileName=None):
    '''
    Saves a list in a file. Each value will be 
    savedin a different line within the file. 

    Parameters
    ----------
    listToSave : iterator of strings
        An iterator containing the list of possible 
        medical conditions that one might encounter

    fileName : string
        An optional fileName to be used to save the list

    Returns
    -------
    '''

    logger = logging.getLogger("findMeds.generateDiseaseList.saveDiseaseList")
    logger.info('Saving the list')

    if not os.path.exists('../data'):
        logger.info('Unable to fine the folder [../data]. Attempting to create it')
        try:
            os.mkdir('../data')
        except:
            logger.error('Unable to create the folder [../data]. Make sure that the folder is writeable.')
            return

    if fileName is None:
        fileName = '../data/diseases.csv'
    else:
        fileName = os.path.join('../data', fileName)

    try:
        with open(fileName, 'w') as fOut:
            for l in listToSave:
                fOut.write(l + '\n')
    except:
        logger.error('Unable to write to the file')

    return

def getDiseaseList():
    '''
    Returns the list of diseases.

    If a file for the disease list isnt present, one
    will be created and cached before returning
    '''
    logger = logging.getLogger("findMeds.generateDiseaseList.getDiseaseList")
    logger.info('Obtaining the list of available diseases')

    if not os.path.exists('../data/diseases.csv'):
        logger.info('Unable to find the file ../data/diseases.csv. Generating the list')
        listToSave = getMedicationList(verbose=True)
        logger.info('Saving generated list to file ../data/diseases.csv.')
        saveDiseaseList(listToSave)
        return listTosave
    else:
        logger.info('Found cache file. returning results.')
        diseaseList = []
        with open('../data/diseases.csv') as fIn:
            diseaseList = [l.strip() for l in fIn.readlines() ]

        return diseaseList

    return

