from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import psycopg2
from wtforms import Form,StringField,TextAreaField,validators,SelectField,IntegerField,FloatField
app=Flask(__name__)
app.secret_key = "12345"

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:1234@localhost/userdata'
#mysql = SQLAlchemy(app)  
 

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
    message=''
    if request.method=='POST' and form.validate():
        productid=form.productid.data
        package=form.package.data
        value=form.value.data
        units=form.units.data
        types=form.types.data
        no=form.no.data
        id=form.id.data
        try:
            connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1", port="5432",database="inventory")
            cursor = connection.cursor()           
            cursor.execute("INSERT INTO data(productid,package,value,units,type,quantity,id) VALUES (%s,%s,%s,%s,%s,%s,%s)",[productid,package,value,units,types,no,id])
            connection.commit()
            message='RECORD SUCCESSFULLY ADDED !'
        
        except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into mobile table", error)
        
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")         
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('insert.html',form=form,msg=message)


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/insertmenu')
def insertmenu():
    return render_template('insertmenu.html')

@app.route('/searchMPN',methods=['GET','POST'])
def smpn():
    message=''
    result=()
    form=SearchForm(request.form)
    if request.method=='POST' and form.validate(): 
        pd=form.productid.data
        try:
            connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1", port="5432",database="inventory")
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM data WHERE productid = %s',[pd])
            result=cursor.fetchone()
            if result:
                    
                connection.commit()      
            else:
                message='MPN doesnt exist !'
                cursor.close()
    
        except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into mobile table", error)
        
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")    
    elif request.method == 'POST':
        print('hello world')
        
    return render_template('searchmpn.html',form=form,nd=result,msg=message)

@app.route('/srcattrib',methods=['GET','POST'])
def sattrib():
    result=()
    message=''
    form=AttribForm(request.form)
    if request.method=='POST' and form.validate():
        package=form.package.data
        value=form.value.data
        vl1=str(value)
        units=form.units.data
        types=form.types.data
        try:
            connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1", port="5432",database="inventory")
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM data WHERE package = %s and value=%s and units=%s and type=%s',[package,vl1,units,types])
            result=cursor.fetchone()
            if result:  
                connection.commit()      
            else:
                message='MPN Doesnt Exist'
                cursor.close()
    
        except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into mobile table", error)
        
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed") 
    elif request.method == 'POST':
        print('hello world')
        
    return render_template('srcattrib.html',form=form,nd=result,msg=message)
        

@app.route('/insertmpn',methods=['GET','POST'])
def impn():
    message=""
    form=InsertMPNForm(request.form)
    if request.method=='POST' and form.validate():
        pd=form.productid.data
        no=form.no.data
        try:
            connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1", port="5432",database="inventory")
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM data WHERE productid = %s',[pd])
            result=cursor.fetchone()
            if result:
                res=no+result[5]
                sql = "UPDATE data SET quantity=%s WHERE productid=%s"
                data = (res,pd)
                cursor.execute(sql, data)  
                message='SUCCESSFULLY ADDED !'   
                connection.commit()      
            else:
                message='MPN doesnt exist'
                cursor.close()
    
        except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into mobile table", error)
        
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")    
            
    elif request.method == 'POST':
        hello=''   
    return render_template('insertmpn.html',form=form,msg=message)

 


if __name__=='__main__':
    app.run(debug=True)