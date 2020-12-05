"""
This is a base class for training models.
It loads models into a list that facilitates the analysis 
and the comparison between models.

Authors: 
   Lucie Hutchins
   Tim Bruce

Modification date: December 04, 2020

"""

##import os
from os import listdir
from os.path import join, isfile,isdir,dirname, realpath
import xml.etree.ElementTree as ET

'''
A policy is an object with the following members:
  -- a title
  -- a brief summary
  -- list of optins
  -- a list of opt-outs

'''
class PPolicy:
    def __init__(self,xml_model):
        self.policy={}
        self.set_policy(xml_model)
    
    def set_policy(self, xml_model):
        if xml_model is not None:
            try:
                if xml_model.find("./label") is not None:
                    self.policy["policy_title"]=xml_model.find("./label").text
                if xml_model.find("./desc") is not None:
                    self.policy["desc"]=xml_model.find("./desc").text
                if xml_model.find("./url") is not None: 
                    self.policy["policy_url"]=xml_model.find("./url").text
                if xml_model.findall("./optin") is not None:
                    self.policy["optins"]=self.get_optins(xml_model.findall("./optin"))
                if xml_model.findall("./optout") is not None:
                    self.policy["optouts"]=self.get_optouts(xml_model.findall("./optout"))
            except: raise

    '''
     A given controller may implement more than one
     optin type, we will store optins into an array.
    '''
    def get_optins(self, xml_optins):
        moptins=[]
        if xml_optins is not None:
            for optin in xml_optins:
                moptins.append({"type":optin.attrib["type"],"title":optin.find("label").text})
        return moptins

    '''
     A given controller may implement more than one
     optout type, we will store optouts into an array.
     For example: optout from data sharing, optout from cookies, ...
    '''
    def get_optouts(self, xml_optouts):
        moptouts=[]
        if xml_optouts is not None:
            for optout in xml_optouts:
                if optout:
                    label=optout.find("optout_label").text
                    options=[]
                    for option in optout.findall("./option"):
                        options.append({"type":option.attrib["type"],"desc":option.text})
                    moptouts.append({"title":label,"options":options})
        return moptouts
'''
A controller is an object with the following members:
  -- main page -> an object
  -- list of policies

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
        if xml_model.find("./main_page/label") is None: return None
        try:
            main_page["title"]=xml_model.find("./main_page/label").text
            main_page["url"]=xml_model.find("./main_page/url").text
        except:pass
        return main_page
    
    ## The anticipation is that a given model may have more than one privacy policies
    def get_privacy_policies(self,xml_model):
        policies=[]
        try:
            for policy in xml_model.findall("./privacy_policy"):
                policies.append(PPolicy(policy).policy)
        except:raise
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
     List of models and the actions on these models
Raises:
    Issues with the models 

'''
class Models:
    def __init__(self,model_dir):
        ## stores a list of training models - 40 policies
        self.models_list=[]
        self.loadModels(model_dir)

    def loadModels(self, model_dir):
        mlist=self.getModelsList(model_dir)
        if isinstance(mlist, list):
            self.models_list=[]
            for model_file in mlist:
                if "template" in model_file: continue
                xml_file=join(model_dir,model_file)
                self.models_list.append(Model(xml_file))

    def getModelsList(self,model_dir):
        file_list=None
        try:
            file_list=[f for f in listdir(model_dir) if isfile(join(model_dir,f))]
        except:raise
        return file_list

    '''
    Returns Optins choices tally
    '''
    def getOpins_tally(self):
        optins={}
        if isinstance(self.models_list,list):
            for site in self.models_list:
                if isinstance(site.model,dict):
                    try:
                        for policy in site.model['ppolicies']:
                            for optin in policy["optins"]:
                                otype=optin["type"]
                                if optin["type"] not in optins: optins[otype]=1
                                else: optins[otype]+=1
                    except:raise
        return optins

    '''
    Returns Optout choice  types tally
    '''
    def getOptouts_tally(self):
        options={}
        if isinstance(self.models_list,list):
            for site in self.models_list:
                if isinstance(site.model,dict):
                    try:
                        for policy in site.model['ppolicies']:
                            for optout in policy["optouts"]:
                                if isinstance(optout,dict):
                                    for option in optout["options"]:
                                        otype=option["type"]
                                        if option["type"] not in options: options[otype]=1
                                        else: options[otype]+=1
                    except:raise
        return options

    '''
    Returns Optout options count distribution
    '''
    def getOptouts_options_dist(self):
        options={}
        if isinstance(self.models_list,list):
            for site in self.models_list:
                if isinstance(site.model,dict):
                    try:
                        for policy in site.model['ppolicies']:
                            for optout in policy["optouts"]:
                                if isinstance(optout,dict):
                                    otype=len(optout["options"])
                                    if otype not in options: options[otype]=1
                                    else: options[otype]+=1
                    except:raise
        return options

           
if __name__== "__main__":
    models_dir=join(dirname(realpath(__file__)),"models")
    if isdir(models_dir):
        models=Models(models_dir)
        for model in models.models_list:
            print("**********************************************************")
            print("**********************************************************")
            print(model.model)
        print("Total models: %d"%(len(models.models_list)))
        print(models.getOpins_tally())
        print(models.getOptouts_tally())
        print(models.getOptouts_options_dist())
    else:
        print("ERROR: missing models directory - see %s"%(models_dir))
