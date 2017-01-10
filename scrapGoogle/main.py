import logging, os
from datetime import datetime

import generateDiseaseList

def main():
    '''
        Initialize everything over here
    '''
    logger = logging.getLogger("findMeds")
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler(datetime.now().strftime('../logs/[%Y-%m-%d_%H-%M-%S][main].log'))
 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
 
    logger.info("Program started")
    
    diseases = generateDiseaseList.getDiseaseList()
    print diseases

    logger.info("Done!")
    return

if __name__ == '__main__':
    main()
    