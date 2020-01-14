from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import psycopg2
from wtforms import Form,StringField,validators,SelectField,IntegerField,FloatField,PasswordField
import xlrd
from mttkinter import mtTkinter as tk 
from tkinter import messagebox


app=Flask(__name__)
app.secret_key = "12345"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:1234@localhost/inventory'
db= SQLAlchemy(app)  




class partdata(db.Model):
    part_no=db.Column(db.String(250))
    mpn=db.Column(db.String(250),primary_key=True)
    description=db.Column(db.String(400))
    quantity=db.Column(db.Integer())
    unit_price=db.Column(db.String(100))
    total_price=db.Column(db.String(150))
    def __init__(self,part_no,mpn,description,quantity,unit_price,total_price):
        self.part_no=part_no
        self.mpn=mpn
        self.description=description
        self.quantity=quantity
        self.unit_price=unit_price
        self.total_price=total_price

class userdata(db.Model):
    username=db.Column(db.String(25),primary_key=True)
    email=db.Column(db.String(50))
    password=db.Column(db.String(50))
    name=db.Column(db.String(400))
    def __init__(self,username,email,password,name):
        self.username=username
        self.email=email
        self.password=password
        self.name=name


@app.route('/',methods=['GET','POST'])
def log():
    message=''
    print('aaaaa')
    form=LogIn(request.form)
    print('bbbbb')
    if request.method=='POST' and form.validate():
        print('cccc')
        un=form.username.data
        print('dddd')
        pw=form.password.data
        print('eeee')
        result=userdata.query.filter_by(username=un,password=pw).first()
        print('fffff')
        if result:
            print('hello world')
            message='successfull login'
            return redirect(url_for('dash'))
        else:
            print('bye world')
            message='login credentials didnt match !'
    return render_template('home.html',form=form)
    
class LogIn(Form):
    username=StringField('USERNAME',[validators.Length(min=1,max=50),validators.DataRequired()])
    password=PasswordField('PASSWORD', [validators.DataRequired()])
class RegisterUser(Form):
    name=StringField('NAME',[validators.Length(min=1,max=50)])
    email=StringField('EMAIL',[validators.Length(min=1,max=50)])
    username=StringField('USERNAME',[validators.Length(min=1,max=50)])
    password = PasswordField('PASSWORD', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('REPEAT PASSWORD')
    

class SearchForm(Form):
    mpn=StringField('MPN',[validators.Length(min=1,max=50)])

class InsertForm(Form):
    mpn=StringField('MPN',[validators.Length(min=1,max=50)])
    part_no=StringField('PART NO',[validators.Length(min=4,max=25)])
    desc=StringField('DESCRIPTION',[validators.Length(min=4,max=200)])
    no=IntegerField('QUANTITY',[validators.DataRequired()])
    up=StringField('UNIT PRICE',[validators.Length(min=2,max=10)])
    tp=StringField('TOTAL PRICE',[validators.Length(min=2,max=10)])
  

class AttribForm(Form): 
    part_no=StringField('PART NO',[validators.Length(min=4,max=25)])

class InsertMPNForm(Form):
    mpn=StringField('MPN',[validators.Length(min=1,max=50)])
    no=IntegerField('QUANTITY',[validators.DataRequired()])

class PathForm(Form):
    pathname=StringField('FILE PATH',[validators.Length(min=5,max=50)])

class PathForm1(Form):
    pathname1=StringField('FILE PATH',[validators.Length(min=5,max=50)])

class PathForm2(Form):
    pathname2=StringField('FILE PATH',[validators.Length(min=5,max=50)])
    qty=IntegerField('ENTER THE NO. OF BOMS',[validators.DataRequired()])

@app.route('/dashboard',methods=['GET','POST'])
def dash():
    return render_template('dashboard.html')   


@app.route('/register',methods=['GET','POST'])
def regd():
    form=RegisterUser(request.form)
    if request.method=='POST' and form.validate():
        temp=form.username.data
        result=userdata.query.filter_by(username=temp).first()
        if result:
            message='SORRY USERNAME ALREADY EXIST ! '
        else:
            me=userdata(form.username.data,form.email.data,form.name.data,form.password.data)
            db.session.add(me)     
            db.session.commit()
            message='SORRY USERNAME ALREADY EXIST ! '
            return redirect(url_for('log'))


    return render_template('register.html',form=form)    


@app.route('/importa',methods=['GET','POST'])
def imp():
    form=PathForm(request.form)
    if request.method=='POST' and form.validate():
        filename=form.pathname.data
        workbook=xlrd.open_workbook(filename)
        sheet=workbook.sheet_by_index(0)
        for r in range(1,sheet.nrows):
            result=partdata.query.filter_by(mpn=sheet.cell(r,1).value).first()
            if result:
                result.quantity=result.quantity+ int(sheet.cell(r,7).value)
                db.session.commit()
            else:
                me=partdata(sheet.cell(r,0).value,sheet.cell(r,1).value,sheet.cell(r,5).value,sheet.cell(r,7).value,sheet.cell(r,9).value,sheet.cell(r,10).value)
                db.session.add(me)     
                db.session.commit()
       # messagebox.showinfo('MRINQ','LCSC FILE IMPORTED SUCCESSFULLY !!') 
    elif request.method == 'POST':
        print('')        
    return render_template('importa.html',form=form)

@app.route('/importb',methods=['GET','POST'])
def imp1():
    form=PathForm1(request.form)
    if request.method=='POST' and form.validate():
        filename=form.pathname1.data
        workbook=xlrd.open_workbook(filename)
        sheet=workbook.sheet_by_index(0) 
        for r in range(1,sheet.nrows):
            result=partdata.query.filter_by(mpn=sheet.cell(r,3).value).first()
            if result:
                result.quantity=result.quantity+ int(sheet.cell(r,1).value)
                db.session.commit()
            else:
                temp=int(sheet.cell(r,1).value)
                me=partdata(sheet.cell(r,2).value,sheet.cell(r,3).value,sheet.cell(r,4).value,temp,sheet.cell(r,7).value,sheet.cell(r,8).value)
                db.session.add(me)     
                db.session.commit()
       # messagebox.showinfo('MRINQ','DIGIKEY FILE IMPORTED SUCCESSFULLY !!') 
    return render_template('importb.html',form=form)

@app.route('/exporta',methods=['GET','POST'])
def exp():
    form=PathForm2(request.form)
    if request.method=='POST' and form.validate():
        filename=form.pathname2.data
        num=form.qty.data
        workbook=xlrd.open_workbook(filename)
        sheet=workbook.sheet_by_index(0) 
        for r in range(1,sheet.nrows):
            tempno=sheet.cell(r,7).value
            result=partdata.query.filter_by(mpn=tempno).first()
            if result:
                if result.quantity==0:
                    messagebox.showinfo('MRINQ','PRODUCT HAS GOT OVER !!')      
                else:
                    temp=int(sheet.cell(r,0).value)
                    temp=temp*num
                    if (result.quantity-temp)<0:
                        print('')
                        #messagebox.showinfo('MRINQ','PRODUCT QUANTITY IS INSUFFICIENT !!') 
                    else:
                        result.quantity=result.quantity-temp
                        db.session.commit()                
      #  messagebox.showinfo('MRINQ','BOM CREATED SUCCESSFULLY !!')
    return render_template('exporta.html',form=form)

@app.route('/import',methods=['GET','POST'])
def imp2():
    return render_template('import.html')




@app.route('/insert',methods=['GET','POST'])
def insert():
    form=InsertForm(request.form)
    if request.method=='POST' and form.validate():
        mpn=form.mpn.data
        part_no=form.part_no.data
        desc=form.desc.data
        no=form.no.data
        up=form.up.data
        tp=form.tp.data       
        me=partdata(part_no,mpn,desc,no,up,tp)
        db.session.add(me)     
        db.session.commit()
       # messagebox.showinfo("MRINQ", "ADDED SUCCESSFULLY !!")   
    elif request.method == 'POST':
        print('')
    return render_template('insert.html',form=form)


@app.route('/search')  
def search():
    return render_template('search.html')

@app.route('/insertmenu')
def insertmenu():
    
    print('data added successfully')
    return render_template('insertmenu.html')

@app.route('/searchMPN',methods=['GET','POST'])
def smpn():
    result=[]   
    form=SearchForm(request.form)
    if request.method=='POST' and form.validate(): 
        pd=form.mpn.data
        result=partdata.query.filter_by(mpn=pd).first()
        if result:
            print('hello')
        else:
            print('') 
            messagebox.showinfo("Title", "MPN DOESNT EXIST")       
    elif request.method == 'POST':
        print('hello world')
        q
    return render_template('searchmpn.html',form=form,nd=result)

@app.route('/srcattrib',methods=['GET','POST'])
def sattrib():
    result=[]
    form=AttribForm(request.form)
    if request.method=='POST' and form.validate():
        pd=form.part_no.data
        result=partdata.query.filter_by(part_no=pd).first()
        if result:
            print('')
           # messagebox.showinfo("MRINQ", "DATA AVAILABLE")
        else:
            print('')
           # messagebox.showinfo("MRINQ", "PRODUCT DOESNT EXIST !")
    elif request.method == 'POST':
        print('hello world')
        
    return render_template('srcattrib.html',form=form,nd=result)

@app.route('/searchall',methods=['GET','POST'])
def srcall():
    result=[]
    result=partdata.query.filter_by().all()
    if result:
        print('')
        #messagebox.showinfo("MRINQ", "data displayed successfully !")
    else:
        print('')
       # messagebox.showinfo("MRINQ", "database empty !")
    return render_template('searchall.html',nd=result)

        

@app.route('/insertmpn',methods=['GET','POST'])
def impn():
    result=[]
    form=InsertMPNForm(request.form)
    if request.method=='POST' and form.validate():
        pd=form.mpn.data
        no=form.no.data
        result=partdata.query.filter_by(mpn=pd).first()
        if result:
            sums=no+result.quantity
            result.quantity=sums
            db.session.commit()
         #   messagebox.showinfo("MRINQ", "DATA ADDED SUCCESSFULLY !")
        else:
            print('')
           # messagebox.showinfo("MRINQ", "MPN doesnt EXIST")    
    elif request.method == 'POST':
        hello=''   
    return render_template('insertmpn.html',form=form)

 
if __name__=='__main__':
    app.run(debug=True)
    
    
