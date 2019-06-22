from flask import Flask,render_template,url_for,request
import pandas as  pd
import numpy as np
import scipy as sp
import pickle
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
from sklearn import model_selection
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn import svm
import sys, os

app = Flask(__name__)

url = "test.csv"
names = ['soil_type','ph','ec','oc','av_p','av_k','av_s','av_zn','av_b','av_fe','av_cu','av_mn']
dataset = pd.read_csv(url, names=names)


# create new column
dataset['class'] = dataset.soil_type.map({'Black':1,'Brown':2,'Laterite':3,'Loam':4,'Red':5,'Sandy':6,'Silt':7})

# separate array into input and output components 
array=dataset.values
X = array[1:,1:12]
Y = array[1:,12] 
Y=Y.astype('int')

# class distribution
validation_size = 0.10
seed = 7
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)


# Test options and evaluation metric
scoring = 'accuracy'

C=0.1
clf_svm = svm.SVC(kernel='linear', C=C)
clf_svm.fit(X_test, Y_test)
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		name = request.form['name']
		loc = request.form['loc']
		ph = request.form['ph']
		ec = request.form['ec']
		oc = request.form['oc']
		av_p = request.form['av_p']
		av_k = request.form['av_k']
		av_s = request.form['av_s']
		av_zn = request.form['av_zn']
		av_b = request.form['av_b']
		av_fe = request.form['av_fe']
		av_cu = request.form['av_cu']
		av_mn = request.form['av_mn']

		global clf_svm
		classes ={1:'Black',2:'Brown',3:'Laterite',4:'Loam',5:'Red',6:'Sandy',7:'Silt'}
		X_new= np.array([[float(ph),float(ec),float(oc),float(av_p),float(av_k),float(av_s),float(av_zn),float(av_b),float(av_fe),float(av_cu),float(av_mn)]])
		Y_predict = clf_svm.predict(X_new)
		return render_template('result.html',result=classes[Y_predict[0]],name=name,loc=loc)

if __name__ == '__main__':
	app.debug=True
	app.run(host='127.0.0.1')




