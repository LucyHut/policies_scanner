# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.common.exceptions as se
import re

'''
'''
import getopt,os,sys
from  datetime import datetime

from os.path import isdir,dirname,abspath,basename

from urllib.parse import urlparse

## domain = urlparse('http://www.example.test/foo/bar').netloc
## print(domain) # --> www.example.test

'''
Organization: The University Of Maine
Authora: Tim Bruce and Lucie N. Hutchins
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
def main():
    driver = webdriver.Chrome()

    policies = []
    url_file = open('links.txt', "r")           # Read link file
    for url in url_file.readlines():            # For every url, instantiate the Policy class with the url
        policies.append(Policy(url, driver))

    url_file.close()                            # Close the browser and file
    driver.close()

    for policyObject in policies:               # Output verification
        if policyObject.extracted_policy is not None:
            print("Extracted " + policyObject.policy_url)


# Class for storing policy information
class Policy:
    def __init__(self, website_url, selenium_driver, policy_url=None, extracted_policy=None):
        self.driver = selenium_driver           # Selenium driver for extracting information.
        self.url = website_url                  # Url of the website's main page
        if policy_url is not None:
            self.policy_url = policy_url        # URL of the privacy policy
        else:
            self.policy_url = self.retrieve_policy_url()

        if extracted_policy is not None:
            self.extracted_policy = extracted_policy    # BeautifulSoup of the privacy policy
        else:
            self.extracted_policy = self.retrieve_policy()

    # Extract the privacy policy URL from the homepage of the website.
    def retrieve_policy_url(self):
        self.driver.get(self.url)
        policy_html = self.driver.page_source
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
        if self.policy_url is not None:
            try:
                self.driver.get(self.policy_url)
            except se.InvalidArgumentException:
                print("Failed " + self.policy_url)
                return None
        else:
            return None
        policy_html = self.driver.page_source
        soup = BeautifulSoup(policy_html, 'html.parser')
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
    ##main()
    sys.exit()
