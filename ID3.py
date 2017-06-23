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
  
allElectronicsData = open(r"spammer.csv","r",encoding='UTF-8')  
reader = csv.reader(allElectronicsData)  
headers =next(reader)  

featureList = []    
labelList = []  
for row in reader:  
    labelList.append(row[len(row)-1])  
    rowDic = {}  
    for i in range(1,len(row)-1):  
        rowDic[headers[i]] = row[i]  
    featureList.append(rowDic)  
      
vec = DictVectorizer()  
dummyX = vec.fit_transform(featureList) .toarray()   
  
lb = preprocessing.LabelBinarizer()  
dummyY = lb.fit_transform(labelList)  
 
x_train, x_test, y_train, y_test = train_test_split(dummyX, dummyY, test_size = 0.2)
 
clf = tree.DecisionTreeClassifier(criterion="entropy") #创建一个分类器，entropy决定了用ID3算法  
clf = clf.fit(x_train, y_train)  
print ("clf:"+str(clf)) 
  
with open("ID3.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

import pydotplus 
dot_data = tree.export_graphviz(clf, out_file=None) 
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("ID3.pdf")

'''''测试结果的打印'''  
answer = clf.predict(x_train)  
print(x_train)  
print(answer)  
print(y_train)  
print(np.mean( answer == y_train))  
  
'''''准确率与召回率'''  
precision, recall, thresholds = precision_recall_curve(y_train, clf.predict(x_train))  
answer = clf.predict_proba(dummyX)[:,1]  
print(classification_report(dummyY, answer, target_names = ['yes', 'no']))