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
    def __init__(self, name = '', parent = None):
        self.name = name
        self.parent = parent

    def __str__(self):
        return "name={0} parent={1}".format(self.name, self.parent)

    def __repr__(self):
        return str(self)

def extract(field_name, line):
    return line[len(field_name):]

with open("data/amazon-meta.txt") as file:
    while True:
        line = file.readline()
        if not line: break

        if line[:2] == "Id":
            print()
            id = int(line[3:])

            if id > 10: break

            print("id:", id)
            asin = extract("ASIN:", file.readline()).strip()
            print("ASIN:", asin)

            disc_check = file.readline().strip()
            if disc_check == "discontinued product": continue

            title = extract("title: ", disc_check)
            print("title:", title)
            group_str = extract("  group:", file.readline()).strip()
            print("group:", group_str)
            salesrank = int(extract("  salesrank:", file.readline()))
            print("salesrank:", salesrank)

            similar_str = extract("  similar:", file.readline()).strip()

            try:
                similars = re.split("\W+", similar_str.split(' ', 1)[1].strip())
                print("similars:", similars)
            except IndexError as e:
                print("similars: None")
                similars = []

            n_categories = int(extract("  categories:", file.readline()))
            categories = {}
            for i in range(0, n_categories):
                category_line = extract("   |", file.readline()).strip()

                parent = None

                for category_str in category_line.split('|'):
                    split = category_str.split('[')
                    name = split[0]
                    id = int(split[1][:-1])
                    categories[id] = Category(name, parent)
                    parent = id

            print("categories:")

            for key in categories:
                cat = categories[key]
                print("\t{0} (parent={1}): {2}".format(key, cat.parent, cat.name))

            reviews_str = extract("  reviews:", file.readline()).strip()
            n_reviews = int(re.match('.*downloaded: (?P<n_reviews>\d+).*', reviews_str).group("n_reviews"))
            reviews = []
            print("reviews:")
            for i in range(0, n_reviews):
                line = file.readline()

                m = re.match("\W*(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)\W+cutomer:\W+(?P<customer_id>\w+)\W+rating:"
                             "\W+(?P<rating>\d+)\W+votes:\W+(?P<votes>\d+)\W+helpful:\W+(?P<helpful>\d+).*", line)

                review = Review()

                year = int(m.group("year"))
                month = int(m.group("month"))
                day = int(m.group("day"))
                review.date = date(year, month, day)
                review.customer = m.group("customer_id")
                review.rating = int(m.group("rating"))
                review.votes = int(m.group("votes"))
                review.helpful = int(m.group("helpful"))

                reviews.append(review)
                print("\t" + str(review))

del extract

