from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.common.exceptions as se
import re


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


main()
