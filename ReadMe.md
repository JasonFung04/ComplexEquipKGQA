#please follow steps of this page to install environment files.

## install dependencies

### First, create environment in terminal (ComplexEquipKGQA) 
#### 1.conda create -n ComplexEquipKGQA python==3.6.13
#### 2.conda activate ComplexEquipKGQA

### Second, install packages using pip
#### 1.pip install itchat
#### 2.pip install sanic
#### 3.pip install sklearn
#### 4..pip install numpy
#### 5..pip install -U sanic-cors
#### 6.pip install sanic-openapi
#### 7.pip install fuzzywuzzy
#### 8.pip install xlrd ==1.2.0
#### 9.pip install pandas
#### 10.pip install jieba
#### 11.pip install thefuzz
#### 12.pip install pickle
#### 13.pip install numpy
#### 14.pip install flask

### Third, run python files
#### code: python local.py

## what we have done?

### 1. create a python model to process the question data and get an output.
### 2. create a api based on flask, let the python model response when giving the model a question and user id, open the api, and then the front-end website will show the reponse of the question.

## what we need to do?

### 1. try to use the front-end website to send the question to the model, and let the model receive the question, so that the model can response the question and show the response in the fron-end website. （We can try it locally，and when we succuss， we can use push function to update the code in the Github.
