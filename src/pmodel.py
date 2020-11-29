"""
This is a base class for training models.
It loads models into a list that facilitates the analysis 
and the comparison between models.

Authors: 
   Lucie Hutchins
   Tim Bruce
"""

##import os
from os import listdir
from os.path import join, isfile,isdir,dirname, realpath
import xml.etree.ElementTree as ET


class PPolicy:
    def __init__(self,xml_model):
        self.policy={}
        self.set_policy(xml_model)
    
    def set_policy(self, xml_model):
        try:
            self.policy["title"]=xml_model.find("./label").text
            self.policy["desc"]=xml_model.find("./desc")
            self.policy["url"]=xml_model.find("./url")
            self.policy["optins"]=self.get_optins(xml_model.findall("./optin"))
            self.policy["optouts"]=self.get_optouts(xml_model.findall("./optout"))
        except: pass
    '''
     A given controller may implement more than one
     optin type, we will store optins into an array.
    '''
    def get_optins(self, xml_optins):
        moptins=[]
        for optin in xml_optins:
            otype=optin.attrib["type"]
            label=optin.find("label").text
            moptins.append({"type":otype,"title":label})
        return moptins

    '''
     A given controller may implement more than one
     optout type, we will store optouts into an array.
     For example: outout from data sharing, outout from cookies, ...
    '''
    def get_optouts(self, xml_optouts):
        moptouts=[]
        for optout in xml_optouts:
            label=optout.find("label").text
            urls=[]
            for option in optout.findall("./url"):
                urls.append({"type":option.attrib["type"],"desc":option.text})
            moptouts.append({"title":label,"options":urls})
        return moptouts
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
        ## get xml object
        xml_model=self.getXmlDocRoot(xml_file)
        if xml_model is not None:
            self.model["main_page"]=self.get_main_page(xml_model)
            self.model["ppolicies"]=self.get_privacy_policies(xml_model)
        
    def get_main_page(self, xml_model):
        main_page={"title":"","url":""}
        try:
            main_page.title=xml_model.find(".//main_page/label").text
            main_page.url=xml_model.find(".//main_page/url").text
        except:pass
        return main_page
    
    ## The anticipation is that a given model may have more than one privacy policies
    def get_privacy_policies(self,xml_model):
        policies=[]
        try:
            for policy in xml_model.fincall("./privacy_policy"):
                policies.append(PPolicy(policy))
        except:pass
        return policies
     
    def getXmlDocRoot(self,xml_file):
      doc_root=None
      print("File "+xml_file )
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
                xml_file=join(model_dir,model_file)
                self.models_list.append(Model(xml_file))

    def getModelsList(self,model_dir):
        file_list=None
        try:
            file_list=[f for f in listdir(model_dir) if isfile(join(model_dir,f))]
        except:raise
        return file_list

    '''
    To Do

    More  members will be added  here for the analysis
    '''
if __name__== "__main__":
    models_dir=join(dirname(realpath(__file__)),"models")
    if isdir(models_dir):
        models=Models(models_dir)
        for model in models.models_list:
            print(model.model)
        print("Current directory is: %s"%(models_dir))
    else:
        print("ERROR: missing models directory - see %s"%(models_dir))
