from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
# import json
import requests
app = Flask(__name__)

bloodgroups=['O Positive','A Positive','B Positive','AB Positive','O Negative','A Negative','B Negative','AB Negative']

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bnz17181;PWD=Tj5kCYGEKITBhBaT",'','')
print("connected")

@app.route('/registration')
def home():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    x = [x for x in request.form.values()]
    print(x)
    name=x[0]
    email=x[1]
    phone=x[2]
    city=x[3]
    infect=x[4]
    blood=x[5]
    password=x[6]
    sql = "SELECT * FROM plasmauser WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('register.html', pred="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO  plasmauser VALUES (?, ?, ?, ?, ?, ?, ?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, phone)
        ibm_db.bind_param(prep_stmt, 4, city)
        ibm_db.bind_param(prep_stmt, 5, infect)
        ibm_db.bind_param(prep_stmt, 6, blood)
        ibm_db.bind_param(prep_stmt, 7, password)
        ibm_db.execute(prep_stmt)
        return render_template('login.html', pred="Registration Successful, please login using your details")
       
           
        

@app.route('/')    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/loginpage',methods=['POST'])
def loginpage():
    user = request.form['user']
    passw = request.form['passw']
    sql = "SELECT * FROM plasmauser WHERE email =? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,user)
    ibm_db.bind_param(stmt,2,passw)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(user,passw)
    if account:
            return redirect(url_for('stats'))
    else:
        return render_template('login.html', pred="Login unsuccessful. Incorrect username / password !") 
      
        
@app.route('/stats')
def stats():

    sql ='SELECT COUNT(*) FROM plasmauser'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    totaldata = ibm_db.fetch_assoc(stmt)
    count=[]
    for i in bloodgroups:
        sql ='SELECT COUNT(*) FROM plasmauser where blood=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,i)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)
        print(data)
        print(data['1'])
        count.append(data['1'])
        print(count)
        print(i)

    #return render_template('stats.html',b=3,b1=2,b2=3,b3=4,b4=5,b5=6,b6=6,b7=5,b8=5)

       
    return render_template('stats.html',b=totaldata['1'],b1=count[0],b2=count[1],b3=count[2],b4=count[3],b5=count[4],b6=count[5],b7=count[6],b8=count[7])

@app.route('/requester')     
def requester():
    return render_template('request.html')


@app.route('/requested',methods=['POST'])
def requested():
    bloodgrp = request.form['bloodgrp']
    address = request.form['address']
    print(address)
    sql = "SELECT * FROM plasmauser WHERE blood=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,bloodgrp)
    ibm_db.execute(stmt)
    data = ibm_db.fetch_assoc(stmt)
    msg = "Need Plasma of your blood group for: "+address
    while data != False:
        print ("The Phone is : ", data["PHONE"])
        url="https://www.fast2sms.com/dev/bulk?authorization=7MVEax6qnutB129z0QIGbhypZgmrPDNH3FdsJj48c5ReWvKSCipv5m1C0IxLWSqXKGtBesyrk7dFl3Vn&sender_id=FSTSMS&message="+msg+"&language=english&route=p&numbers="+str(data["PHONE"])
        result=requests.request("GET",url)
        print(result)
        data = ibm_db.fetch_assoc(stmt)
    return render_template('request.html', pred="Your request is sent to the concerned people.")
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)

