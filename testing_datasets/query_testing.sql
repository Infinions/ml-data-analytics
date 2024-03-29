SELECT invoices.*, cn.nif as company_nif, csn.nif as company_seller_nif
FROM invoices
INNER JOIN companies as cn ON invoices.company_id 
=cn.id
INNER JOIN companies as csn ON invoices.company_seller_id=csn.id
WHERE csn.nif='9999';



SELECT invoices.*, cn.nif as company_nif, csn.nif as company_seller_nif, cat.name as category
FROM invoices
INNER JOIN companies as cn ON invoices.company_id 
=cn.id
INNER JOIN companies as csn ON invoices.company_seller_id=csn.id
left join categories as cat on invoices.category_id=cat.id
WHERE cn.nif='1234';


select companies.nif, cs.date as dates, cs.value as total_value
from  companies
inner join costs as cs on companies.id=cs.company_id 
where companies.nif = '1234';