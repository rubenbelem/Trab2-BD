select psim.title, psim.salesrank
from product psim, similars sim, (select id, salesrank from product where asin = {0}) ptarget
where sim.product_id = ptarget.id and sim.asin_of_similar = psim.asin and psim.salesrank < ptarget.salesrank;
