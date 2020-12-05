from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.common.exceptions as se
import re
import pickle


# This function draws from the links.txt file for URLs, and extracts the link to the privacy policies,
#   as well as the policies themselves from these links.
def collect_and_save_data():
    driver = webdriver.Chrome()

    policies = []
    url_file = open('links.txt', "r")           # Read link file
    for url in url_file.readlines():            # For every url, instantiate the Policy class with the url
        policies.append(Policy(url, driver))

    # policies.append(Policy(url_file.readlines()[1], driver))

    url_file.close()                            # Close the browser and file
    driver.close()

    policy_data = []
    for policyObject in policies:               # Output verification
        if policyObject.extracted_policy is not None:
            policy_text = []
            for string in policyObject.extracted_policy.body.strings:
                string = string.rstrip().replace("\n", "").replace("\t", "")
                policy_text.append(string)
            print("Extracted " + policyObject.policy_url)
            policy_data.append({"policy_homepage": policyObject.url,
                                "policy_url": policyObject.policy_url,
                                "trained_key": [None for i in range(len(policy_text))],
                                "policy_text": policy_text})

    save_array_to_file(policy_data, "policy_data.p")

# This is a list of words that have been identified to appear commonly in opt-in and opt-out statements.
# This is used to filter out strings that are unlikely to contain privacy option statements.
opt_identifiers = ['you may', 'setting', 'you can', 'deactivate', 'revoke', 'chang', 'opt out', 'opt in',
                   'opt-out', 'opt-in', 'how to', 'update', 'manage', 'choice', 'opting', 'consent', 'disable',
                   'withdraw', 'permission', 'sign a', 'signed', 'rights', 'right', 'cookie', 'unsubscribe']


# This script allows a user to tag individual HTML tags from privacy policies for use in training the neural network.
# It also allows them to save this data to a serialized file.
def tag_trainning_data():
    data = get_array_from_file("policy_data.p")
    for policy in data:
        for paragraph in policy['policy_text']:
            if policy['trained_key'][policy['policy_text'].index(paragraph)] is None:
                flag = False
                for identifier in opt_identifiers:
                    if identifier in paragraph:
                        flag = identifier
                if flag is False:
                    policy['trained_key'][policy['policy_text'].index(paragraph)] = 'n'
                else:
                    print(paragraph)
                    print("Identified based on %s" % (flag, ))
                    x = input("Is this an opt statement? (y/n) (q to quit)\n")
                    if x == "y" or x == "n":
                        policy['trained_key'][policy['policy_text'].index(paragraph)] = x
                        print("Response noted")
                        print("Currently %s%s done with this policy.\n\n" %
                              ((policy['policy_text'].index(paragraph) + 1) / len(policy['policy_text']), "%"))
                    elif x == "q":
                        save_array_to_file(data, "policy_data.p")
                        return 1
        print("Policy %s completed." % (policy['policy_url'], ))
    print("Completed all data. Terminating Program")
    return 1


# Class for storing policy information. Contains methods that extract policy information as well,
#   such as the links to the policies, and the policies themselves.
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


# These functions are for saving values to and getting values from serialized files.
def save_array_to_file(array, filename):
    pickle.dump(array, open(filename, "wb"))


def get_array_from_file(filename):
    return pickle.load(open(filename, "rb"))

#collect_and_save_data()
tag_trainning_data()
