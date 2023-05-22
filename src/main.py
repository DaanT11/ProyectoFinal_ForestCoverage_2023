
import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder

import numpy as np

## Steps saved as function in the .py procesing 

from src.procesing import  deploy_pred

from src.procesing import loading_data

from src.etl import saving_athena
#import
import logging
      




def main():
    logging.basicConfig(filename='./logs/results.log', level=logging.INFO,  filemode='w')
    
    
    try :
        logging.info('Started loading data')
        
        prod_data=loading_data()
        
        deploy_pred(prod_data)
        
        saving_athena()
    except:
        logging.info('The predictions could not being calculated ')

 
    

if __name__ == '__main__':
    main()
