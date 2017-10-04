(select *
from (
    select r.rating as rating, r.helpful, r.votes
    from review r, product ptarget
    where ptarget.asin = {0} and r.product_id = ptarget.id
    order by r.rating desc, r.helpful desc
) as t
limit 5)
union all
(select *
from (
    select r.rating as rating, r.helpful, r.votes
    from review r, product ptarget
    where ptarget.asin = {0} and r.product_id = ptarget.id
    order by r.rating asc, r.helpful desc
) as t
limit 5);
