create table category (
	id integer primary key,
	name varchar(100),
	father_id integer
);

create table productgroup (
	id serial primary key,
	name varchar(100) unique
);

create table product (
	id integer primary key,
	asin varchar(11) unique,
	title varchar(500),
	salesrank integer
);

create table product_group (
	product_id integer,
	group_id integer,
	primary key (product_id, group_id)
);

create table customer (
	amazon_id varchar(25) primary key
);

create table review ( 
	id serial primary key,
	reviewdate date,
	rating integer,
	votes numeric,
	helpful numeric,
    product_id integer --foreign key para id do produto na tabela product
);

create table customer_review (
	customer_id varchar(25),
	review_id integer
);

create table category_product (
	category_id integer,
	product_id integer,
	primary key (category_id, product_id)
);

create table similars (
	product_id integer,
	asin_of_similar varchar(11),
	primary key (product_id, asin_of_similar)
);