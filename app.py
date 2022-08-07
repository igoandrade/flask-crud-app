from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a=\dfrac'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'students_db'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students;")
    data = cursor.fetchall()
    cursor.close()

    return render_template("index.html", students=data)

@app.route('/indert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data inserted succsessfully!")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s);", (name, email, phone))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('index'))
        
@app.route('/update', methods = ['POST', 'GET'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE students
        SET name=%s, email=%s, phone=%s
        WHERE id=%s;
        """, (name, email, phone, id_data))

        flash("Data Updated Successfully!")

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s;", [id_data])

    flash("Data Deleted Successfully!")

    mysql.connection.commit()

    return redirect(url_for('index'))



if __name__=="__main__":
    app.run(debug=True)
