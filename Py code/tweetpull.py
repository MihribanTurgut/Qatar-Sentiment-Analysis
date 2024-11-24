import snscrape.modules.twitter as sntwitter
import pandas as pd
from textblob import TextBlob
import xlsxwriter

query = "(World Cup 2022) (2022 World Cup) (Qatar 2022)  until:2010-12-01 since:2009-03-01"
tweets = []
limit = 50000

workbook = xlsxwriter.Workbook("WorldCup2.xlsx")
worksheet = workbook.add_worksheet()

headers = ['Date', 'User', 'Tweet', 'Sentiment']
for col, header in enumerate(headers):
    worksheet.write(0, col, header)


df = pd.read_excel('WorldCup2.xlsx')
print(df)