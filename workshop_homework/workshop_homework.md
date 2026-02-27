## Questions
Once your pipeline has run successfully, use the methods covered in the workshop to investigate the following:

- dlt Dashboard: dlt pipeline taxi_pipeline show
- dlt MCP Server: Ask the agent questions about your pipeline
- Marimo Notebook: Build visualizations and run queries

## Question 1. What is the start date and end date of the dataset?

Answer: `2009-06-01 to 2009-07-01`

## Question 2. What proportion of trips are paid with credit card?

```bash
SELECT 
    ROUND(
        100.0 * SUM(CASE WHEN LOWER(payment_type) = 'credit' THEN 1 ELSE 0 END) 
        / COUNT(*),
    2) AS credit_card_percentage
FROM trips;
```
Answer: `26.66`

## Question 3. What is the total amount of money generated in tips?

Answer: `12,126.82000000002`