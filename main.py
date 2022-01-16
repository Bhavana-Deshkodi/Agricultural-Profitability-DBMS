from unittest.mock import FILTER_DIR
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
import os
from sqlalchemy import exists
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect

with open('config.json','r') as c:
    params = json.load(c)['params']
    
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)

class User(db.Model):
    U_ID= db.Column(db.Integer,primary_key = True)
    U_NAME = db.Column(db.String,nullable = False)
    ADDRESS = db.Column(db.String,nullable = False)
    PHONE = db.Column(db.Integer,nullable = False)
    GENDER = db.Column(db.String,nullable = False)
    PASSWORD = db.Column(db.String,nullable = False)

class Stock_available(db.Model):
    S_ID= db.Column(db.Integer,primary_key = True)
    QUANTITY = db.Column(db.String,nullable = False)
    
class Crop_yield(db.Model):
    C_ID= db.Column(db.Integer,primary_key = True)
    LAND = db.Column(db.Integer,nullable = False)
    TRANSPORT = db.Column(db.Integer,nullable = False)
    C_TYPE = db.Column(db.String,nullable = False)
    


class Domestic_farming(db.Model):
    F_ID= db.Column(db.Integer,primary_key = True)
    DAIRY_FARMING = db.Column(db.Integer,nullable = False)
    POULTRY_FARMING = db.Column(db.Integer,nullable = False)
    FISHERY_FARMING = db.Column(db.Integer,nullable = False)
    C_ID = db.Column(db.Integer,ForeignKey(Crop_yield.C_ID),nullable = False)
    S_ID = db.Column(db.Integer,ForeignKey(Stock_available.S_ID),nullable = False)
    

class Annual_profitability(db.Model):
    A_ID = db.Column(db.Integer,primary_key = True)
    TOTAL_EXP = db.Column(db.Integer,nullable = False)
    SRC_OF_INCOME = db.Column(db.String,nullable = False)
    MARKETING = db.Column(db.String,nullable = False)
    F_ID = db.Column(db.String,ForeignKey(Domestic_farming.F_ID),nullable = False)
    S_ID = db.Column(db.String,ForeignKey(Stock_available.S_ID),nullable = False)
    U_ID = db.Column(db.String,ForeignKey(User.U_ID),nullable = False)
    
class Workers(db.Model):
    W_ID = db.Column(db.Integer,primary_key = True)
    W_NAME = db.Column(db.Integer,nullable = False)
    W_SALARY = db.Column(db.String,nullable = False)
    S_ID = db.Column(db.String,ForeignKey(Stock_available.S_ID),nullable = False)
    
class By_products(db.Model):
    B_ID= db.Column(db.Integer,primary_key = True)
    MANURE = db.Column(db.Integer,nullable = False)
    V_WASTE = db.Column(db.Integer,nullable = False)
    FERTILIZER = db.Column(db.Integer,nullable = False)
    S_ID = db.Column(db.Integer,ForeignKey(Stock_available.S_ID),nullable = False)
    C_ID = db.Column(db.Integer,ForeignKey(Crop_yield.C_ID),nullable = False)
    
class Expenses(db.Model):
    E_ID= db.Column(db.Integer,primary_key = True)
    TOOLS = db.Column(db.Integer,nullable = False)
    CHEM_FERTILIZERS = db.Column(db.Integer,nullable = False)
    LOAN = db.Column(db.Integer,nullable = False)
    WATER = db.Column(db.Integer,nullable = False)
    ELECTRICITY = db.Column(db.Integer,nullable =  False)
    C_ID = db.Column(db.Integer,ForeignKey(Crop_yield.C_ID),nullable = False)
    W_ID = db.Column(db.Integer,ForeignKey(Workers.W_ID),nullable = False)
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods = ['GET', 'POST'])
def login():
    if(request.method == "POST"):
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        exists = db.session.query(User.U_NAME).filter_by(
            U_NAME=uname, PASSWORD=psw).first() is not None
        if(exists):
            params["crnt_usr"] = uname
            return redirect('/details')
        else:
            return redirect('/signup')


    return render_template('login.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if(request.method == "POST"):
        try:
            name = request.form.get("name")           
            phno = request.form.get("phno")
            gender = request.form.get("gender")
            address = request.form.get("address")
            psw = request.form.get("psw")
            entry = User(U_NAME=name, ADDRESS=address, PHONE=phno,
                              GENDER=gender, PASSWORD=psw)
            params['crnt_usr'] = name
            db.session.add(entry)
            db.session.commit()
            return redirect("/")
        except:
            redirect("/signup")
    return render_template('signup.html')

app.run(debug = True)
