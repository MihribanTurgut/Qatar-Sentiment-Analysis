import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re
from collections import Counter
import networkx as nx

df = pd.read_excel('WorldCup.xlsx')

df = df.drop_duplicates(subset=['Tweet'])

df.to_excel('WorldCupNew.xlsx', index=False)

df = df[["Date", "Sentiment"]]
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# Line chart
daily_counts = df.resample("D").count()
daily_positive = df[df["Sentiment"] == "Positive"].fillna(0).resample("D").count()
daily_negative = df[df["Sentiment"] == "Negative"].fillna(0).resample("D").count()

# Ensure that all dataframes have the same number of rows
daily_positive = daily_positive.reindex(daily_counts.index, fill_value=0)
daily_negative = daily_negative.reindex(daily_counts.index, fill_value=0)

# Plot positive and negative sentiment over time
plt.plot(daily_counts.index, daily_positive["Sentiment"], label="Positive")
plt.plot(daily_counts.index, daily_negative["Sentiment"], label="Negative")
plt.xlabel("Date")
plt.ylabel("Number of Tweets")
plt.title("Comparison of Positive and Negative Sentiment during the 2022 World Cup")
plt.legend()
plt.show()

#bar chart

sentiment_counts = df['Sentiment'].value_counts()
sentiment_counts.plot(kind='bar')
plt.title('Sentiment Counts')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

#pie chart
sentiment_counts = df['Sentiment'].value_counts()

plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
plt.title('Sentiment Distribution')

plt.show()



#relational chart


keywords = ['Qatar', 'World','Cup','bid','football', 'soccer']

G = nx.Graph()

for keyword in keywords:
    G.add_node(keyword)

for i, row in df.iterrows():
    tweet_words = row['Tweet'].split()
    for word in tweet_words:
        if word in keywords:
            for other_word in tweet_words:
                if other_word != word and other_word in keywords:
                    G.add_edge(word, other_word)


nx.draw(G, with_labels=True)
plt.show()
 

#most common words
tweets = df['Tweet'].tolist()
stop_words = ['the', 'a', 'and', 'of', 'in', 'to', 'is','for','an'] 

words = []
for tweet in tweets:
    words += [word for word in tweet.split() if word.lower() not in stop_words]


word_counts = Counter(words)
most_common_words = word_counts.most_common(6)

print(f"Most common words: {most_common_words}")

#hashtag 
 
hashtags = []
for tweet in df['Tweet']:
    tags = re.findall(r'\#\w+', tweet)
    if tags:
        hashtags.extend(tags)


tag_freq = Counter(hashtags)


top_tags = tag_freq.most_common(10)
print(top_tags)


#most tweeeted date

df['Date'] = pd.to_datetime(df['Date']).dt.date


date_counts = df['Date'].value_counts()

most_common_date = date_counts.index[0]
tweet_count = date_counts.iloc[0]
print(f"Most tweeted date: {most_common_date}, Tweet count: {tweet_count}")

#sentiment aanalysis
sentiment_counts = df['Sentiment'].value_counts()

positive_count = sentiment_counts.loc['Positive']
negative_count = sentiment_counts.loc['Negative']
neutral_count = sentiment_counts.loc['Neutral']


most_common_sentiment = sentiment_counts.idxmax()
print(f"Most common sentiment: {most_common_sentiment}")

print(f"Positive tweets : {positive_count}")
print(f"Negative tweets : {negative_count}")
print(f"Neutral tweets : {neutral_count}")

#user count
user_counts = df['User'].value_counts()

most_common_user = user_counts.idxmax()
most_common_user_tweet_count = user_counts.loc[most_common_user]
print(f"Most tweeted user: {most_common_user}")
print(f"{most_common_user} tweeted a total of {most_common_user_tweet_count}.")