hvn-or-hell
===========

The django heaven or hell search engine
It is dependent upon: 
The scrapy 0.21 webcrawling library
The django 1.6 web framework
The python stemming library
The python json libray
The nltk library with the stopwords corpus.
The lxml library

For the scraper go into the directory and run scrapy crawl

For checkpoint3 run 
python CoreAlgorithm.py
This runs a KNN algorithm on a small portion of the data and prints out the
results for a pre classified page that should be G. Note that this
is far from perfect due to the low amount of data being used.

For the final project run "python manage.py runserver"
Then go to http://127.0.0.1/hvnrhell to get to the app.
NOTE: This will take an exceedingly long amount of time to run
