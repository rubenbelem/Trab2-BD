alter table product add constraint fk_product_group foreign key(group_id) references productgroup(id);
alter table similars add constraint fk_similars_product foreign key(product_id) references product (id);
alter table similars add constraint fk_similars_review foreign key(asin_of_similar) references product (asin);
alter table category_product add constraint fk_category_category foreign key(category_id) references category (id);
alter table category_product add constraint fk_category_product foreign key(product_id) references product (id);
alter table category add constraint fk_category_father foreign key(father_id) references category (id);
alter table review add constraint fk_review_product foreign key(product_id) references product(id);
alter table review add constraint fk_review_costumer foreign key(customer_id) references customer(amazon_id);
