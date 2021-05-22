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
def logincustomer():

    if request.method == 'POST' :
        Email = request.form['email']
        Password = request.form['password']
        
        cur = mysql.connection.cursor()

        query = 'SELECT Email, Password FROM cutomer \
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

            return render_template("halamanCustomer.html")
        
        con.close()

    else:
        return render_template("loginCustomer.html")

@app.route('/base.html/', methods=['GET'])
def logoutcutomer():

    return render_template("base.html")

@app.route('/loginAdmin/', methods=['GET','POST'])
def loginadmin():

    
    if request.method == 'POST' :
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

            return render_template("halamanAdmin.html")
        
        con.close()

    else:
        return render_template("loginAdmin.html")


@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cutomer WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])


if __name__ == "__main__":
    app.run(debug=True)