import psycopg2
import random

con = psycopg2.connect(host='localhost', database='trab2bd',user='bruno',password='123mudar')
cur = con.cursor()

cur.execute(open("create-tables.sql", "r").read())
con.commit()
con.close()
