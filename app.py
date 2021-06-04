from flask import Flask, render_template,request,redirect
from flask_mysqldb import MySQL,MySQLdb
import datetime
from user import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "bankita"

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def base():
    return render_template("base.html")


@app.route('/register/', methods=['GET','POST'])
def register():

    if request.method == 'POST' :
        Customer_id = request.form['customer_id']
        Customer_name = request.form['customer_name']
        Address = request.form['address']
        Phone = request.form['phone']
        Email = request.form['email']
        Account_id = request.form['account_id']
        Type_account = request.form['type_account']
        Password = request.form['password']
        Date_time = datetime.datetime.now()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO account  (Account_id, Customer_id, Type) VALUES (%s,%s,%s)", (Account_id, Customer_id, Type_account))
        cur.execute("INSERT INTO customer  (Customer_id, Customer_name, Address, Phone, Email, Password) VALUES (%s,%s,%s,%s,%s,%s)", (Customer_id, Customer_name, Address, Phone, Email, Password))
        mysql.connection.commit()
        cur.close()

        return render_template("base.html")

    return render_template("register.html")

@app.route('/loginCustomer/', methods=['GET','POST'])
def logincustomer():

    if request.method == 'POST' :
        global simpanID

        
        Customer_id = request.form['customer_id']
        Password = request.form['password']
                
        cur = mysql.connection.cursor()

        query = 'SELECT Customer_id, Password FROM customer \
        where Customer_id=\'%s\' and Password=\'%s\' '
        query = query % (Customer_id, Password)
        cur.execute(query)
        mysql.connection.commit()
        rows =cur.fetchall()

        if (len(rows)) == 0:
            accept_Login = False

            return render_template("loginCustomer.html")
            
        else :
            accept_Login = True
            
            simpanID = customer(Customer_id,Password)
            simpanID.info()

            return redirect("/halamanCustomer")

        cur.close()

    else:

        return render_template("loginCustomer.html")

@app.route('/halamanCustomer', methods=['GET'])
def halamancutomer():

    return render_template("halamanCustomer.html")

@app.route('/deposit/', methods=['GET','POST'])
def deposit():

    if request.method == 'POST' :
        global simpanID
        print(simpanID)
        Transaction_type = 'Deposit'
        Account_id = request.form['account_id']
        Amount = request.form['amount']
        Data_time = datetime.datetime.now()
        Customer_id = simpanID.cus_id()
        cur = mysql.connection.cursor()

        query = "select balance from account where account_id=\'%s\'"
        query = query % (Account_id)
        cur.execute(query)
        temp = cur.fetchall()
        balance = int(temp[0][0]) + int(Amount)
        query = "update account set Balance=\'%s\' where account_id=\'%s\'"
        query = query % (balance,Account_id)
        cur.execute(query)
        mysql.connection.commit()
        cur.execute("INSERT INTO transaction  (Account_id, Customer_id ,Amount, Data_time , Transaction_type) VALUES (%s,%s,%s,%s,%s)", (Account_id, Customer_id, Amount, Data_time, Transaction_type))
        mysql.connection.commit()
    
        cur.close()
        return render_template("halamanCustomer.html")
        
    return render_template("deposit.html")

@app.route('/withdraw/', methods=['GET','POST'])
def withdraw():

    if request.method == 'POST' :
        global simpanID
        Transaction_type = 'Withdraw'
        Account_id = request.form['account_id']
        Amount = request.form['amount']
        Data_time = datetime.datetime.now()
        Customer_id = simpanID.cus_id()
        cur = mysql.connection.cursor()

        query = "select balance from account where account_id=\'%s\'"
        query = query % (Account_id)
        cur.execute(query)
        temp = cur.fetchall()
        balance = int(temp[0][0]) - int(Amount)
        query = "update account set Balance=\'%s\' where account_id=\'%s\'"
        query = query % (balance,Account_id)
        cur.execute(query)
        mysql.connection.commit()
        cur.execute("INSERT INTO transaction  (Account_id, Customer_id, Amount, Data_time , Transaction_type) VALUES (%s,%s,%s,%s,%s)", (Account_id, Customer_id, Amount, Data_time, Transaction_type))
        mysql.connection.commit()
    
        cur.close()
        return render_template("halamanCustomer.html")
        
    return render_template("withdraw.html")

@app.route('/tambahAccount/', methods=['GET','POST'])
def tambahaccount():

    if request.method == 'POST' :
        Customer_id = request.form['customer_id']
        Account_id = request.form['account_id']
        Type_account = request.form['type_account']

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO account  (Account_id, Customer_id, Type) VALUES (%s,%s,%s)", (Account_id, Customer_id, Type_account))
        mysql.connection.commit()
        cur.close()

        return render_template("halamanCustomer.html")

    return render_template("tambahAccount.html")


@app.route('/Account', methods=['GET'])
def Account():

    global simpanID
    print(simpanID)
    cur = mysql.connection.cursor()
    query = 'select * from account where Customer_id=\'%s\''
    query = query % (simpanID.cus_id())
    cur.execute(query)
    temp = cur.fetchall()

    return render_template("Account.html", info=temp)

@app.route('/Transaction', methods=['GET'])
def Transaction():

    global simpanID
    print(simpanID)
    cur = mysql.connection.cursor()
    query = 'select * from transaction where Customer_id=\'%s\''
    query = query % (simpanID.cus_id())
    cur.execute(query)
    temp = cur.fetchall()

    return render_template("Transaction.html", info=temp)

@app.route('/base.html/', methods=['GET'])
def logoutcutomer():

    return render_template("base.html")

@app.route('/loginAdmin/', methods=['GET','POST'])
def loginadmin():

    
    if request.method == 'POST' :
        global AdminID
        Username = request.form['username']
        Password = request.form['password']
        
        cur = mysql.connection.cursor()

        query = 'SELECT username, Password FROM admin \
        where username=\'%s\' and Password=\'%s\' '
        query = query % (Username, Password)
        cur.execute(query)
        mysql.connection.commit()
        rows =cur.fetchall()
        accept_Login = True
        if (len(rows)) == 0:
            accept_Login = False

        if accept_Login == False:

            return render_template("loginAdmin.html")
        elif Username == rows[0][0] and Password == rows[0][1]:
            accept_Login = True

            AdminID = admin(Username)
            AdminID.info()

            return redirect("/halamanAdmin")
        
        cur.close()

    else:
        return render_template("loginAdmin.html")

@app.route('/halamanAdmin', methods=['GET'])
def customAdmin():

    return render_template("halamanAdmin.html")


@app.route('/infoAccount', methods=['GET'])
def infoAccount():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT Account_id, Customer_id, Balance from account")
    rv = cur.fetchall()
    return render_template("infoAccount.html", info=rv)

@app.route('/infoTransaction', methods=['GET'])
def infoTransaction():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from Transaction")
    rv = cur.fetchall()
    return render_template("infoTransaction.html", info=rv)

if __name__ == "__main__":
    app.run(debug=True)