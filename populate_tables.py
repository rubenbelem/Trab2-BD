from parsing import *
import psycopg2
import sys
from collections import defaultdict
import create_schema

con = psycopg2.connect(host='localhost', database='trab2bd',user='bruno',password='123mudar')
cur = con.cursor()


if len(sys.argv) < 1:
    print("Please pass the path to the amazon file as an argument to the script.")
else:
    #file_path = sys.argv[1]
    similars = defaultdict(list)

    product_groups = defaultdict(list)
    counter = 1
    for product in read_products(limit=1000):
        # con.rollback()
        if counter % 100 == 0:
            con.commit()

        counter += 1
        cur.execute("insert into product values({}, '{}', '{}', {})".format(product.id, product.asin, product.title, product.salesrank))
        #con.commit()

        for sim in product.similars:
            similars[product.id].append(sim)

        product_groups[product.group_name].append(product.id)

        #cur.execute("insert into product_group (product_id, group_id) values({}, {})".format(product.id, group_id))

        for cat in product.categories:
            if (cat.parent is None):
                father_id = 'NULL'
            else: father_id = cat.parent

            cur.execute("insert into category (id, name, father_id) values({}, '{}', {}) on conflict do nothing".format(cat.id, cat.name, father_id))

            cur.execute("insert into category_product (category_id, product_id) values({}, {}) on conflict do nothing".format(cat.id, product.id))

        for review in product.reviews:
            cur.execute("insert into review (reviewdate, rating, votes, helpful) values('{}', {}, {}, {}) returning id".format(
                review.date, review.rating, review.votes, review.helpful))
            #con.commit()

            review_id = cur.fetchone()[0]

            cur.execute("insert into product_review (product_id, review_id) values({}, {})".format(product.id, review_id))

            #print("insert into customer (amazon_id) values('{}') where not exists(selec * from customer T where T.name='{}')".format(review.customer, review.customer))
            cur.execute("insert into customer (amazon_id) values('{}') on conflict do nothing".format(review.customer))

            #con.commit()
            cur.execute("insert into customer_review (customer_id, review_id) values ('{}', {})".format(review.customer, review_id))


    for key in similars:
        for asin in similars[key]:
            cur.execute("insert into similars (product_id, asin_of_similar) values({}, '{}')".format(key, asin))

    cur.execute("delete from similars where asin_of_similar not in (select asin from product where asin is not null)")

    for key in product_groups:
        cur.execute("insert into productgroup (name) values('{}') returning id".format(key))
        group_id = cur.fetchone()[0]

        for product_id in product_groups[key]:
            cur.execute("insert into product_group (product_id, group_id) values({}, {})".format(product_id, group_id))

    con.commit()


print('done.')
