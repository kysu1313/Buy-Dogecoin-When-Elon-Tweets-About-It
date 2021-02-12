import os
import robin_stocks as rs
from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error
from datetime import date
import urllib
import twitter
import time

# Keywords to look for in each tweet
# I recommend expanding this a bit
DOGIES = ["Doge", "doge", "DOGE", "dogecoin",
          "Dogecoin", "ogecoin", "gecoin", "ecoin"]
LAST_TWEETS = []
TOTAL_PURCHASED = 0
PREVIOUS_PRICE = 0

# Minimum amount of money you want in in your account
# Will not purchase after this
MINIMUM_ACCOUNT_BALANCE = 5

# Amount of dogecoin (number of coins) you want to purchase
# each time Elon tweets about it.😂
BUY_AMOUNT = 10

# The location where you want your database
DATABASE_LOCATION = r"D:\PROGRAMS\Python\DogeTrader\doge.db"


def user_tweet(thandle, conn):
    # Get last 5 tweets from the given username

    statuses = twitter_api.GetUserTimeline(screen_name=thandle, count=5)
    for status in statuses:
        isNew = find_in_db(status.text, conn)
        if (isNew):
            print("New Post: ", status.text)
            insert_post_into_db(status.text, conn)
            for doge in DOGIES:
                if doge in status.text:
                    return True
    return False


def find_in_db(status_text, conn):
    # Search database for post message
    # Don't want to buy many times for the same post.... or do I?

    select_query = "SELECT * FROM posts WHERE post LIKE \'" + \
        str(status_text) + "\'"
    cursor = conn.cursor()
    result = ""
    if conn is not None:
        cursor.execute(select_query)
        result = cursor.fetchall()
    if not result:
        return True
    else:
        return False


def insert_post_into_db(status_text, conn):
    # Insert the given post into the database

    insert_query = '''INSERT INTO posts(post, date) VALUES(\'{}\', \'{}\');'''.format(
        str(status_text), date.today())
    cursor = conn.cursor()
    if conn is not None:
        cursor.execute(insert_query)
        conn.commit()


def create_connection(db_file):
    # Opens a connection to the SQLite database

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def create_db_table(conn):
    # Creates the table in the SQLite database where we will store the
    # posts we've already viewed.

    table_query = """
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    post BLOB NOT NULL,
                    date TEXT NOT NULL
                );
                """
    cursor = conn.cursor()
    if conn is not None:
        cursor.execute(table_query)


def buy(rs, amt):
    # How many doge coins you want to purchase when
    # the bot gets a hit

    cash = rs.profiles.load_account_profile("buying_power")
    if (float(cash) > MINIMUM_ACCOUNT_BALANCE):
        rs.orders.order_buy_crypto_by_quantity(
            'DOGE', amt, timeInForce='gtc')
    print("Buying power: $", cash)
    print("Just purchased ", amt, " of dogecoins")


if __name__ == "__main__":
    load_dotenv()
    conn = create_connection(DATABASE_LOCATION)
    create_db_table(conn)
    robin_user = os.environ.get("robinhood_username")
    robin_pass = os.environ.get("robinhood_password")

    rs.login(username=robin_user,
             password=robin_pass,
             expiresIn=86400,
             by_sms=True)

    twitter_api = twitter.Api(consumer_key=os.getenv("TWITTER_KEY"),
                              consumer_secret=os.getenv("TWITTER_SECRET"),
                              access_token_key=os.getenv(
        "TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_TOKEN_SECRET"))
    user_dict = rs.account.build_user_profile()
    loop_count = 0

    try:
        while True:
            response = user_tweet("@elonmusk", conn)
            if (response):
                buy(rs, BUY_AMOUNT)
                #print("test buy")
            print("Loop: ", loop_count)
            loop_count += 1
            time.sleep(15)

    except KeyboardInterrupt:
        conn.close()
        pass
