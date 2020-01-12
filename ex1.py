from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import psycopg2
from wtforms import Form,StringField,validators,SelectField,IntegerField,FloatField
app=Flask(__name__)
app.secret_key = "12345"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:1234@localhost/inventory'
db= SQLAlchemy(app)  

class data(db.Model):
    productid=db.Column(db.String(50),primary_key=True)
    package=db.Column(db.String(50))
    value=db.Column(db.String(10))
    units=db.Column(db.String(10))
    types=db.Column(db.String(20))
    quantity=db.Column(db.Integer)
    id=db.Column(db.String(50))
    def __init__(self,productid,package,value,units,types,quantity,id):
        self.productid=productid
        self.package=package
        self.value=value
        self.units=units
        self.types=types
        self.quantity=quantity
        self.id=id

@app.route('/')
def hell():
    return render_template('home.html')

class SearchForm(Form):
    productid=StringField('MPN',[validators.Length(min=1,max=50)])

class InsertForm(Form):
    productid=StringField('MPN',[validators.Length(min=1,max=50),validators.required()])
    package=StringField('Package',[validators.Length(min=4,max=25),validators.required()])
    value=FloatField('Value',[validators.required()])
    units=SelectField( 'UNITS', choices=[('','---select---'),('FARAD', 'FARAD'), ('OHMS', 'OHMS'), ('JOULES', 'JOULES')]  )
    types=StringField('Types',[validators.Length(min=4,max=25),validators.required()])
    no=IntegerField('Quantity',[validators.required(),validators.required()])
    id=SelectField( 'UNITS', choices=[('','---select---'),('RESISTOR', 'RESISTOR'), ('CAPACITOR', 'CAPACITOR'), ('IC', 'IC')]  )

class AttribForm(Form):
    package=StringField('Package',[validators.Length(min=4,max=25),validators.required()])
    value=StringField('Value',[validators.required()])
    units=SelectField( 'UNITS', choices=[('','---select---'),('FARAD', 'FARAD'), ('OHMS', 'OHMS'), ('JOULES', 'JOULES')]  )
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
        me=data(productid,package,value,units,types,no,id)
        db.session.add(me)     
        db.session.commit()
        message='ADDED SUCCESSFULLY !!'   
    elif request.method == 'POST':
        print('')
    return render_template('insert.html',form=form,msg=message)


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/insertmenu')
def insertmenu():
    return render_template('insertmenu.html')

@app.route('/searchMPN',methods=['GET','POST'])
def smpn():
    result=[]
    message=''
    form=SearchForm(request.form)
    if request.method=='POST' and form.validate(): 
        pd=form.productid.data
        result=data.query.filter_by(productid=pd).first()
        if result:
            message='DATA AVAILABLE'
        else:
            message='MPN doesnt EXIST'         
    elif request.method == 'POST':
        print('hello world')
        
    return render_template('searchmpn.html',form=form,nd=result,msg=message)

@app.route('/srcattrib',methods=['GET','POST'])
def sattrib():
    result=[]
    message=''
    form=AttribForm(request.form)
    if request.method=='POST' and form.validate():
        pg=form.package.data
        v=form.value.data
        vl1=str(v)
        u=form.units.data
        t=form.types.data
        result=data.query.filter_by(package=pg,value=vl1,units=u,types=t).first()
        if result:
            message='DATA AVAILABLE'
        else:
            message='PRODUCT DOESNT EXIST !'
    elif request.method == 'POST':
        print('hello world')
        
    return render_template('srcattrib.html',form=form,nd=result,msg=message)
        

@app.route('/insertmpn',methods=['GET','POST'])
def impn():
    message=''
    result=[]
    form=InsertMPNForm(request.form)
    if request.method=='POST' and form.validate():
        pd=form.productid.data
        no=form.no.data
        result=data.query.filter_by(productid=pd).first()
        if result:
            sums=no+result.quantity
            result.quantity=sums
            db.session.commit()
            message='DATA ADDED SUCCESSFULLY !'
        else:
            message='MPN doesnt EXIST'       
    elif request.method == 'POST':
        hello=''   
    return render_template('insertmpn.html',form=form,msg=message)

 
if __name__=='__main__':
    app.run(debug=True)