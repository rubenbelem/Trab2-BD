import re
from datetime import date

class Review:
    def __init__(self):
        self.date = None
        self.customer = ''
        self.rating = 0
        self.votes = 0
        self.helpful = 0

    def __str__(self):
        return "date={0} customer={1} rating={2} votes={3} helpful={4}".format(
            self.date, self.customer, self.rating, self.votes, self.helpful)

class Category:
    def __init__(self, id = 0, name = '', parent = None):
        self.id = id
        self.name = name
        self.parent = parent

    def __str__(self):
        return "name={0} parent={1}".format(self.name, self.parent)

    def __repr__(self):
        return str(self)

class Product:
    def __init__(self):
        # Inserir um produto com esses dados:
        self.id = 0
        self.asin = ''
        self.title = ''
        self.salesrank = 0

        # Tentar inserir um grupo com esse nome (é possível que ele já exista):
        self.group_name = ''

        # Adicionar essa lista a um dicionário, usando o id desse produto como chave
        # Depois que todos os produtos forem adicionados, percorrer o dicionário e adicionar as relações "similars"
        self.similars = []

        # Percorrer esse dicionário e ir adicionando categorias (as chaves neste dicionário são os id's de cada
        # categoria) (é possível que já existam):
        self.categories = []

        # Percorrer esta lista e ir adicionando as avaliações:
        self.reviews = []

def extract(field_name, line):
    return line[len(field_name):]

def read_products(filepath = "data/amazon-meta.txt", limit = None):
    with open(filepath) as file:
        while True:
            line = file.readline()
            if not line: break

            if line[:2] == "Id":
                p = Product()

                # print()
                p.id = int(line[3:])

                if limit != None and p.id > limit: break

                # print("id:", id)
                p.asin = extract("ASIN:", file.readline()).strip()
                # print("ASIN:", asin)

                disc_check = file.readline().strip()
                if disc_check == "discontinued product": continue

                p.title = extract("title: ", disc_check).replace("'", "''")
                # print("title:", title)
                p.group_name = extract("  group:", file.readline()).strip()
                # print("group:", group_str)
                p.salesrank = int(extract("  salesrank:", file.readline()))
                # print("salesrank:", salesrank)

                similar_str = extract("  similar:", file.readline()).strip()

                try:
                    p.similars = re.split("\W+", similar_str.split(' ', 1)[1].strip())
                    # print("similars:", similars)
                except IndexError as e:
                    # print("similars: None")
                    p.similars = []

                line = file.readline()
                n_categories = int(extract("  categories:", line))

                for i in range(0, n_categories):
                    category_line = extract("   |", file.readline()).strip()

                    parent = None

                    for category_str in category_line.split('|'):
                        bracket_begin = category_str.rfind('[')
                        name = category_str[:bracket_begin].replace("'", "''")
                        id = int(category_str[bracket_begin + 1 : -1])
                        p.categories.append(Category(id, name, parent))
                        parent = id

                # print("categories:")

                # for key in p.categories:
                    # cat = p.categories[key]
                    # print("\t{0} (parent={1}): {2}".format(key, cat.parent, cat.name))

                reviews_str = extract("  reviews:", file.readline()).strip()
                n_reviews = int(re.match('.*downloaded: (?P<n_reviews>\d+).*', reviews_str).group("n_reviews"))
                # print("reviews:")
                for i in range(0, n_reviews):
                    line = file.readline()

                    m = re.match("\W*(?P<date>[\w-]+)\W+cutomer:\W+(?P<customer_id>\w+)\W+rating:"
                                 "\W+(?P<rating>\d+)\W+votes:\W+(?P<votes>\d+)\W+helpful:\W+(?P<helpful>\d+).*", line)

                    review = Review()

                    review.date = m.group("date")
                    review.customer = m.group("customer_id")
                    review.rating = int(m.group("rating"))
                    review.votes = int(m.group("votes"))
                    review.helpful = int(m.group("helpful"))

                    p.reviews.append(review)
                    # print("\t" + str(review))

                yield p
