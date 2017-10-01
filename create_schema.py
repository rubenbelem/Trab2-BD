import psycopg2
import random

con = psycopg2.connect(host='localhost', database='trab2bd',user='bruno',password='123mudar')
cur = con.cursor()

sql = 'create table numeros (x integer, y integer)'
cur.execute(sql)

for i in range(1, 10):
    sql = "insert into numeros values({}, {})".format(random.randint(100, 200), random.randint(100, 200))
    cur.execute(sql)

con.commit()

cur.execute('select x,y, CAST(x as NUMERIC) / CAST(y as NUMERIC) from numeros')

recset = cur.fetchall()

for rec in recset:
	print(rec)

con.close()
