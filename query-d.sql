select * 
from (
	select 
        row_number() over (partition by p.group_id order by p.salesrank) as r, p.*
	from (select * from product where salesrank >= 0) p ) x
where x.r <= 10;
