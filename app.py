import pymysql
from flask import Flask, render_template, flash, redirect, url_for,request,logging
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, validators, IntegerField

app = Flask(__name__)

# Config MySQL

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] =  'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pranav1212'
app.config['MYSQL_DATABASE_DB'] = 'catalog'


mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

class AddEmployee(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    desig = StringField('Designation', [validators.Length(min=1, max=50)])
    address = StringField('Address', [validators.Length(min=1, max=200)])
    phone = IntegerField('Phone')

@app.route('/addemployee', methods=['GET', 'POST'])
def addemployee():
    form = AddEmployee(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        desig = form.desig.data
        address = form.address.data
        phone = form.phone.data
        
        ##Create cursoe
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO employee(name, designation, address, phone) VALUES(%s,%s,%s,%s)", (name, desig, address, phone))
        conn.commit()
        cur.close()
        flash('Employee is added to database')
        return redirect('/')
    return render_template('addemployee.html', form = form)


@app.route('/listemployee')
def listemployee():
    conn = mysql.connect()
    #cur = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor()
    result = cur.execute("SELECT * from employee")
    employees = cur.fetchall()
    
    if result > 0:
        return render_template('listemployee.html', employees = employees)
    else:
        msg = 'No employees Found'
        return render_template('listemployee.html', msg = msg)
    cur.close()


@app.route('/deleteemployee/<string:id>')
def deleteemployee(id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("DELETE from employee where id = %s", [id])
    conn.commit()
    cur.close()
    return redirect('/listemployee')

@app.route('/searchemployee', methods=['GET','POST'])
def searchemployee():
    if request.method == "POST":
        name = request.form['employee']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT name, designation, address, phone from employee WHERE name LIKE %s OR designation LIKE %s",(name, name))
        conn.commit()
        data = cur.fetchall()
        return render_template('searchemployee.html', data = data)
    return render_template('searchemployee.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
