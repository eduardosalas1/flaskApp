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

@app.route('/edit/<codigo>')
def edit_product(codigo):
    conn =get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from productos where codigo = %s',[codigo])
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html',producto = data[0])

@app.route('/delete/<string:codigo>')
def delete_product(codigo):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('delete from productos where codigo = {0}'.format(codigo))
    conn.commit()
    flash('Producto Eliminado correctamente')
    return redirect(url_for('index'))

@app.route('/update/<codigo>', methods = ['POST'])
def update_product(codigo):
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        categoria = request.form['categoria']
        marca = request.form['marca']
        modelo = request.form['modelo']
        print('UPDATE', codigo, descripcion, precio, stock)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            update productos
            set descripcion = %s,
                precio = %s,
                stock = %s,
                categoria = %s,
                marca = %s,
                modelo = %s
            where codigo = %s
        """,(descripcion,precio,stock,categoria,marca,modelo,codigo) )
        conn.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)