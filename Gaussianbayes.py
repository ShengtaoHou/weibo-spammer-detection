#-*- coding: UTF-8 -*-   
''''' 
Created on 2016/4/23 
 
@author: Administrator 
'''  
from sklearn.feature_extraction import DictVectorizer  
import csv  
from sklearn import preprocessing  
from sklearn import tree  
from sklearn.externals.six import StringIO  
import numpy as np

 
import scipy as sp  
from sklearn.metrics import precision_recall_curve  
from sklearn.metrics import classification_report   
from sklearn.model_selection import train_test_split 

from sklearn.datasets import load_iris
#from sklearn import tree
import sys
import os       
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz2.38/bin'

#from matplotlib import pyplot  
from sklearn.datasets import load_files  
from sklearn.feature_extraction.text import  CountVectorizer  
from sklearn.feature_extraction.text import  TfidfVectorizer  
from sklearn.naive_bayes import GaussianNB  


#Read in the csv File and put feature in a list of class label  
allElectronicsData = open(r"spammer.csv","r",encoding='UTF-8')  
reader = csv.reader(allElectronicsData)  
headers =next(reader)  
#print headers  
  
featureList = []    
labelList = []  
#存放在两个元祖中  
for row in reader:  
    labelList.append(row[len(row)-1])  
    rowDic = {}  
    for i in range(1,len(row)-1):  
        rowDic[headers[i]] = row[i]  
    featureList.append(rowDic)  
      
# print featureList  
# print labelList  
  
# Vector Feature  
vec = DictVectorizer()  
dummyX = vec.fit_transform(featureList) .toarray()  
# print "dummyX:",dummyX  
# print vec.get_feature_names()  
# print "labelList:"+str(labelList)  
  
lb = preprocessing.LabelBinarizer()  
dummyY = lb.fit_transform(labelList)  
#print "dummyY:" + str(dummyY)  

''''' 拆分训练数据与测试数据+ '''  
x_train, x_test, y_train, y_test = train_test_split(dummyX, dummyY, test_size = 0.2)

#using desicionTree for classfication 
clf = GaussianNB().fit(x_train, y_train)  
doc_class_predicted = clf.predict(x_test)  
      
#print(doc_class_predicted)  
#print(y)  
print(np.mean(doc_class_predicted == y_test))  
  
#准确率与召回率  
precision, recall, thresholds = precision_recall_curve(y_test, clf.predict(x_test))  
answer = clf.predict_proba(x_test)[:,1]  
report = answer > 0.5  
print(classification_report(y_test, report, target_names = ['yes', 'no'])) 