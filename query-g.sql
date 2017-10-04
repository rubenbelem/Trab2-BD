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
