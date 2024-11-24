THE CODE WE DRAW DATA FROM TWITTER AND ANALYSIS OF EXCELE PRINTING SENTIMENT:

import snscrape.modules.twitter as sntwitter
import pandas as pd
from textblob import TextBlob
import xlsxwriter
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
with xlsxwriter.Workbook("WorldCup2.xlsx") as workbook:
    worksheet = workbook.add_worksheet()

# Define functions for data cleaning
def remove_links(text):
    # Remove hyperlinks from text
    return re.sub(r'http\S+', '', text)

def remove_retweets(text):
    # Remove retweet label from text
    return re.sub(r'^RT[\s]+', '', text)

def remove_symbols(text):
    # Remove symbols from text
    return re.sub(r'[^\w\s]', '', text)

def remove_stopwords(text):
    # Remove stopwords from text
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_tokens)


# Define list to store cleaned tweets
cleaned_tweets = []

query = "(World Cup 2022) (2022 World Cup) (Qatar 2022 World Cup) (Qatar World Cup 2022) (Qatar World Cup) until:2023-04-01since:2022-12-30"
tweets = []
limit = 500000

workbook = xlsxwriter.Workbook("Qatar3.xlsx")
worksheet = workbook.add_worksheet()

headers = ['Date', 'User', 'Tweet', 'Sentiment']
for col, header in enumerate(headers):
    worksheet.write(0, col, header)

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break
    if tweet.content not in cleaned_tweets:
        cleaned_tweet = remove_links(tweet.content)
        cleaned_tweet = remove_retweets(cleaned_tweet)
        cleaned_tweet = remove_symbols(cleaned_tweet)
        cleaned_tweet = remove_stopwords(cleaned_tweet)
        cleaned_tweets.append(cleaned_tweet)
        worksheet.write(len(cleaned_tweets), 0, tweet.date.strftime('%Y-%m-%d %H:%M:%S')) 
        worksheet.write(len(cleaned_tweets), 1, tweet.username) 
        worksheet.write(len(cleaned_tweets), 2, cleaned_tweet) 

        blob = TextBlob(cleaned_tweet)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            worksheet.write(len(cleaned_tweets), 3, 'Positive')
        elif sentiment < 0:
            worksheet.write(len(cleaned_tweets), 3, 'Negative')
        else:
            worksheet.write(len(cleaned_tweets), 3, 'Neutral')

workbook.close()

# Read cleaned data into dataframe
df = pd.read_excel('WorldCup2.xlsx')

# Drop unnecessary columns
df = df.drop(columns=['User'])

# Rename columns
df = df.rename(columns={'Date': 'Date/Time', 'Tweet': 'Cleaned Tweet', 'Sentiment': 'Sentiment Score'})

# Remove duplicates
df = df.drop_duplicates(subset=['Cleaned Tweet'])

df = df.groupby('Cleaned Tweet').first().reset_index()


# Calculate statistics
total_tweets = len(df.index)
positive_tweets = len(df[df['Sentiment Score'] == 'Positive'])
negative_tweets = len(df[df['Sentiment Score'] == 'Negative'])
neutral_tweets = len(df[df['Sentiment Score'] == 'Neutral'])


percent_positive = round((positive_tweets / total_tweets) * 100, 2)
percent_negative = round((negative_tweets / total_tweets) * 100, 2)
percent_neutral = round((neutral_tweets / total_tweets) * 100, 2)

print('Total tweets:', total_tweets)
print('Positive tweets:', positive_tweets)
print('Negative tweets:', negative_tweets)
print('Neutral tweets:', neutral_tweets)
print('Percent positive:', percent_positive, '%')
print('Percent negative:', percent_negative, '%')
print('Percent neutral:', percent_neutral, '%')


----------------------------------------------------------------------

POSTING EXCEL FILE TO COLUMNS CHART

import pandas as pd
import matplotlib.pyplot as plt

//Upload the excel file
df = pd.read_excel('Qatar3.xlsx')

//Group the date column by months and calculate the number of tweets for each month
df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
grouped = df.groupby(df['Date'].dt.strftime('%Y-%m'))['Tweet'].count()

//Create a bar chart
grouped.plot(kind='bar')

//Set chart properties
plt.title('Number of Tweets per Month')
plt.xlabel('Month')
plt.ylabel('Number of Tweets')
plt.show()


---------------------------


POSTING EXCEL FILE TO A PIE CHART

import pandas as pd
import matplotlib.pyplot as plt

//Upload the excel file
df = pd.read_excel('Qatar3.xlsx')

//Calculate the number of distinct values ​​in the Sentiment column
sentiment_counts = df['Sentiment'].value_counts()

//Draw the pie chart
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
plt.title('Sentiment Distribution')

plt.show()


------------------------------

10 MOST USED WORDS


import pandas as pd
from collections import Counter

//Read Excel file
df = pd.read_excel('Qatar3.xlsx')

//Get all tweets as a list
tweets = df['Tweet'].tolist()

//Get all words as a list
words = []
for tweet in tweets:
    words += tweet.split()

//Count the words and find the most passed
word_counts = Counter(words)
most_common_words = word_counts.most_common(10)

//Print the top 10 words
print(most_common_words)



--------------------------

MOST TWEET AND WHICH DAY IT WAS MADE:

İmport pandas as pd

//Read Excel file
df = pd.read_excel('Qatar3.xlsx')

df['Date'] = pd.to_datetime(df['Date']).dt.date

//Count the dates
date_counts = df['Date'].value_counts()

//Print most tweeted date and number of tweets
most_common_date = date_counts.index[0]
tweet_count = date_counts.iloc[0]
print(f"Most tweeted date: {most_common_date}, number of tweets: {tweet_count}")



----------------------------------


MOST USED SENTIMENT AND NUMBER OF SENTIMENTS



import pandas as pd

//Read Excel file
df = pd.read_excel('Qatar3.xlsx')

//Count tweets in Sentiment column
sentiment_counts = df['Sentiment'].value_counts()

//Print positive, negative and neutral tweet counts
positive_count = sentiment_counts.loc['Positive']
negative_count = sentiment_counts.loc['Negative']
neutral_count = sentiment_counts.loc['Neutral']

//Print which emotion is used the most
most_common_sentiment = sentiment_counts.idxmax()
print(f"Most used emotion: {most_common_sentiment}")


//Print results
print(f"Number of positive tweets: {positive_count}")
print(f"Number of negative tweets: {negative_count}")
print(f"Number of neutral tweets: {neutral_count}")


--------------------------------------------------------


MOST TWEET USERS AND NUMBER OF TWEETS

import pandas as pd

//Read Excel file
df = pd.read_excel('Qatar3.xlsx')

//Count tweets in User column
user_counts = df['User'].value_counts()

//Print the name of the user who tweeted the most and how many tweets they have tweeted
most_common_user = user_counts.idxmax()
most_common_user_tweet_count = user_counts.loc[most_common_user]
print(f"User who tweeted the most: {most_common_user}")
print(f"{most_common_user} total {most_common_user_tweet_count} tweeted.")



-------------------------------------------

CLEANED EXCEL FILE

import pandas as pd

//Read Excel file
df = pd.read_excel('Qatar3.xlsx')

//Delete rows with duplicate content in tweet column
df = df.drop_duplicates(subset=['Tweet'])

//Printing updated data to Excel file
df.to_excel('Replica.xlsx', index=False)


