from flask import Flask
from flask import jsonify
from flask import request
import pandas as pd
import numpy as np
from flask_cors import CORS
from selenium import webdriver
import os
import time
from selenium.webdriver.chrome.options import Options
from pandas import ExcelWriter
import pickle

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

path = '/home/ubuntu/flaskproject/'

# X = pd.read_excel('/home/ubuntu/flaskapp/final_data_17406_30.xlsx')
# list_sentences_train = X["content"].fillna("_na_").values

embed_size = 50 # how big is each word vector
max_features = 20000 # how many unique words to use (i.e num rows in embedding vector)
maxlen = 500 # max number of words in a comment to use

# tokenizer = Tokenizer(num_words=max_features)
# tokenizer.fit_on_texts(list(list_sentences_train))

#loading
with open(path + 'tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

tags = ['startups', 'mobile', 'apps', 'social', 'gadgets', 'europe',
       'enterprise']

model = load_model(path + 'model_dropout_50_20000_500.h5')

app = Flask(__name__)
CORS(app)

def scrape_data(url):
    driver = webdriver.Chrome(os.path.join(path, 'chromedriver'), chrome_options=options)
    driver.get(url)
    heading = driver.find_element_by_class_name('article__title').text
    body = driver.find_element_by_class_name('article-content').text
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
    blog_data = (heading, body, tagsString.strip())
    driver.close()
    return blog_data

@app.route('/getTags', methods=['GET'])
def get_tags():
    print("request")
    url = request.args.get('url')
    data = scrape_data(url)
    content = data[0] + data[1]
    list_sentences_test = [content]
    list_tokenized_test = tokenizer.texts_to_sequences(list_sentences_test) 
    X_te = pad_sequences(list_tokenized_test, maxlen=maxlen)
    y_predict = model.predict([X_te], batch_size=1024, verbose=1)
    y_predict = pd.DataFrame(y_predict)
    y_predict = y_predict.apply(lambda x: [0 if y <= 0.3 else 1 for y in x])
    #   print(y_predict)
    tag_list = []
    pred_tags = list(y_predict.ix[0,:])
    for i, tag in enumerate(tags):
        if pred_tags[i] == 1:
            tag_list.append(tag)    
    tag_list = ' ,'.join(tag_list)
    return jsonify({'tags' : tag_list, 'real_tags' : data[2]})    

if __name__ == '__main__':
    app.run(debug=True)
