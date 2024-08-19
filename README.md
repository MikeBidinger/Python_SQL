# SQL conversion using Python

This repository contains the following functionalities:

-   Convert a CSV file into a SQL file
-   Convert a SQL file into CSV files

## Convert CSV to SQL

With the [csv_to_postgresql.py](csv_to_postgresql.py) Python script, a CSV file
can be selected by the file dialog to convert the CSV data to a SQL script. The
CSV file name should contain the following pattern,
`[SCHEMA_NAME].[TABLE_NAME].csv`. The resulting SQL script file will contain
the following pattern, `[SCHEMA_NAME].sql`.

> [!NOTE]
> Not all existing preserved keywords are implemented.
> Also be aware of delimiter settings.
> Adjust these in the Python script accordingly.
> The assumed CSV file structure is shown below.

```csv
Field_1;Field_2;Field_3;Field_4
1;ABC DEF;7.93;2024-08-19
```

CSV file name example: `schema_1.table_1.csv`

## Convert SQL to CSV

With the [sql_to_csv.py](sql_to_csv.py) Python script, a SQL file can be
selected by the file dialog to convert the SQL script to a CSV file for each
table within the script. The resulting CSV files will contain the following
pattern, `[SCHEMA_NAME].[TABLE_NAME].csv`.

> [!NOTE]
> The assumed SQL script structure is shown below.
> If the given SQL script is structured differently than the Python script
> needs to be adjusted accordingly.

```sql
CREATE SCHEMA IF NOT EXISTS schema_1

CREATE TABLE IF NOT EXISTS schema_1.table_1
(
    Field_1 NUMERIC,
    Field_2 CHARACTER(50),
    Field_3 FLOAT,
    Field_4 DATE,
CONSTRAINT table_1_pkey PRIMARY KEY (Field_1));

INSERT INTO schema_1.table_1(
    Field_1, Field_2, Field_3, Field_4)
    VALUES (1, 'ABC DEF', 7.93, '2024-08-19');
```

## Data example

All the examples used above refer to the data below:

| Field_1 | Field_2 | Field_3 | Field_4    |
| ------- | ------- | ------- | ---------- |
| 1       | ABC DEF | 7.93    | 2024-08-19 |
