
## Engineering Privacy, COS 598: Privacy Policies: Opting in and out of private data collection post GDPR

### Project Authors

* Lucie Hutchins
* Timothy Bruce 

### Project Description

``` 
create or modify a tool for extracting opting policy from given websites in an automated manner.
This tool will be intended for use by users to save time when evaluating 
if they want to use an application or service provided by that website.

```
# Quick Links

- [Privacy Policy Extractor ](#privacy-policy-extractor)
- [Directory Structure](#directory-structure)
- [Training Models](#training-models)
- [How it works](#how-it-works)
- [Tool and Software Requirements](#tool-and-software-requirements)

### Privacy Policy Extractor

```
A Python program that extracts the Opt-in and Opt-out sections from a given Privacy Policy html document.
A sample of 40 policies of controllers ranging from healthcare to education is used as a training model.

```
### Directory Structure

There is a src sub-directory and under that directory we have: 

* a subdirectory called models that contains model xml files,
* pextractor.py  which is the main program - still work in progress 
* pmodel.py  which a module that implements the structure and  actions on training models - still work in progress

```
src/
   models/ 	
   pextractor.py	
   pmodel.py
```

### Training Models

   40 Controllers ranging from healthcare, finance, to education were manually selected by the researchers and their website’s privacy policies used in this research as the training models. These policies were selected and reviewed manually.  For each controller, the website main page was used as the point of entry to search for its privacy policy link. Next, the policy itself was reviewed and scanned, looking for Opt-in and Opt-out sections  and the different choices  of Opt-out/Opt-in the controller makes available to the user. 

The review process turned out to be more challenging than anticipated as there was no structure or standards shared between these policy documents. In addition, the section header label for Opt-in and Opt-out options varies from one controller to another making it hard to predict the beginning of an Opt-in/Opt-out section within a given document. Moreover, most of these policies did not even have an Opt-in section. Furthermore, the Opt-out choices did not follow a specific structure. For example, it would be easier if all the options available to the user to Opt-in/Opt-out a given policy are provided in structural form – say a list of choices – with a user-friendly label signaling the list and the type of choices. 

The lack of structure and standards from Privacy Policy documents makes it hard to create an automation that detects and extracts these Opt-in/Opt-out options. To that end, an xml model was created for each Privacy policy. These xml models were used as the training model for our policy-extractor tool. Each model stores two types of information:

1.	Information about the controller - a label and a link to the controller main page
2.	Information about the privacy policy – page tittle, first_paragraph, page_url,  optin, optout. 

### Model sample:

```
<?xml version="1.0" encoding="utf-8" ?>
<site name="fec.gov">
   <link id="Main">
      <label><![CDATA[FEC.gov Main Page]]></label>
      <url><![CDATA[https://www.fec.gov/]]></url>
   </link>
   <link id="Privacy Policy">
      <label><![CDATA[Privacy and security policy]]></label>
      <desc><![CDATA[Thank you for visiting the FEC website and reviewing our privacy and security statement. This webpage outlines our privacy and security policy as it applies to our site as well as third-party sites and applications that the FEC uses.]]></desc>
      <url><![CDATA[https://www.fec.gov/about/privacy-and-security-policy/]]></url>
      <optin type="default">
         <label><![CDATA[none]]></label>
      </optin>
      <optout>
       <label>How to opt out or disable cookies</label>
       <url type="cookies"><![CDATA[Cookies setting]]></url>
      </optout>
  </link>
</site>
```

### How it works

```
Usage: PROG [-h] --curl=main_page_url [--purl=policy_page_url]
 Where:
     -h To show the usage
     -c url Or --curl=url  ... required, specifies the controller main page
     -p url Or --purl=url  ... optional, specifies the direct link to the privacy policy page  
      
Usage examples :

 Example 1 -  The user does not have direct link to the privacy policy - in that case, the program
              expects to get the link of the privacy policy document from the controller main page
  Usage: 
       python3 PROG  -c https://www.nih.gov
       OR 
       python3 PROG  --curl=https://www.nih.gov


  Example 2 -  The user  provides the direct link to the privacy policy document
  Usage: 
       python3 PROG -p https://www.nih.gov/web-policies-notices
       OR 
       python3 PROG --purl=https://www.nih.gov/web-policies-notices

 Where PROG is the name of the program

 ASSUMPTIONS: 
       1) The url provided is a valid url of either the controller main site or the privacy policy document
       2) The document rendered is an html document
       3) Python3 is used and all the dependencies have been installed 
```

###  Tool and Software Requirements

#### Tool Requirements 
```
 1) The user must provide either the controller's main site url or a direct url to the privacy policy
 2) The privacy policy url takes precendence if both urls are provided
 3) The url provided is a valid url of either the controller main site or the privacy policy document
 4) The document rendered is an html document
 5) The tool must detect the Opt-in section within the privacy policy document
 6) The tool must detect the Opt-out section within the privacy policy document
 7) The tool must detect the email option within an Opt-out/Opt-in section where available
 8) The tool must detect the toll-free phone number wihtin an Opt-out/Opt-in section where available
 9) The tool must detect links within an Opt-out/Opt-in section where available
 ```
 ### Software Requirements
 ```
 Python3 is used and all the dependencies have been installed 
 
  * Python3
  * Selenium
  * chromedriver
  * bs4

```

### Useful resources
* Extraction of Opt-Out Choices from Privacy Policies using BERT

** https://canvas.eee.uci.edu/courses/14385/files/5940142/download?wrap=1

** https://github.com/google-research/bert
