select r.reviewdate, avg(r.rating)
from review r, (select id from product where asin = {0}) ptarget
where r.product_id = ptarget.id
group by r.reviewdate
order by r.reviewdate;
