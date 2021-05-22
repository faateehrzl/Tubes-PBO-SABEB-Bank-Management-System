from flask import Flask, render_template,request,redirect,url_for
from flask_mysqldb import MySQL,MySQLdb
import bcrypt 

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
        Password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO cutomer  (Customer_id, Customer_name, Address, Phone, Email, Password) VALUES (%s,%s,%s,%s,%s,%s)", (Customer_id, Customer_name, Address, Phone, Email, Password))

        mysql.connection.commit()

        cur.close()
        
        return render_template("base.html")

    return render_template("register.html")

@app.route('/loginCustomer/', methods=['GET','POST'])
def login():

    if request.method == 'POST' :
        Email = request.form['email']
        Password = request.form['password']
        
        cur = mysql.connection.cursor()

        query = 'SELECT Email, Password FROM Cutomer \
        where Email=\'%s\' and Password=\'%s\' '
        query = query % (Email, Password)
        cur.execute(query)
        mysql.connection.commit()
        rows =cur.fetchall()
        accept_Login = True
        if (len(rows)) == 0:
            accept_Login = False

        if accept_Login == False:

            return render_template("loginCustomer.html")
        elif Email == rows[0][0] and Password == rows[0][1]:
            accept_Login = True

            return render_template("HalamanLoginCustomer.html")
        
        con.close()

    else:
        return render_template("loginCustomer.html")

@app.route('/loginAdmin/', methods=['GET'])
def loginadmin():

    return render_template("loginAdmin.html")

if __name__ == "__main__":
    app.run(debug=True)