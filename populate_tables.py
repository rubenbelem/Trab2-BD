from parsing import *
import psycopg2
import sys
from collections import defaultdict
import create_schema

con = psycopg2.connect(host='localhost', database='trab2bd',user='dummy',password='teste123')
cur = con.cursor()

groups = {}
categories = {}
category_product = set()
valid_asins = {}
customers = set()

def bulk_insert(cursor, sql, template, list_to_insert):
    if list_to_insert is not []:
        args_str = ','.join(str(cursor.mogrify(template, x), 'utf-8') for x in list_to_insert)
    #print(sql + args_str)
        cursor.execute(sql + args_str)

if len(sys.argv) < 1:
    print("Please pass the path to the amazon file as an argument to the script.")
else:
    #file_path = sys.argv[1]
    similars = defaultdict(list)

    product_groups = defaultdict(list)
    products_to_insert = []
    categories_to_insert = []
    reviews_to_insert = []

    counter = 1
    for product in read_products(limit=None):
        # con.rollback()
        if product.asin not in valid_asins:
            valid_asins[product.asin] = 0

        counter += 1

        if counter % 20000 == 0:
            #del products_to_insert
            bulk_insert(cur, "insert into product values ", "(%s, %s, %s, %s, %s)", products_to_insert)
            bulk_insert(cur, "insert into category values ", "(%s, %s, %s)", categories_to_insert)
            bulk_insert(cur, "insert into review (reviewdate, rating, votes, helpful, product_id, customer_id) values ", "(%s, %s, %s, %s, %s, %s)", reviews_to_insert)
            bulk_insert(cur, "insert into category_product (category_id, product_id) values", "(%s, %s)", category_product)
            products_to_insert = []
            categories_to_insert = []
            reviews_to_insert = []
            category_product = set()

        if product.group_name not in groups:
            #print(product.group_name)
            cur.execute("insert into productgroup (name) values('{}') returning id".format(product.group_name))
            groups[product.group_name] = cur.fetchone()[0]

        products_to_insert.append((product.id, str(product.asin), str(product.title), product.salesrank, groups[product.group_name]))

        #cur.execute("insert into product values({}, '{}', '{}', {}, {})".format(product.id, product.asin, product.title, product.salesrank, groups[product.group_name]))
        #con.commit()

        for sim in product.similars:
            similars[product.id].append(sim)

        product_groups[product.group_name].append(product.id)

        #cur.execute("insert into product_group (product_id, group_id) values({}, {})".format(product.id, group_id))

        for cat in product.categories:
            if (cat.parent is None):
                father_id = None
            else: father_id = cat.parent

            if cat.id not in categories:
                categories[cat.id] = cat.name
                categories_to_insert.append((cat.id, cat.name, father_id))

            category_product.add((cat.id, product.id))

        for review in product.reviews:
            reviews_to_insert.append((review.date, review.rating, review.votes, review.helpful, product.id, review.customer))
            # cur.execute("insert into review (reviewdate, rating, votes, helpful, product_id, customer_id) values('{}', {}, {}, {}, {}, '{}')".format(
            #     review.date, review.rating, review.votes, review.helpful, product.id, review.customer))
            #con.commit()

            #review_id = cur.fetchone()[0]

            #print("insert into customer (amazon_id) values('{}') where not exists(selec * from customer T where T.name='{}')".format(review.customer, review.customer))
            customers.add(str(review.customer))

            #con.commit()
            #cur.execute("insert into customer_review (customer_id, review_id) values ('{}', {})".format(review.customer, review_id))

    bulk_insert(cur, "insert into product values ", "(%s, %s, %s, %s, %s)", products_to_insert)
    bulk_insert(cur, "insert into category values ", "(%s, %s, %s)", categories_to_insert)
    bulk_insert(cur, "insert into review (reviewdate, rating, votes, helpful, product_id, customer_id) values ", "(%s, %s, %s, %s, %s, %s)", reviews_to_insert)
    bulk_insert(cur, "insert into category_product (category_id, product_id) values ", "(%s, %s)", category_product)

    for key in similars:
        for asin in similars[key]:
            if asin in valid_asins:
                cur.execute("insert into similars (product_id, asin_of_similar) values({}, '{}')".format(key, asin))

    comma = False
    values = ""
    for customer in customers:
        if comma:
            values += ", "
        else: comma = True

        values += "('" + customer + "')"

    #print(values)
    cur.execute("insert into customer (amazon_id) values " + values)
    #bulk_insert(cur, "insert into customer values ", "(%s)", customers)

    # for customer in customers:
    #     cur.execute("insert into customer (amazon_id) values('{}') on conflict do nothing".format(customer))

    # for cat_id, product_id in category_product:
    #     cp_to_insert.append()
    #     cur.execute("insert into category_product (category_id, product_id) values({}, {})".format(cat_id, product_id))
    # cur.execute("delete from similars where asin_of_similar not in (select asin from product where asin is not null)")

    # for key in product_groups:
    #     cur.execute("insert into productgroup (name) values('{}') returning id".format(key))
    #     group_id = cur.fetchone()[0]
    #
    #     for product_id in product_groups[key]:
    #         cur.execute("insert into product_group (product_id, group_id) values({}, {})".format(product_id, group_id))

    con.commit()


print('done.')
