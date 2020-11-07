
## Engineering Privacy, COS 598

### Project Title : Privacy Policies: Opting in and out of private data collection post GDPR

### Project Authors

* Lucie Hutchins
* Timothy Bruce 

### Project Description

``` 
create or modify a tool for extracting opting policy from given websites in an automated manner.
This tool will be intended for use by users to save time when evaluating 
if they want to use an application or service provided by that website.

```
### Policies_scanner

```
 Coming soon
 
```
### How it works


### Usage
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

### Software and tool Requirements

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
