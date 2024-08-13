# Drum Corps International Analysis

## Project Summary

This project aims to analyze the scores and data from Drum Corps International (DCI) competitions. The goal is to provide insights and visualizations that help understand the trends and patterns in the data.

## SQL

The project uses PostgreSQL and pgAdmin4 to store and manipulate the data. The SQL code is used to:

* Create a table to store the data
* Filter out open class corps and focus on world class corps
* Identify and correct discrepancies in the data
* Recreate the penalties column
* Analyze the data to identify trends and patterns

### SQL Code

```sql
CREATE TABLE dci_master(
	corps_name varchar(255),
	comp_date varchar(255),
	comp_location varchar(255),
	geneff DECIMAL(6,3),
	vis DECIMAL(6,3),
	mus DECIMAL(6,3),
	sub DECIMAL(6,3),
	total DECIMAL(6,3)
);

-- Filter out open class corps
SELECT * FROM dci_master WHERE corps_name NOT LIKE '%Open%';

-- Identify and correct discrepancies in the data
UPDATE dci_master
SET subtotal = total - penalties
WHERE subtotal != total;

-- Recreate the penalties column
SELECT corps_name, comp_date, comp_location, geneff, vis, mus, sub, total, total - sub AS penalties
FROM dci_master;

-- Analyze the data to identify trends and patterns
SELECT corps_name, AVG(geneff) AS avg_geneff, AVG(vis) AS avg_vis, AVG(mus) AS avg_mus, AVG(sub) AS avg_sub, AVG(total) AS avg_total
FROM dci_master
GROUP BY corps_name;
