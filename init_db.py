import os
import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    database = "flaskapp",
    user = os.environ["DB_USERNAME"],
    password = os.environ["DB_PASSWORD"])


cur = conn.cursor()

cur.execute('CREATE TABLE productos('
            'codigo serial PRIMARY KEY,'
            'descripcion TEXT NOT NULL,'
            'precio NUMERIC(10,2) NOT NULL,'
            'stock INTEGER NOT NULL,'
            'categoria TEXT NOT NULL,'
            'marca TEXT NOT NULL,'
            'modelo TEXT NOT NULL)' 
)

conn.commit()

cur.close()
conn.close()