Runwithme recently changed its name to Racery! [Racery](http://racery.com/) let's people build "real races, virtual routes". Back in March, they sent a preliminary survey to their runners to get to know them better. I did some tests + made some graphs to see whether there were any interesting trends in the data. The results hinted at interesting trends, and gave a better idea of the kinds of questions Racery could ask in the future. Namely, there was a strong indication that running in groups pushed runners to run further and more frequently. They published the related graphs on their [blog](http://racery.tumblr.com/post/122282121215/to-run-farther-run-together).

### Overview

To run w/ survey results: `python survData.py`

Data.py reads in data from the RunWithMe submissions database. There are various functions for sorting and graphing this data.

A survey was sent to RunWithMe users 03/15, the information from this survey is handled in survData.py. When run, the main method in this file creates an instance of the Data class from survData.py, which makes it possible to access additional information about the survey respondents based on their past history using RunWithMe.

I used csv files downloaded 04/01 for the sumbissions and the survey responses. However, there is the option to read the submissions.csv file from the specified url at any date in the future (although login is required for access to the RunWithMe database).

Many of the graphing functions in survData.py are commented out instead of being put into seperate definitions. This was done because I was rapidly testing different graphs. It would make sense to make them into functions in the future. Similarly, the code for some of the graphs that appear in my write up have been deleted. 

###Survey:

1. How often do you run with other people? 
* Never
* Rarely
* Often
* Always
2. How many people do you usually run with?
* 1
* 2-3
* 3-6
* >6
* It really varies
3. How many real-world races did you run in the last twelve months? (0-9+)
4. What is the total distance you’ve covered in real-world races in the last twelve months? 
5. Have you initiated a RunWithMe race? (Yes, No, Planning to)
6. How many people do you know personally who have used RunWithMe? (0-9+)
7. Which new feature would you prefer? 
* Dedicated URL for my profile
* Message board for each race
* Display my bio photo as my avatar on the map 
* Automatically push my daily mileage to Facebook                            
8. How would you describe RunWithMe to a friend? (free response)
9. Where do you get news and information about running? (free response)
10. Age? (free response)
11. Sex? (free response)

###Reflections:

The survey results were interesting, but they also revealed the holes in the survey/the questions Racery might want to ask in the future. We avoided asking obvious questions like , "How would you rate Racery on a scale of 1-5?" or "Why do you use RWM?" , but questions like this could yeild useful data points. Also, some of the response options were vague so I had to make more definitive categories as I was doing the analysis, although I made an effort not to let my cognitive biases distort the data, cognitive biases were the only way to break apart the categories, so that's treading a fine line. To avoid this in the future, it might make sense to use more concrete/uniform categories (at the risk of forcing respondents to robotically quantify their running habits).

One question that Racery could ask in its next survey is, "What question would you like Racery to ask in its next survey?"

The 9+ categories in 3 and 6 were much more populous than expected! We were pretty impressed by the number of people who had raced over 9 races in the past year, and the number of people who personally new other RunWithMe users! This distribution made it impossible to do any statistical testing on these two questions without inducing some pattern or leaving out data. It would make sense to collect new data on one or both of those questions and allow the respondent to enter a number so that those questions are actually viable for statistical tests.


###Questions of interest:

*this part is not really organized or updated*

At least two questions that result in quantitative variables that you feel may be related:

Do those who personally know more RunWithMe users also participate in more RWM races? (q.6 vs. run data)
Do those who complete more real-world races also participate in more RunWithMe races? (q.3 vs. run data)

TWO WAY TABLES-- At least two questions that result in categorical variables:

-Are “avid racers” more likely to initiate a RunWIthMe race? (q3+q4 and q5)

The response variable is likelyhood of initiating a RunWithMe race and the explanatory variable is the type of racer.

If the grouping for avid racers doesn't work out we could likelyhood if initiating a race (q5- response) and the miles completed in races (q4).

-Are “social runners” more likely to initiate a RunWithMe race? (q1+q2 and q5)

Likelihood to initiate is the response and social is the explanatory. 

-If neither of the above, relate 1 and 2, and 3 and 4

--At least two questions that result in quantitative variables for making mean comparisons between groups:

Do “avid racers” log more miles on RunWithMe? (total, not average) (q3+q4 and run data)

Do “social runners” know more RunWithMe users? (q1+q2 and q6)

Are "social runners" members of more RunWithMe races?

Have respondents been using RunWithMe for longer than non-respondents? (histogram overlay w/ duration for respondents vs duration for non. respondents)
