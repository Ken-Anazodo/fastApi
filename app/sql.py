"""SQL QUERIES AND STATEMENTS"""

"""
The logical order of execution in SQL is different from the order in which you write the query.
 
Order of Writing vs. Order of Execution:
How you write it: SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY
How the database executes it: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY 

Step-by-Step Breakdown (The Execution Flow):
 
1. FROM (and JOIN and ON) What it does: 
Gathers all the raw data from the specified tables. 
How to think of it: Unpacking all the filing cabinets into one massive, messy pile of papers. 

2. WHERE What it does: Filters individual rows based on specific conditions. 
How to think of it: Going through the pile and throwing away any rows you do not care about before doing any math. (This is why you cannot use aggregate functions like SUM() here—the database hasn't grouped or added anything up yet).

3. GROUP BY What it does: Collapses individual rows into summary buckets or groups.
How to think of it: Sorting the remaining papers into separate labeled folders (e.g., grouping all sales by "Region"). 

4. HAVING What it does: Filters the newly created groups based on aggregate results.
How to think of it: Looking at your labeled folders and throwing away entire folders if their combined total doesn't meet your goal. It is a WHERE clause, but for groups. 

5. SELECT What it does: Picks which columns, math calculations, or aliases to display.
How to think of it: Deciding what information to print out on a clean sheet of paper for the final report. This is where column aliases are officially born. 

6. DISTINCT - Removes duplicate rows from the selected output.

7. ORDER BY What it does: Sorts the final output (ascending or descending).
How to think of it: Arranging your final printed report alphabetically or numerically so it is easy to read

8. LIMIT / OFFSET - Trims the final list to a specific number of rows.


"""


#+==================================================================================    =========================================================================================================================================

"""TO RETRIEVE DATA FROM A TABLE, YOU CAN USE THE SELECT STATEMENT. THE BASIC SYNTAX FOR A SELECT STATEMENT IS AS FOLLOWS:"""

"""To select every column from a table, you can use the following syntax:"""       
# SELECT * FROM table_name;

"""To select specific columns from a table, you can use the following syntax:"""
# SELECT column1, column2 FROM table_name;

"""To filter results based on a condition, you can use the WHERE clause:"""
# SELECT * FROM table_name WHERE condition (e.g., column1 = value, column2 > value, column3 >= value, column4 LIKE value, etc.);

"""To use logical operators to combine multiple conditions, you can use AND, OR, and NOT:"""
# SELECT * FROM table_name WHERE condition1 AND condition2;
#Ex: SELECT * FROM product WHERE price = 30 AND inventory > 30;

# SELECT * FROM table_name WHERE condition1 OR condition2;
#Ex: SELECT * FROM product WHERE price = 50 OR price > 80;

# SELECT * FROM table_name WHERE NOT condition;
#Ex: SELECT * FROM product WHERE NOT price = 30;

"""To retrieve products with id 1, 2 and 3, you can use the OR operator or the IN operator:"""
#Ex: SELECT * FROM product WHERE id = 1 OR id = 2 OR id = 3;
#Ex: SELECT * FROM product WHERE id IN (1, 2, 3); 

"""To rename a column in the result set, you can use the AS keyword:"""
# SELECT column1 AS new_column1, column2 AS new_column2 FROM table_name;


"""Using LIKE operator to filter results based on a pattern:"""
# SELECT * FROM table_name WHERE column LIKE pattern; #The pattern can include wildcards such as % (matches any sequence of characters. before a text it signals randomness or random character and after it signals the end and then randomness or random character) and _ (matches any single character).
#Ex: SELECT * FROM product WHERE name LIKE '%phone%'; #This will return all products whose name contains the word phone anywhere in the name.
#EX: SELECT * FROM product WHERE name LIKE 'A%'; #This will return all products whose name starts with A.
#Ex: SELECT * FROM product WHERE name LIKE '%phone'; #This will return all products whose name ends with phone.
#Ex: SELECT * FROM product WHERE name LIKE '_phone'; #This will return all products whose name has exactly 6 characters and ends with phone. The first character


"""Using NOT LIKE operator to filter results based on a pattern:"""
# SELECT * FROM table_name WHERE column NOT LIKE pattern; #This will return all products whose name does not contain the word in the pattern anywhere in the name.
#Ex: SELECT * FROM product WHERE name NOT LIKE '%phone%'; #This will return all products whose name does not contain the word phone anywhere in the name.

"""Using orders to sort results:"""
# SELECT * FROM table_name ORDER BY column1 ASC, column2 DESC; #This will sort the results by column1 in ascending order and then by column2 in descending order.

"""Using LIMIT to restrict the number of results returned:"""
# SELECT * FROM table_name LIMIT number_of_rows; #This will return only the specified number of rows from the result set.
#Ex: SELECT * FROM product LIMIT 10; #This will return only the first 10 rows from the result set.

"""Using OFFSET to skip a specified number of rows before starting to return rows from the result set:"""
# SELECT * FROM table_name LIMIT number_of_rows OFFSET number_of_rows_to_skip; #This will return the specified number of rows from the result set, starting after the specified number of rows to skip.
#Ex: SELECT * FROM product LIMIT 10 OFFSET 20; #This will return 10 rows from the result set, starting after skipping the first 20 rows.

"""Using WHERE clause with ORDER BY and LIMIT to filter, sort, and restrict results:"""
# SELECT * FROM table_name WHERE condition ORDER BY column1 ASC, column2 DESC LIMIT number_of_rows; #This will return the specified number of rows from the result set that meet the condition, sorted by column1 in ascending order and then by column2 in descending order.
#Ex: SELECT * FROM product WHERE price > 50 ORDER BY price DESC LIMIT 5; #This will return the top 5 most expensive products that have a price greater than 50, sorted by price in descending order.

"""Using Offset with WHERE clause to skip a specified number of rows that meet the condition before starting to return rows from the result set:"""
# SELECT * FROM table_name WHERE condition LIMIT number_of_rows OFFSET number_of_rows_to_skip;
#Ex: SELECT * FROM product WHERE price > 50 LIMIT 5 OFFSET 10; #This will return 5 rows from the result set that have a price greater than 50, offset to determine how many item to skip before displaying the remaining items

"""Using JOIN to retrieve data from multiple tables based on a related column between them:"""
# SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.column = t2.column; #This will join table1 and table2 on the specified column and return all rows from both tables where the join condition is met.

"""Using LEFT JOIN to retrieve all rows from the left table and matching rows from the right table:"""
#SELECT posts.id, COUNT(votes.post_id) FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id; #Note: The LEFT JOIN returns all rows from the left table (posts) and the matching rows from the right table (votes). If there is no match, the result is NULL on the right side. The COUNT function counts the number of votes for each post, and the GROUP BY clause groups the results by post id. if COUNT has * as an argument, it counts all rows, including NULLs as 1 in the result. If COUNT has a specific column as an argument, it counts only non-NULL values in that column.
#SELECT posts.*, COUNT(votes.post_id) as vote_count FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id; #posts.* means select all columns from the posts table. This will return all columns from the posts table and the count of votes for each post, even if a post has no votes. The result will include posts with zero votes, and the vote_count for those posts will be 0.
#SELECT posts.*, COUNT(votes.post_id) as vote_count FROM posts LEFT JOIN votes ON posts.id = votes.post_id WHERE posts.id = 1 GROUP BY posts.id; #This will return all columns from the posts table and the count of votes for the post with id 1, even if the post has no votes. 

"""Using RIGHT JOIN to retrieve all rows from the right table and matching rows from the left table:"""
#SELECT posts.id, COUNT(votes.post_id) FROM posts RIGHT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id; #Note: The RIGHT JOIN returns all rows from the right table (votes) and the matching rows from the left table (posts). If there is no match, the result is NULL on the left side. The COUNT function counts the number of votes for each post, and the GROUP BY clause groups the results by post id. if COUNT has * as an argument, it counts all rows, including NULLs as 1 in the result. If COUNT has a specific column as an argument, it counts only non-NULL values in that column.

"""Using DISTINCT to retrieve unique values from a column:"""
# SELECT DISTINCT column1 FROM table_name; #This will return only the unique values from column1, removing any duplicates.
#Ex: SELECT DISTINCT category FROM product; #This will return all unique categories from the product table.

"""Using COUNT to count the number of rows that meet a condition:"""
# SELECT COUNT(*) FROM table_name; #This will return the total number of rows in the table including those with NULL values.
# SELECT COUNT(column1) FROM table_name; #This will return the number of non-NULL values in column1.
#Ex: SELECT COUNT(*) FROM product; #This will return the total number of products in the product table including those with NULL values.
#Ex: SELECT COUNT(*) FROM product WHERE price > 100; #This will return the number of products with a price greater than 100.

"""Using GROUP BY to group rows by one or more columns:"""
# SELECT column1, COUNT(*) FROM table_name GROUP BY column1; #This will group the rows by column1 and return the count of rows in each group.
#Ex: SELECT category, COUNT(*) FROM product GROUP BY category; #This will return the category and the number of products in each category.

"""Using HAVING to filter groups based on a condition:"""
# SELECT column1, COUNT(*) FROM table_name GROUP BY column1 HAVING COUNT(*) > value; #This will group the rows by column1 and return only the groups where the count of rows is greater than the specified value.
#Ex: SELECT category, COUNT(*) FROM product GROUP BY category HAVING COUNT(*) > 5; #This will return the category and the number of products in each category, but only for categories that have more than 5 products.

"""Using aggregate functions like SUM, AVG, MIN, MAX:"""
# SELECT SUM(column1) FROM table_name; #This will return the sum of all values in column1.
# SELECT AVG(column1) FROM table_name; #This will return the average of all values in column1.
# SELECT MIN(column1) FROM table_name; #This will return the minimum value in column1.
# SELECT MAX(column1) FROM table_name; #This will return the maximum value in"""

#+==================================================================================    ================================================================================

"""TO INSERT DATA INTO A TABLE, YOU CAN USE THE INSERT INTO STATEMENT. THE BASIC SYNTAX FOR AN INSERT INTO STATEMENT IS AS FOLLOWS:"""
# INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...); #This will insert a new row into the table with the specified values for each column. The order of the columns in the column list must match the order of the values in the value list.
#Ex: INSERT INTO product (name, price, inventory) VALUES ('iPhone 13', 999.99, 50); #This will insert a new row into the product table with the name 'iPhone 13', price 999.99, and inventory 50.

"""To INSERT MULTIPLE ROWS INTO A TABLE, YOU CAN USE THE INSERT INTO STATEMENT WITH MULTIPLE VALUE LISTS:"""  
# INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...), (value1, value2, value3, ...), ...; #This will insert multiple new rows into the table with the specified values for each column. Each set of values in parentheses represents a new row to be inserted.
#Ex: INSERT INTO product (name, price, inventory) VALUES ('iPhone 13', 999.99, 50), ('Samsung Galaxy S21', 799.99, 100), ('Google Pixel 6', 599.99, 75); #This will insert three new rows into the product table with the specified values for each column. 

"""Using returning clause to return the inserted row(s) after the insert operation:"""
# INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...) RETURNING *; #This will insert a new row into the table and return the inserted row(s) with all columns.
#Ex: INSERT INTO product (name, price, inventory) VALUES ('iPhone 13', 999.99, 50) RETURNING *; #This will insert a new row into the product table with the name 'iPhone 13', price 999.99, and inventory 50, and return the inserted row with all columns.
#Ex: INSERT INTO product (name, price, inventory) VALUES ('iPhone 13', 999.99, 50), ('Samsung Galaxy S21', 799.99, 100), ('Google Pixel 6', 599.99, 75) RETURNING name, price, inventory; #This will insert three new rows into the product table with the specified values for each column, and return the name, price, and inventory of the inserted rows.


#+==================================================================================    ====================================================================================================================================================================

"""TO DELETE DATA FROM A TABLE, YOU CAN USE THE DELETE STATEMENT. THE BASIC SYNTAX FOR A DELETE STATEMENT IS AS FOLLOWS:"""
# DELETE FROM table_name WHERE condition; #This will delete rows from the table that meet the specified condition. If you omit the WHERE clause, all rows from the table will be deleted.
#Ex: DELETE FROM product WHERE id = 1; #This will delete the row from the product table where the id is equal to 1.
#Ex: DELETE FROM product WHERE price < 100; #This will delete all products from the product table that have a price less than 100.

#+==================================================================================    =====================================================================================================================================================================
"""TO UPDATE DATA IN A TABLE, YOU CAN USE THE UPDATE STATEMENT. THE BASIC SYNTAX FOR AN UPDATE STATEMENT IS AS FOLLOWS:"""
# UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; #This will update the specified columns with the new values for rows that meet the specified condition. If you omit the WHERE clause, all rows in the table will be updated.
#Ex: UPDATE product SET price = 899.99 WHERE id = 1; #This will update the price of the product with id 1 to 899.99.
#Ex: UPDATE product SET inventory = inventory - 10 WHERE price > 500; #This will decrease the inventory of all products with a price greater than 500 by 10.

#+==================================================================================    =====================================================================================================================================================================

"""TO CREATE A TABLE IN SQL, YOU CAN USE THE CREATE TABLE STATEMENT. THE BASIC SYNTAX FOR A CREATE TABLE STATEMENT IS AS FOLLOWS:"""

"""To create a table in SQL, you can use the following syntax:"""
# CREATE TABLE table_name (
#     column1 datatype PRIMARY KEY, #This will set column1 as the primary key of the table, which means that it will uniquely identify each row in the table and cannot contain NULL values.
#     column2 datatype NOT NULL, #This will set column2 as a NOT NULL column, which means that it cannot contain NULL values.
#     column3 datatype UNIQUE, #This will set column3 as a UNIQUE column, which means that it cannot contain duplicate values.
#     ...
# ); 


"""TO DELETE A TABLE IN SQL"""
# DROP TABLE table_name; #This will delete the table and all its data from the database.

"""TO DELETE ALL ROWS IN A TABLE"""
# DELETE FROM table_name; #This will delete all rows from the table, but the table structure will remain intact.



