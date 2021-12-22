# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 20:19:02 2020

@author: Eugene
"""

# For Indeed

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable as EC
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
import time
import sys

# DataFrame columns for JobsDB layout
col = ['title', 'company', 'employment type', 'salary', 'description']
jobs = pd.DataFrame(columns=col)

# Headless chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-popup-blocking')
driver = webdriver.Chrome(options=chrome_options)
second_driver = webdriver.Chrome(options=chrome_options)

# General url website
url = 'https://sg.indeed.com/'

# Number of pages to crawl
pages = 2

# Number of profiles to crawl -> edit the loop condition
# number = 100

# Counter for pd
count = 0

# Troubleshoot: driver = webdriver.Chrome()
driver.get(url)

# Search keyword
inputElement = driver.find_element_by_id("text-input-what")
inputElement.send_keys('manager')
inputElement.send_keys(Keys.ENTER)

# Crawl the stated number of pages
while pages != 0:
    
# For number of profiles -> while numbers != 0:   edit the counter and next page condition  
    
    # Crawl through all profile listings 
    profiles = []
    profiles = driver.find_elements_by_class_name("jobtitle")
        
    for i in range(len(profiles)):
        test = profiles[i].get_attribute("href")
    
        # Open second driver for individual listing
        # Troubleshoot: second_driver = webdriver.Chrome()
        second_driver.get(test)

        # Get title and other info
        title = second_driver.find_element_by_class_name("jobsearch-JobInfoHeader-title-container").text
        # print(title)
        
        company = second_driver.find_element_by_class_name('jobsearch-InlineCompanyRating').text
        # print(company)
        
        salary = ""
        sub_header = second_driver.find_elements_by_class_name("jobsearch-JobMetadataHeader-iconLabel")  
        for j in sub_header:
            # print (j.text)
            if '$' in j.text:
                salary = j.text
        
        # Extract lines in job description
        lst=[]
        JD = second_driver.find_element_by_id("jobDescriptionText")
        child = JD.find_elements_by_css_selector("*")
        for k in range(len(child)):
            if (child[k].tag_name != 'ul') and (child[k].text not in lst):
                lst.append(child[k].text)
                # print (child[k].text)
        
        employment = ""
        for l in lst:
            if 'salary' == "" and 'salary' in l.lower():
                salary = l
                lst.remove(l)
            if 'job type' in l.lower():
                employment = l
                lst.remove(l)
        
        description = ','.join(lst)
        
        jobs.loc[count] = [title, company, employment, salary, description]
        count += 1
    
    # For next page
    try:
        driver.find_element_by_css_selector("[aria-label=Next]").click()
    except ElementClickInterceptedException:
        driver.find_element_by_id("popover-close-link").click()
        WebDriverWait(driver, 5).until(EC((By.CSS_SELECTOR, "[aria-label=Next]"))).click()
        
    pages -= 1
    
jobs.to_csv('data.csv', index=False)