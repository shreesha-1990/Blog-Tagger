from selenium import webdriver
import os
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from pandas import ExcelWriter
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

data = pd.read_csv("techcrunch_posts.csv")
df = data.sort_values(['date'], ascending=[0])
urls = list(set(df['url']))

def process_url(url, driver):
    driver.get(url)
    tagBlock = driver.find_element_by_class_name('article__tags')
    tags = tagBlock.find_elements_by_class_name('menu__item')
    tagsString = ''
    first = True
    for tag in tags:
        if '(' not in tag.text and '-' not in tag.text and 'TC' not in tag.text and '&amp;' not in tag.text:
            if first:
                first = False
                tagsString = tag.text
            else:
                tagsString += ',' + tag.text
    return (url, tagsString)

def get_tags(urls):
    counter = 0
    driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'), chrome_options=options)
    tagData = []
    for url in urls:
        try:
            tagData.append(process_url(url, driver))
        except Exception as e:
            print(e)
            try:
                driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'), chrome_options=options)
                tagData.append(process_url(url, driver))
            except Exception as e1:
                print(e1)
                continue
        counter += 1    
        if(counter % 1 == 0):
            print('Done fetching tags for', counter,'blogs')
    driver.close()
    return tagData

start = time.time()

tags = get_tags(urls[28000:29000])

done = time.time()
elapsed = done - start
print('Total Time Taken', elapsed, 'seconds')

tags_df = pd.DataFrame(tags)
tags_df.columns = ['url', 'tags']
tags_df

df = df.drop_duplicates(subset = 'url')
final = pd.merge(df, tags_df, on='url')
final

writer = ExcelWriter('TC_final29.xlsx')
final.to_excel(writer,'Sheet1')
writer.save()
