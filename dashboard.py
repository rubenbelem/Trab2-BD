import psycopg2
import sys

if len(sys.argv) < 5:
    print("Por favor, insira todos os parâmetros:\n\n<host> <database> <user> <password> ")
    exit()

con = psycopg2.connect(host=sys.argv[1], database=sys.argv[2],user=sys.argv[3], password=sys.argv[4])
cur = con.cursor()

message  = ""
message += "Seja bem vindo, escolha um comando baseado em sua letra:\n\n"
message += "(a) Dado produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação;\n"
message += "(b) Dado produto, listar os produtos similares com mais vendas do que ele;\n"
message += "(c) Dado produto, mostrar a evolução diária das médias de avaliação;\n"
message += "(d) Listar os 10 produtos líderes de venda em cada grupo de produtos;\n"
message += "(e) Listar os 10 produtos com a maior média de avaliações úteis positivas por produto;\n"
message += "(f) Listar as 5 categorias de produto com a maior média de avaliações úteis positivas por produto;\n"
message += "(g) Listar os 10 clientes que mais fizeram comentários por grupo de produto;\n"
message += "(q) Sair.\n"

print(message)

while True:
    print("---")
    command = input().lower()

    if command == 'a':
        print("Forneça o ASIN do produto.")
        asin = input()

        sql = open("query-a.sql").read()
        cur.execute(sql.format("'" + asin + "'"))

        print()
        print("Nota da avaliação | Votos de 'útil' | Votos totais")
        print("---")
        for record in cur:
            print(record[0], "|", int(record[1]), "|", int(record[2]))
        print()

    elif command == 'b':
        print("Forneça o ASIN do produto.")
        asin = input()

        sql = open("query-b.sql").read()
        cur.execute(sql.format("'" + asin + "'"))

        print()
        print("Título | Ranking de vendas")
        print("---")
        for record in cur:
            print(record[0], "|", record[1])
        print()

    elif command == 'c':
        print("Forneça o ASIN do produto.")
        asin = input()

        sql = open("query-c.sql").read()
        cur.execute(sql.format("'" + asin + "'"))

        print()
        print("Data da avaliação | Média de notas")
        print("---")
        for record in cur:
            print(record[0], "|", record[1])
        print()

    elif command == 'd':
        sql = open("query-d.sql").read()
        cur.execute(sql)

        print()
        print("Ranking liderança | ID | ASIN | Título | Ranking de vendas | ID de Grupo")
        print("---")
        for record in cur:
            s = ""
            for i in range(0, 6):
                s += ("" if s == "" else " | ") + str(record[i])
            print(s)
        print()

    elif command == 'e':
        sql = open("query-e.sql").read()
        cur.execute(sql)

        print()
        print("Título | Média")
        print("---")
        for record in cur:
            s = ""
            for i in range(0, 2):
                s += ("" if s == "" else " | ") + str(record[i])
            print(s)
        print()

    elif command == 'f':
        sql = open("query-f.sql").read()
        cur.execute(sql)

        print()
        print("Nome da categoria | Média")
        print("---")
        for record in cur:
            s = ""
            for i in range(0, 2):
                s += ("" if s == "" else " | ") + str(record[i])
            print(s)
        print()

    elif command == 'g':
        sql = open("query-g.sql").read()
        cur.execute(sql)

        print()
        print("Ranking | ID do cliente | ID do grupo | Quant. de comentários")
        print("---")
        for record in cur:
            s = ""
            for i in range(0, 4):
                s += ("" if s == "" else " | ") + str(record[i])
            print(s)
        print()

    elif command == 'q':
        break

    else:
        print("O comando deve ser uma letra que corresponda a um dos comandos.")