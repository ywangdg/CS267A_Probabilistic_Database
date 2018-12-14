// 1. To run the first query to find out if a player is making 20 million dollars or more, run the following script.
// required files t_salary.txt query_salary.txt
python qeval.py -t t_salary.txt -q query_salary.txt


// 2. To run the second query to find out if a player is overpaid, run the following script.
// required files t_salary.txt ,t_overpaid.txt ,query_overpaid.txt
python qeval.py -t  t_salary.txt   -t t_overpaid.txt -q query_overpaid.txt

// 3. To run the third query to find the probability that a specific nba team has an overpaid player, run the following script.
// required files t_myteam.txt, query_myteam.txt
python qeval.py -t t_myteam.txt -q query_myteam.txt


// 4. To run the fourth query ,to find the probability a player has scored 1000 points at least once in the last decade, run the following script.
// required files t_thousand.txt ,query_thousand.txt
python qeval.py -t t_thousand.txt -q query_thousand.txt
