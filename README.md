# looking-ahead

Readme:

How to run the code getfirstandTenthPR.py:
==========
python getfirstandTenthPR.py -username 'xxxx' -token 'aaaa' -year 'yyyy' 



How to run the code git.py:
==========
[[basic/oauth] With credentials (Pass the password/token in token)

script.py -org "Twitter" -top 2 -username “user” -token ‘token’ 

[No credentials run, API limit of 60/hour]
script.py -org "Twitter" -top 2 

Unit test:
=========
1. Passing all required arguments at command line
2. Passing all arguments at command line (optional too)
3. Not passing required argument
4. Failed api response - credential based . 
5. Keys missing in the api response.

Future modifications:
====================

1. Adding more structure - Putting main method in a runner.py and segregating the helper methods in a separate class.
2. Providing an additional flag that can provide a certain stat based on input.
ex.parser.add_argument('-flag', help = 'Flag to set the stats type. Default=All', dest = 'stats_type', type=str, default="All")
3. Adding xception handling [403, ZeroDivisionError, 422 Client Error, etc]
4. Adding Unit tests
5. Updating 'get_pr_contibution_percent' for efficiency.

Limitation/Assumptions:
======================
1. Pulling public repo
2.  Considered only first 100 records [https://developer.github.com/v3/guides/traversing-with-pagination/]
3.Fork= 0, If the PR api response is missing the dictionary key (head, repo)
4. Considered all states PR.


Test Data:
==========
1. -org "Twitter" -top 2
2. -org "Twitter" -top 10
3. -org "facebook" -top 3
4. -org "google" -top 2
5. -org "awesomedata" -top 20
