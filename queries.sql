--(a)

(SELECT * FROM (SELECT r.rating as rating, r.votes, r.helpful FROM review r, product_review pr WHERE pr.product_id = 21 AND r.id = pr.review_id AND r.votes <> 0 ORDER BY r.helpful DESC) AS utility_ordered ORDER BY utility_ordered.rating DESC LIMIT 5)
union all
(SELECT * FROM (SELECT r.rating as rating, r.votes, r.helpful FROM review r, product_review pr WHERE pr.product_id = 21 AND r.id = pr.review_id AND r.votes <> 0 ORDER BY r.helpful DESC) AS utility_ordered ORDER BY utility_ordered.rating ASC LIMIT 5);


--(b)

SELECT p.title, p.salesrank FROM product p, product param, (SELECT s.asin_of_similar as similar_asin FROM similars s WHERE s.product_id = $produto_id) as sim WHERE param.id = $produto_id AND p.asin = sim.similar_asin AND p.salesrank < param.salesrank;

--(c)

SELECT r.reviewdate, r.rating, AVG(r.rating) FROM review r, product_review pr WHERE pr.product_id = 21 AND r.id = pr.review_id GROUP BY r.reviewdate, r.rating ORDER BY r.reviewdate;


--(d)

select * 
from (
	select 
        row_number() over (partition by p.group_id order by p.salesrank) as r, p.*
	from (select * from product where salesrank >= 0) p ) x
where x.r <= 10;

--(e)

select revs.title, avg(revs.rating) as average from (select product_id, pp.title, rating from review r, product pp where r.helpful > 0 and pp.id = r.product_id) revs group by revs.title order by average desc limit 10;


--(f)

select cc.name, res.rating_average from (select p.category_id, avg(revs.rating) as rating_average from 
(select product_id, rating from review r where r.helpful > 0) revs 
join 
(select x.id, cp.category_id from product x, category_product cp where cp.product_id = x.id) p 
on revs.product_id = p.id group by p.category_id order by rating_average desc limit 5) res, category cc where res.category_id = cc.id;

--(g)

select * 
from (
	select 
        row_number() over (partition by p.group_id order by p.ncomments desc) as r, p.*
	from (
		select al.customer_id, al.group_id, count(al.customer_id) as ncomments from ( 
		select p.group_id, r.customer_id, r.id from product p, review r where p.id = r.product_id) al 
		group by al.customer_id, al.group_id
	) p ) x
where x.r <= 10;