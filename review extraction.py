# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:36:15 2022

@author: Bill
"""

from joblib import Parallel, delayed
import time
from textblob import TextBlob
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd

def getRdata(browser):
    
    k = browser.find_elements_by_xpath('//*[@data-hook="review"]')
    list1 =[]
    sampleData = []
    for x in k:
        list1.append(x.get_attribute('id'))
    for id in list1:
        list2 = []
        try: #this is to stop while encountering foreigner reviews with different xpath
            title = browser.find_element_by_xpath('//*[@id="customer_review-{}"]/div[2]/a[2]'.format(id)).text
            list2.append(title)
        except:
            break
        star = browser.find_element_by_xpath('//*[@id="customer_review-{}"]/div[2]/a[1]'.format(id))
        str = star.get_attribute("title")
        intRate = int(float(str.split()[0]))
        list2.append(intRate)
        
        comment = browser.find_element_by_xpath('//*[@id="customer_review-{}"]/div[4]'.format(id)).text
        list2.append(comment)
        '''
        #directly apply textblob to the comment
        list2.append(TextBlob(comment).sentiment.subjectivity)
        list2.append(TextBlob(comment).sentiment.polarity)
        blob = TextBlob(comment)
        subjtot = 0
        polartot = 0
        num = len(blob.sentences)
        #apply textblob to every sentense of the comment and count average
        for sentence in blob.sentences:
            subjtot += sentence.sentiment.subjectivity
            polartot += sentence.sentiment.polarity
        list2.append(subjtot/num)
        list2.append(polartot/num)
        '''
        sampleData.append(list2)   
    return sampleData
                  
def storeData(i):
    
    option = webdriver.ChromeOptions()
    driver_path = r'C:\Users\Bill\Desktop\HKU\7033\chrome\chromedriver.exe'
    service = ChromeService(executable_path=driver_path)
    browser = webdriver.Chrome(service=service,options = option)
    #below is the url of comment page from verified users
    browser.get('https://www.amazon.com/Oral-B-Black-Pro-1000-Rechargeable/product-reviews/B01AKGRTUM/ref=cm_cr_arp_d_viewopt_rvwer?ie=UTF8&reviewerType=avp_only_reviews&pageNumber={}'.format(i))
    time.sleep(0.01)
    result = getRdata(browser)
    return result

sampleData = Parallel(n_jobs = 6)(delayed(storeData)(i) for i in range(500))
totalData = []
for i in sampleData:
    for x in i:
        totalData.append(x)
        
dff = pd.DataFrame(totalData, columns = ('title','rating','content'))
dff.to_csv(r"C:\Users\Bill\Desktop\HKU\7036\Amazon OralBsample.csv",encoding = 'utf-8-sig')

    







    


