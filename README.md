# CS267A Probabilistic database

## Dependencies
1. python==2.7.15
2. numpy==1.15.4
3. pandas==0.23.4

These dependencies are in the `requirements.txt` file.
To install the dependencies, run
`pip install -r requirements.txt` for python2.
To ensure the code runs correctly, please run in python 2.7.15 and not in python 3. We noticed that earlier versions of panda do not have the groupby functions, so the panda version must be >=0.23.4.

## qeval.py
qeval.py is the main logic file for the algorithm.

##Sample qeval script:
qeval.py -t t1.txt -t t2.txt -t t3.txt -t t4.txt -t t5.txt -q query1.txt

## lifted_algorithm.py and query_parser.py
The lifted algorithm.py includes the main parts of the lifted inference logic.
This query_parser.py file includes the string parser for the queries and tables and stores them into panda dataframes.
Both these files are called in qeval.py.



## Extension, can also be found in readme_nba.txt.
The extension results can be obtained as follows.
// 1. To run the first query to find out if a player is making 20 million dollars or more, run the following script.
// required files t_salary.txt query_salary.txt	
qeval.py -t t_salary.txt -q query_salary.txt	


// 2. To run the second query to find out if a player is overpaid, run the following script.
// required files t_salary.txt ,t_overpaid.txt ,query_overpaid.txt
qeval.py -t  t_salary.txt   -t t_overpaid.txt -q query_overpaid.txt

// 3. To run the third query to find the probability that a specific nba team has an overpaid player, run the following script.
// required files t_myteam.txt, query_myteam.txt
qeval.py -t t_myteam.txt -q query_myteam.txt


// 4. To run the fourth query ,to find the probability a player has scored 1000 points at least once in the last decade, run the following script.
// required files t_thousand.txt ,query_thousand.txt
qeval.py -t t_thousand.txt -q query_thousand.txt
