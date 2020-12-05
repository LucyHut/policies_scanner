# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.common.exceptions as se
import re

'''
'''
import getopt, os, sys
from datetime import datetime

from os.path import isdir, dirname, join, abspath, basename
# import pmodel

from urllib.parse import urlparse

## domain = urlparse('http://www.example.test/foo/bar').netloc
## print(domain) # --> www.example.test

'''
Organization: The University Of Maine
Authors: Tim Bruce and Lucie N. Hutchins
Date: November 2020
'''
def display_header():
    header='''
****************** Starting policy-extrator *******************************************

This tool extracts the Opt-out and Opt-in sections from a given privacy policy document

***************************************************************************************
    '''
    print("%s"%(header))

def prog_usage():
    usage='''
******************* policy-extrator ****************************************************

The tool extracts the Opt-out and Opt-in sections from a given privacy policy document.


*****************************************************************************************
 Usage: PROG [-h] --curl=main_page_url [--purl=policy_page_url]
 Where:
     -h To show the usage
     -c url Or --curl=url  ... required, specifies the controller main page
     -p url Or --purl=url  ... optional, specifies the direct link to the privacy policy page  
      

 Example 1 -  The user does not have direct link to the privacy policy - in that case, the program
              expects to get the link of the privacy policy document from the controller main page
  Usage: 
       python PROG  -c https://www.nih.gov
       OR 
       python PROG  --curl=https://www.nih.gov

  Example 2 -  The user  provides the direct link to the privacy policy document
  Usage: 
       python PROG --p https://www.nih.gov/web-policies-notices
       OR 
       python PROG --purl=https://www.nih.gov/web-policies-notices

 ASSUMPTIONS: 
       1) The user must provide either the controller's main site url or a direct url to the privacy policy
       2) The privacy policy url takes precendence if both urls are provided
       3) The url provided is a valid url of either the controller main site or the privacy policy document
       4) The document rendered is an html document
       5) Python3 is used and all the dependencies have been installed 
   '''
    print("%s"%(usage))


# This function draws from the links.txt file for URLs.
def multiple_policy_extraction(urls=[], policy_urls=[]):
    policy_objects = []
    if urls:
        for url in urls:            # For every url, instantiate the Policy class with the url
            policy_objects.append(Policy(website_url=url))
    if policy_urls:
        for url in policy_urls:
            policy_objects.append(Policy(policy_url=url))

    for policyObject in policy_objects:               # Output verification
        if policyObject.extracted_policy is not None:
            print("Extracted " + policyObject.policy_url)
    return policy_objects


# Class for storing policy information
class Policy:
    def __init__(self, website_url=None, policy_url=None, extracted_policy=None):
        self.url = website_url                  # Url of the website's main page
        if policy_url is not None:
            self.policy_url = policy_url        # URL of the privacy policy
        else:
            self.policy_url = self.retrieve_policy_url()
            print("Automatically retrieved policy URL for %s.\n Policy found at %s" % (website_url, self.policy_url))

        if extracted_policy is not None:
            self.extracted_policy = extracted_policy    # BeautifulSoup of the privacy policy
        else:
            self.extracted_policy = self.retrieve_policy()
            print("Automatically retrieved policy URL for %s." % (website_url, ))

    # Extract the privacy policy URL from the homepage of the website.
    def retrieve_policy_url(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        policy_html = driver.page_source
        driver.close()
        soup = BeautifulSoup(policy_html, 'html.parser')

        links = soup.find_all('a')

        for item in links:
            if re.search(r"privacy", str(item.get_text()), re.IGNORECASE):
                if item.get('href')[0:4] != "http":
                    if item.get('href')[0:2] == "//":
                        return "http:" + item.get('href')
                    else:
                        return self.url.rstrip() + item.get('href')
                return item.get('href')
        return None

    # Extract the privacy policy from the URL.
    def retrieve_policy(self):
        driver = webdriver.Chrome()
        if self.policy_url is not None:
            try:
                driver.get(self.policy_url)
            except se.InvalidArgumentException:
                print("Failed " + self.policy_url)
                driver.close()
                return None
        else:
            print("Policy URL not found.")
            driver.close()
            return None
        policy_html = driver.page_source
        soup = BeautifulSoup(policy_html, 'html.parser')
        driver.close()
        return soup

if __name__== "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:p:", 
                    ["help", "curl=","purl="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print("ERROR:%s" % (str(err) )) # will print something like "option -a not recognized"
        prog_usage()
        sys.exit(1)
    #set program arguments
    controller_url=None
    ppolicy_url=None
    for o, a in opts:
        if o in ("-c", "--curl"):controller_url = a
        elif o in ("-p", "--purl"):ppolicy_url = a
        elif o in ("-h", "--help"):
            prog_usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    ## Display program usage if the user did not specify a url
    if controller_url is None and ppolicy_url is None:
        prog_usage()
        sys.exit()
    display_header()
    currentDirectory = os.getcwd()
    model_dir=join(currentDirectory,"models")

    # These two lines are for when the XML component is implemented
    #models = pmodel.Models(model_dir=model_dir)
    #print(models.models_list)

    if controller_url is not None:
        policies = multiple_policy_extraction(urls=[controller_url])

    for policy in policies:

        # Helper function
        def print_topics(model, count_vectorizer, n_top_words):
            words = count_vectorizer.get_feature_names()
            for topic_idx, topic in enumerate(model.components_):
                print("LDA:")
                print(" ".join([words[i]
                                for i in topic.argsort()[:-n_top_words - 1:-1]]))

        policy_extracted = [str(paragraph.text) for paragraph in policy.extracted_policy.find_all('p')]
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.decomposition import LatentDirichletAllocation as LDA

        for policy_paragraph in policy_extracted:
            count_vectorizer = CountVectorizer(stop_words='english')
            count_data = count_vectorizer.fit_transform(policy_paragraph.split('.'))
            # Tweak the two parameters below
            number_topics = 1
            number_words = 10
            # Create and fit the LDA model
            lda = LDA(n_components=number_topics, n_jobs=-1)
            lda.fit(count_data)
            # Print the topics found by the LDA model
            if "controls" in count_vectorizer.get_feature_names():
                print(policy_paragraph)
                print_topics(lda, count_vectorizer, number_words)
                print("\n")

    print("%s - %s - %s"%(currentDirectory, basename(__file__),model_dir))
    sys.exit()
