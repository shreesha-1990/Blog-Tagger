# Blog-Tagger
Tagging bolg articles using multilabel classification

# Data Collection - Web Scraping
Using selenium with chrome driver for scraping.
Download chrome driver appropriate for the version of chrome you are using. 
Unzip and place in same directory as python notebook.

# Model
Tried two variations of RNNs. Bidirectional LSTM and Bidirectional Gated Recurrent Unit.
Used Glove embedding with LSTM and Fasttext embedding with GRU.

# REST API - Model Deployment
The model is deployed in AWS as REST API developed using Flask.

# Front end
A front end application is developed using ReactJS that enables to load and tag Tech Crunch Blogs.
