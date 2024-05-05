# libraries and module 

from sklearn.metrics import r2_score, mean_absolute_percentage_error
from flask_cors import CORS
from flask import Flask
from flask import request
import pandas as pd
import re
from flask_pymongo import pymongo
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset
from datetime import date
import json
import numpy as np
import hashlib
from werkzeug.utils import secure_filename
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression



# flask establishment
app = Flask(__name__)
CORS(app)


# regex for email validation
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# database connection establishment

con_string = "mongodb+srv://kiran:kiran@cluster0.9bnuchr.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('example')

user_collection = pymongo.collection.Collection(db, 'collectionsexample') #(<database_name>,"<collection_name>")
print("MongoDB connected Successfully")


# routings



@app.route('/')
def welcome():
    return 'welcome'


# user signup
@app.route('/register-user', methods=['POST'])
def register_user():
    msg=''
    try:
        req_body = request.get_json(force=True)
        var=req_body['username']
        if re.fullmatch(regex,req_body['username']):
            if (not user_collection.find_one({"username":var})):
                # Hashing password using message digest5 algorithm
                password=req_body['password']
                hash_password=hashlib.md5(password.encode()).hexdigest()

                # username and passwords are inserted to mongoDB using insert_one function
                user_collection.insert_one({"username":var,"password":hash_password}) 
                msg='SignUp Successful'
            else:
                msg='User Already Exists'
        else:
            msg='User Name is not an email'
    
    except Exception as e:
        print(e)
        msg='User Already Exists'
    return {'resp': msg}


# user signin
@app.route('/signin',methods=['POST'])
def signin():
    msg=''
    try:
        data=request.get_json(force=True)
        print(data)
        var=data['username'] 
       
        # Hashing password using message digest5 algorithm
        password=data['password']
        hash_password=hashlib.md5(password.encode()).hexdigest()

        # username and password are comapred with mongoDB using find_one function
        out=user_collection.find_one({"username":var,"password":hash_password})
        u1=out.get('username')
        p1=out.get('password')
        
        msg='Login Successful'
    except Exception as e:
        print(e)
        msg='Unsuccessful'
    return {'resp': msg}


@app.route('/predict',methods=['POST'])
def prediction():
    
    data=request.get_json(force=True)

    Age=int(data['Age'])
    Sex=int(data['Sex'])
    Chest_pain_type=int(data['Chest_pain_type'])
    BP=int(data['BP'])
    Cholesterol=int(data['Cholesterol'])
    FBS_over_120=int(data['FBS_over_120'])
    EKG_results=int(data['EKG_results'])
    Max_HR=int(data['Max_HR'])
    Exercise_angina=int(data['Exercise_angina'])
    ST_depression=int(data['ST_depression'])
    Slope_of_ST=int(data['Slope_of_ST'])
    Number_of_vessels_fluro=int(data['Number_of_vessels_fluro'])
    Thallium=int(data['Thallium'])

    print(Age,Sex,end=" ")
    
    df = pd.read_csv(r'Heart_Disease_Prediction.csv')
    X=df.drop('Heart Disease',axis=1)
    y=df['Heart Disease']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    LR = LogisticRegression()
    LR.fit(X_train, y_train)
    y_pred = LR.predict(X_test)
    # pred=LR.predict([[67,0,3,115,564,0,2,160,0,1.6,2,0,7]])
    pred=LR.predict([[Age,Sex,Chest_pain_type,BP,Cholesterol,FBS_over_120,EKG_results,Max_HR,Exercise_angina,ST_depression,Slope_of_ST,Number_of_vessels_fluro,Thallium]])
    resp=pred[0]
   
    return {'resp':resp}
  

if __name__ == '__main__':
    app.run(debug=True)


