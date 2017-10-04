select cc.name, res.rating_average from (select p.category_id, avg(revs.rating) as rating_average from 
(select product_id, rating from review r where r.helpful > 0) revs 
join 
(select x.id, cp.category_id from product x, category_product cp where cp.product_id = x.id) p 
on revs.product_id = p.id group by p.category_id order by rating_average desc limit 5) res, category cc where res.category_id = cc.id;
