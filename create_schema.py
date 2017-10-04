import psycopg2
import sys
from psycopg2 import errorcodes

if len(sys.argv) < 5:
    print("Por favor, insira todos os parâmetros:\n\n<host> <database> <user> <password> ")
else:

    con = psycopg2.connect(host=sys.argv[1], database=sys.argv[2],user=sys.argv[3], password=sys.argv[4])

    cur = con.cursor()
    cur.execute(open("create-tables.sql", "r").read())

    con.commit()
    con.close()