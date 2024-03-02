
/*Total Sales, Total Profit, Profit Ratio, Avg Discount*/
select round(sum(sales), 2) as Total_Sales,
	round(sum(profit), 2) as Total_Profit,
	round(avg(profit * 1.0 / sales), 3) as Profit_Ratio,
	round(avg(discount), 3) as Avg_Discount
from orders o
left join "returns" r on o.order_id = r.order_id 
where returned is null;

-- Profit per Order

select o.order_id,
	round(sum(profit), 3) as Profit_per_Order
from orders o
left join "returns" r on o.order_id = r.order_id 
where returned is null
group by o.order_id;
order by Profit_per_Order;

-- Sales per Customer

select customer_id,
	customer_name,
	round(sum(sales), 2) AS Sales_per_Customer
FROM orders o
left join "returns" r on o.order_id = r.order_id 
where returned is null
group by customer_id, customer_name
order by Sales_per_Customer;

-- Monthly Sales by Segment

select extract(year FROM order_date)::text || '-' || LPAD(extract(month FROM order_date)::text, 2, '0') AS year_month,
	segment,
	round(sum(sales), 2) AS Monthly_Sales_by_Segment
from orders o
left join "returns" r on o.order_id = r.order_id 
where returned is null
group by year_month, segment
order by year_month, segment;

-- Monthly Sales by Product Category

select extract(year FROM order_date)::text || '-' || LPAD(extract(month FROM order_date)::text, 2, '0') AS year_month,
	category,
	round(sum(sales), 2) AS Monthly_Sales_by_Segment
from orders o
left join "returns" r on o.order_id = r.order_id 
where returned is null
GROUP BY year_month, category
ORDER BY year_month, category;

--Sales_by_region
select region,
	round(sum(sales), 2) AS Sales_per_region
FROM orders o
left join "returns" r on o.order_id = r.order_id
where returned is null
group by region;

-- Sales by Product Category over the time

select
	category,
	round(sum(sales), 2) AS Monthly_Sales_by_Segment
from orders o
left join "returns" r on o.order_id = r.order_id 
where returned is null
group by category
order by category;

