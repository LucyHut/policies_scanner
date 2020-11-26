"""
This is a base class for training models.
It loads models into a list that facilitates the analysis 
and the comparison between models.

Authors: 
   Lucie Hutchins
   Tim Bruce
"""

import os
from os.path import join, isfile,isdir
import xml.etree.ElementTree as ET

'''
Args:
     model xml file
Returns:
     Load the xml element into an object
Raises:
    Issues with the model file

'''
class Model: 
    def __init__(self, xml_file):
        self.model={}
        self.set_model(xml_file)

    def set_model(self,xml_file):
        '''
        To Do

        This is were I will put the code to load a model into an object
        we will call getXmlDocRoot to get the xml_element from the xml file
        '''

    def getXmlDocRoot(self,xml_file):
      doc_root=None
      if not isfile(xml_file): 
          print("File does not exist "+xml_file )
          return doc_root
      try:
           xml_doc=ET.parse(xml_file)
           doc_root=xml_doc.getroot()
      except:raise
      return doc_root

'''
Args:
     models base directory

Returns:
     List of models and that actions on these models
Raises:
    Issues with the models directory

'''
class Models:
    def __init__(self,model_dir):
        ## stores a list of training models - 40 policies
        self.models_list=[]
        self.loadModels(model_dir)

    def loadModels(self, model_dir):
        mlist=self.getModelsList(model_dir)
        if isinstance(mlist, list):
            for model_file in mlist:
                self.models_list.append(Model(model_file))

    def getModelsList(self,model_dir):
        file_list=None
        try:
            file_list=[f for f in os.listdir(model_dir) if isfile(join(model_dir,f))]
        except:raise
        return file_list

    '''
    To Do

    More  members will be added  here for the analysis
    '''