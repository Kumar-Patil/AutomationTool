'''
Created on 11-Mar-2016

@author: Santosh Patil
'''
import logging

class customLog(object):
    '''
    classdocs
    '''

    LOG_FILENAME = 'automation.log'
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',filename=LOG_FILENAME,level=logging.INFO)
    
    def __init__(self):
        '''
        Constructor
        '''
    def log(self,bmcLogMesssage):
        logging.info(bmcLogMesssage)
        
    