# CS267A Probabilistic database

## Dependencies
1. python==2.7.15 or python==3.4.6 (both python2 and python3 work)
2. numpy==1.15.4
3. pandas==0.23.4

These dependencies are in the `requirements.txt` file.
To install the dependencies, run
`pip install -r requirements.txt` for python2 and `pip3 install -r requirements.txt` for python3
To ensure the code runs correctly, please make sure the version of pandas is  >=0.23.4 since the older version of pandas do not have the groupby() functions and the program will fail.

## Program description
### qeval.py
qeval.py is the main logic file for the algorithm. It takes input of table files and query files in command line.

#### Sample qeval script:
qeval.py -t t1.txt -t t2.txt -t t3.txt -t t4.txt -t t5.txt -q query1.txt -q query2.txt
Please make sure there's a -t/-q before every table/query file.

### lifted_algorithm.py
The lifted algorithm.py includes the main parts of the lifted inference logic.

###  query_parser.py
This query_parser.py file includes the string parser for the queries and tables and stores them into panda dataframes.

###  utils.py
Helper function that operates on lists, dictionaries and pandas dataframes

###  file_create.py
Create your own table and query file using this function

## Extension, can also be found in readme_nba.txt.
The extension results can be obtained as follows.

1. To run the first query to find out if a player is making 20 million dollars or more, run the following script:\n
qeval.py -t t_salary.txt -q query_salary.txt


2. To run the second query to find out if a player is overpaid, run the following script:\n
qeval.py -t  t_salary.txt   -t t_overpaid.txt -q query_overpaid.txt

3. To run the third query to find the probability that a specific nba team has an overpaid player, run the following script:\n
qeval.py -t t_myteam.txt -q query_myteam.txt


4. To run the fourth query ,to find the probability a player has scored 1000 points at least once in the last decade, run the following script:\n
qeval.py -t t_thousand.txt -q query_thousand.txt

## Final Report
See the file CS_267_Project_Final_Report.pdf
