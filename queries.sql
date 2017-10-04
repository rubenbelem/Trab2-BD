--(a)

-- asin para teste: '0790747324'

(select *
from (
    select r.rating as rating, r.votes, r.helpful
    from review r, product ptarget
    where ptarget.asin = {0} and r.product_id = ptarget.id and r.votes <> 0
    order by r.rating desc, r.helpful desc
) as t
limit 5)
union all
(select *
from (
    select r.rating as rating, r.votes, r.helpful
    from review r, product ptarget
    where ptarget.asin = {0} and r.product_id = ptarget.id and r.votes <> 0
    order by r.rating asc, r.helpful desc
) as t
limit 5);

--(b)

-- asin para teste: 'B00000INB2'

select psim.title, psim.salesrank
from product psim, similars sim, (select id, salesrank from product where asin = {0}) ptarget
where sim.product_id = ptarget.id and sim.asin_of_similar = psim.asin and psim.salesrank < ptarget.salesrank;

--(c)

-- asin para teste: '0790747324'

select r.reviewdate, avg(r.rating)
from review r, (select id from product where asin = {0}) ptarget
where r.product_id = ptarget.id
group by r.reviewdate
order by r.reviewdate;

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