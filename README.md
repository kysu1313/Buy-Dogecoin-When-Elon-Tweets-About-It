# Buy-Dogecoin-When-Elon-Tweets-About-It
 Link your robinhood account to this app to purchase some dogecoin any time Elon Musk tweets about it.
 
This was a fun project I made in a few hours when I was supposed to be studying.
The codes not perfect, or even good, but it does work.

#Setup:
1) Clone this repository
2) To run this bot you need to get your username/email and account number from robinhood. 
3) `pip install robinhood_stocks`
   or, Clone this repo https://github.com/jmfernandes/robin_stocks and put it in the root folder, then inside it `pip install .`
4) `pip install python-twitter`
5) `pip install dotenv`
6) Create a twitter developer account and then make a new app. From this app collect your keys and secrets and put them in the .env file like below.
7) Create a .env file that contains:
       `TWITTER_KEY="your twitter api key"`
       `TWITTER_SECRET="your twitter secret"`
       `TWITTER_BEARER_TOKEN="your twitter bearer token"`
       `TWITTER_ACCESS_TOKEN="your access token"`
       `TWITTER_TOKEN_SECRET="your token secret"`
8) Download Sqlite DBrowser from https://sqlitebrowser.org/dl/
9) Modify the variables at the top of app.py to your liking. 
10) Make $$$  :)
