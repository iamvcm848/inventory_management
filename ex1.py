from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import psycopg2
from wtforms import Form,StringField,TextAreaField,validators,SelectField,IntegerField,FloatField
app=Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:1234@localhost/userdata'
mysql = SQLAlchemy(app)

@app.route('/')
def hell():
    flash('USER ALREADY EXISTS')
    return render_template('home.html')

class SearchForm(Form):
    productid=StringField('MPN',[validators.Length(min=1,max=50)])

class InsertForm(Form):
    productid=StringField('MPN',[validators.Length(min=1,max=50),validators.required()])
    package=StringField('Package',[validators.Length(min=4,max=25),validators.required()])
    value=FloatField('Value',[validators.required()])
    units=StringField('Units',[validators.Length(min=3,max=5),validators.required()])
    types=StringField('Types',[validators.Length(min=4,max=25),validators.required()])
    no=IntegerField('Quantity',[validators.required(),validators.required()])
    id=StringField('ID',[validators.Length(min=4,max=25),validators.required()])

class AttribForm(Form):
    package=StringField('Package',[validators.Length(min=4,max=25),validators.required()])
    value=FloatField('Value',[validators.required()])
    units=StringField('Units',[validators.Length(min=3,max=5),validators.required()])
    types=StringField('Types',[validators.Length(min=4,max=25),validators.required()])

class InsertMPNForm(Form):
    productid=StringField('MPN',[validators.Length(min=1,max=50),validators.required()])
    no=IntegerField('Quantity',[validators.required()])



@app.route('/insert',methods=['GET','POST'])
def insert():
    form=InsertForm(request.form)
    
    if request.method=='POST' and form.validate():
        productid=form.productid.data
        package=form.package.data
        value=form.value.data
        units=form.units.data
        types=form.types.data
        no=form.no.data
        id=form.id.data
        cursor = mysql.connection.cursor()
        result=cursor.execute('SELECT * FROM data1 WHERE productid = %s',[ productid])
        if result>0:
            flash('USER ALREADY EXISTS')
            cursor.close()
        
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO  data1(productid,package,value,units,types,quantity,identifier) VALUES(%s, %s, %s,%s, %s,%s,%s)', (productid,package,value,units,types,no,id))
            mysql.connection.commit()
            flash('Registered Successfully !')
            cursor.close()
            
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('insert.html',form=form)


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/insertmenu')
def insertmenu():
    return render_template('insertmenu.html')

@app.route('/searchMPN',methods=['GET','POST'])
def smpn():
    numberdata={}
    form=SearchForm(request.form)
    if request.method=='POST' and form.validate(): 
        productid=form.productid.data
        cursor = mysql.connection.cursor()
        result=cursor.execute('SELECT * FROM data1 WHERE productid = %s ',[ productid])
        if result>0:
            numberdata=cursor.fetchone()
            mysql.connection.commit()
                 
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            flash('MPN Doesnt EXISTS')
            cursor.close()
    elif request.method == 'POST':
        print('hello world')
        
    return render_template('searchmpn.html',form=form,nd=numberdata)

@app.route('/srcattrib',methods=['GET','POST'])
def sattrib():
    numberdata={}
    form=AttribForm(request.form)
    if request.method=='POST' and form.validate():
        package=form.package.data
        value=form.value.data
        units=form.units.data
        types=form.types.data
        cursor = mysql.connection.cursor()
        result=cursor.execute('SELECT * FROM data1 WHERE package = %s and value=%s and units=%s and types=%s',[ package,value,units,types])
        if result>0:
            numberdata=cursor.fetchone()
            mysql.connection.commit()
            return render_template('srcattrib.html',form=form,nd=numberdata)
            
                 
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            flash('PRODUCT DOESNT EXISTS')
            cursor.close()
    elif request.method == 'POST':
        print('hello world')
        
    return render_template('srcattrib.html',form=form,nd=numberdata)
        

@app.route('/insertmpn',methods=['GET','POST'])
def impn():
    message=""
    form=InsertMPNForm(request.form)
    if request.method=='POST' and form.validate():
        productid=form.productid.data
        no=form.no.data
        cursor = mysql.connection.cursor()
        result=cursor.execute('SELECT * FROM data1 WHERE productid = %s',[ productid])
        
        if result>0:
            numberdata=cursor.fetchone()
            qty=numberdata["quantity"]         
            sum1=no+qty
            no=sum1
            sql = "UPDATE data1 SET quantity=%s WHERE productid=%s"
            data = (no,productid)
            message="Updated Successfully !"
            cursor.execute(sql, data)
            mysql.connection.commit()
            
            
                 
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            message="MPN DOESNT EXIST"
            
    elif request.method == 'POST':
        hello=''
    
    return render_template('insertmpn.html',form=form,msg=message)

 


if __name__=='__main__':
    app.run(debug=True)