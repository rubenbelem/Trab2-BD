create schema tp2bd_ruben_timoteo;

create table tp2bd_ruben_timoteo.category (
	id integer primary key,
	name varchar(100),
	father_id integer references category (id)
);

create table tp2bd_ruben_timoteo.productgroup (
	id serial primary key,
	name varchar(100) unique
);

create table tp2bd_ruben_timoteo.product (
	id integer primary key,
	asin varchar(11) unique,
	title varchar(500),
	salesrank integer
);

create table tp2bd_ruben_timoteo.product_group (
	product_id integer references product (id),
	group_id integer references productgroup (id),
	primary key (product_id, group_id)
);

create table tp2bd_ruben_timoteo.customer (
	amazon_id varchar(25) primary key
);

create table tp2bd_ruben_timoteo.review ( 
	id serial primary key,
	date date,
	rating integer,
	votes numeric,
	helpful numeric
);

create table tp2bd_ruben_timoteo.customer_review (
	customer_id varchar(25) references customer (amazon_id),
	review_id integer references review (id)
);

create table tp2bd_ruben_timoteo.category_product (
	category_id integer references category (id),
	product_id integer references product (id),
	primary key (category_id, product_id)
);

create table tp2bd_ruben_timoteo.similars (
	product_id integer references product (id),
	asin_of_similar varchar(11) references product (asin),
	primary key (product_id, asin_of_similar)
);

create table tp2bd_ruben_timoteo.product_review (
	product_id integer references product (id),
	review_id integer references review (id),
	primary key (product_id, review_id)
);


