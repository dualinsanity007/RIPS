# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 20:19:36 2020

@author: Eugene
"""

# For JobsDB

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import sys

# DataFrame columns for JobsDB layout
col = ['title', 'company', 'location', 'description']
jobs = pd.DataFrame(columns=col)

# Headless chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-popup-blocking')
driver = webdriver.Chrome(options=chrome_options)
second_driver = webdriver.Chrome(options=chrome_options)

# General url website
url = 'https://jobsdb.com/'

# Number of pages to crawl
pages = 2

# Number of profiles to crawl -> edit the loop condition. 
# number = 100

# Counter for pd
count = 0

# JobsDB apparently has 2 different html settings when using selenium
# Function to test and run the 2 different html settings
def html_settings(test):
    second_driver = webdriver.Chrome()
    second_driver.get(test)
    global jobs
    global count
    
    try:
        title = second_driver.find_element_by_id("job-info-container").text
        # print(title)
        company = second_driver.find_element_by_class_name("company").text
        # print(company)
        location = second_driver.find_element_by_class_name("location").text
        # print(location)
        lst=[]
        JD = second_driver.find_element_by_id("job-description-container")
        child = JD.find_elements_by_css_selector("*")
        for j in range(len(child)):
            if (child[j].tag_name != 'ul') and (child[j].text not in lst):
                lst.append(child[j].text)
        description = ','.join(lst)
        # print(description)
            
    except NoSuchElementException: 
        try:
            title = second_driver.find_element_by_tag_name("h1").text
            # print(title)
            company = second_driver.find_element_by_class_name("company").text
            # print(company)
            location = second_driver.find_element_by_class_name("location").text
            # print(location)
            lst=[]
            JD = second_driver.find_element_by_class_name("summary")
            child = JD.find_elements_by_css_selector("*")
            for j in range(len(child)):
                if (child[j].tag_name != 'ul') and (child[j].text not in lst):
                    lst.append(child[j].text)
            description = ','.join(lst)
            # print(description)
        except NoSuchElementException:
            title, company, location, description = 'NA', 'NA', 'NA', 'NA'
        
    jobs.loc[count] = [title, company, location, description]
    count += 1
    second_driver.close()

# Troubleshoot: driver = webdriver.Chrome()
driver.get(url)

# Search keyword
inputElement = driver.find_element_by_id("q")
inputElement.send_keys('manager')
inputElement.send_keys(Keys.ENTER)

# Crawl the stated number of pages
while pages != 0:
    
# For number of profiles -> while numbers != 0:   edit the counter and next page condition  
    
    # Crawl through all profile listings 
    # 2 profile lists for the different html settings
    profiles = []
    profiles = driver.find_elements_by_class_name("job-item")
    profiles2 = driver.find_elements_by_class_name("jobtitle")

    if len(profiles) == 0:
        for i in range(len(profiles2)):
            test = profiles2[i].get_attribute("href")
            html_settings(test)
    else:
        for i in range(len(profiles)):
            test = profiles[i].get_attribute("href")
            html_settings(test)
            
    pages -= 1
            
jobs.to_csv('data.csv', index=False)