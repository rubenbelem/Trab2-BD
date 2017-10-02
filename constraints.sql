alter table category add constraint father_id references category (id);
alter table product_group add constraint product_id references product (id);
alter table product_group add constraint group_id references productgroup (id);
alter table customer_review add constraint review_id references review (id);
alter table customer_review add constraint customer_id references customer (amazon_id);
alter table category_product add constraint category_id references category (id);
alter table category_product add constraint product_id references product (id);
alter table similars add constraint product_id references product (id);
alter table similars add constraintre view_id references review (id); 

create table similars (
	product_id integer references product (id),
	asin_of_similar varchar(11) references product (asin),
	primary key (product_id, asin_of_similar)
);