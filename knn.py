#-*- coding: UTF-8 -*-   
''''' 
Created on 2016/4/23 
 
@author: Administrator 
''' 
from sklearn import neighbors  
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
   
allElectronicsData = open(r"spammer.csv","r",encoding='UTF-8')  
reader = csv.reader(allElectronicsData)  
headers =next(reader)  
  
featureList = []    
labelList = []  
#存放在两个元祖中  
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
#print "dummyY:" + str(dummyY)  

''''' 拆分训练数据与测试数据+ '''  
x_train, x_test, y_train, y_test = train_test_split(dummyX, dummyY, test_size = 0.2)


clf = neighbors.KNeighborsClassifier(algorithm='kd_tree')  

clf.fit(x_train, y_train.ravel())  
print ("clf:"+str(clf)) 

'''''测试结果的打印'''  
answer = clf.predict(dummyX)  
print(dummyX)  
print(answer)  
print(dummyY)  
print(np.mean( answer == dummyY))  
  
'''''准确率与召回率'''  
precision, recall, thresholds = precision_recall_curve(y_train, clf.predict(x_train))   
answer = clf.predict(dummyX)
print(classification_report(dummyY, answer, target_names = ['yes', 'no']))