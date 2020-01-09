from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from wtforms import Form,StringField,TextAreaField,validators
app=Flask(__name__)
app.secret_key = "12345"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory'  
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def hell():
    flash('USER ALREADY EXISTS')
    return render_template('home.html')

class SearchForm(Form):
    productid=StringField('MPN',[validators.Length(min=1,max=50)])

class InsertForm(Form):
    productid=StringField('MPN',[validators.Length(min=1,max=50)])
    package=StringField('Package',[validators.Length(min=4,max=25)])
    value=StringField('Value',[validators.Length(min=4,max=25)])
    units=StringField('Units',[validators.Length(min=4,max=25)])
    types=StringField('Types',[validators.Length(min=4,max=25)])
    no=StringField('Quantity',[validators.Length(min=4,max=25)])
    id=StringField('ID',[validators.Length(min=4,max=25)])

class AttribForm(Form):
    package=StringField('Package',[validators.Length(min=4,max=25)])
    value=StringField('Value',[validators.Length(min=4,max=25)])
    units=StringField('Units',[validators.Length(min=4,max=25)])
    types=StringField('Types',[validators.Length(min=4,max=25)])

class InsertMPNForm(Form):
    productid=StringField('MPN',[validators.Length(min=1,max=50)])
    no=StringField('Quantity',[validators.Length(min=4,max=25)])


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
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('insert.html',form=form)


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/insertmenu')
def insertmenu():
    return render_template('insertmenu.html')

@app.route('/searchMPN')
def smpn():
    form=SearchForm(request.form)
    if request.method=='POST' and form.validate():
        return render_template('searchmpn.html')
    return render_template('searchmpn.html',form=form)

@app.route('/srcattrib',methods=['GET','POST'])
def sattrib():
    form=AttribForm(request.form)
    if request.method=='POST' and form.validate():
        return render_template('srcattrib.html')
    return render_template('srcattrib.html',form=form)

@app.route('/insertmpn')
def impn():
    form=InsertMPNForm(request.form)
    if request.method=='POST' and form.validate():
        productid=form.productid.data
        no=form.no.data
        cursor = mysql.connection.cursor()
        result=cursor.execute('SELECT quantity FROM data1 WHERE productid = %s',[ productid])
        if result>0:
            flash('Updated Successfully !')
                 
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            flash('MPN Doesnt EXISTS')
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('insertmpn.html',form=form)

 


if __name__=='__main__':
    app.run(debug=True)