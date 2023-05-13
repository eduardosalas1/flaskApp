import os 
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host = 'localhost',
                            database = 'flaskapp',
                            user = os.environ['DB_USERNAME'],
                            password = os.environ['DB_PASSWORD'])
    
    return conn



app.secret_key = "mysecretkey"

@app.route('/')
def index():

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from productos')
    data = cur.fetchall()
    return render_template('index.html',productos = data)

@app.route('/add_product', methods = ['POST'])
def add_product():
    conn = get_db_connection()
    cur = conn.cursor()
    description = request.form['descripcion']
    precio = request.form['precio']
    stock = request.form['stock']
    categoria = request.form['categoria']
    marca = request.form['marca']
    modelo = request.form['modelo']
    cur.execute('insert into productos (descripcion,precio,stock,categoria,marca,modelo) values (%s,%s,%s,%s,%s,%s)',(description,precio,stock,categoria,marca,modelo))
    conn.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)