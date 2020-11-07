"""
This is a base class for training models
Load models into a list that facilitate 

Args:
     None
Returns:
     Sets global variables 
Raises:
     Nothing
"""

from os.path import join, isfile,isdir
import xml.etree.ElementTree as ET

class Model: 
    def __init__(xml_element):
        self.model={}
        self.set_model(xml_element)
    def set_model(self,xml_element):

class Models:
    def __init__(self):
        #local base directories
        self.models_base=os.environ['data_base']
        ## stores a list of training models - 40 policies
        self.models_list=[]

    def getDirFile(self):
        file_list=[]
        try:
            file_list=[f for f in listdir(dir_name) if isfile(join(dir_name,f))]
        except:pass
        return file_list