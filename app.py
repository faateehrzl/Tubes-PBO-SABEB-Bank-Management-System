from flask import Flask, render_template,request

from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "bankkita"

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST' :
        username = request.form['username']
        alamat = request.form['alamat']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO customer (username, alamat, phone, email, password) VALUES (%s,%s,%s,%s,%s)", (username, alamat, phone, email, password))

        mysql.connection.commit()

        cur.close()

        return "succes"

    return render_template("sign_up.html")



if __name__ == "__main__":
    app.run(debug=True)