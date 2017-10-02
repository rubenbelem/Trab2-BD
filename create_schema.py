import psycopg2
from psycopg2 import errorcodes
con = psycopg2.connect(host='localhost', database='trab2bd',user='bruno',password='123mudar')

cur = con.cursor()
cur.execute('drop table category, category_product, customer, customer_review, product, product_group, product_review, productgroup, review, similars cascade')
cur.execute(open("create-tables.sql", "r").read())

con.commit()
con.close()