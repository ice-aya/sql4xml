# sql4xml
A Python utility for query XML data with SQL

# Introduction
Sometime I want to create reports from structured data, that come to me in XML. For little amount of data it can be done by manual, but for more that 100k objects(rows) it may be difficult. Therefore this utility was created.

# Input
1. XML file(s) contains a data.
2. Job description JSON file, contains description of datatables ('desc' dict), list of XML files to processing ('files' dict), and list of SQL queries ('queries' dict).

or

3. Three JSON files in sql4xml.py folder, named 'desc.json', 'queries.json', and 'files.json' contains a job decription, as introduced in (2).

# Output
A semicolon (like CSV) separated file(s) whose names listed in 'queries' dict or 'queries.json', that can be processed with the text editors, spreadsheets etc.

# Example
Copy 'sql4xml.py' to 'example3' folder and:
1. run it by python3 interpreter without command line arguments, i.e.
  >sql4xml

or

2. run it by python3 interpreter with './job/data.json' command line argument, i.e.
  >sql4xml ./job/data.json

A 'dat.txt' semicolon separated text file with data from './xml/data.xml' must be created.
