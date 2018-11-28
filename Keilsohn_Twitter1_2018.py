# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 19:40:11 2018

@author: William Keilsohn
"""

# Import Packages
import tweepy
import pandas as pd
import numpy as np
import emoji
import re

# Import Twitter API
exec(open('twitter.py').read())

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)

# Retrieve the Users
userList = []
msg =[]
for user in tweepy.Cursor(api.search_users, q ='villanova').items(100): # From ppt provided
    msg = [user.screen_name, user.id]                  
    userList.append(msg)


# Now to get their tweets... like a boss
info = []
infos = []
for i in userList:
    for tweet in tweepy.Cursor(api.user_timeline, user_id = i[1]).items(1): # Takes forever, but thats your problem.
     info = [tweet.created_at, tweet.retweet_count, tweet.text]
     infos.append(info)

# Make one central data frame
colValues = ['User_Name', 'User_ID', 'Creation_Time', 'Retweets', 'Text']

allData = pd.DataFrame(columns=colValues) # From ppt provided.

df1 = pd.DataFrame(userList, columns = ['User_Name', 'User_ID'])
df1['ID'] = range(0, 100)
df2 = pd.DataFrame(infos, columns = ['Creation_Time', 'Retweets', 'Text'])
df2['ID'] = range(0, 100)
df3 = pd.merge(df1, df2, on = 'ID') # Ensures each tweet has a unique ID
df3 = df3.drop(columns = ['ID']) # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html#pandas.DataFrame.drop

allData = pd.DataFrame(df3) #From ppt provided.

# Deal with emojies
#for index, row in allData.iterrows(): #https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
#    emoji.demojize(row['Text']) # https://pypi.org/project/emoji/

# Create New File
userFile = open('users.txt', 'w')
userFile.write("{0:^40}{1:^30}{2:^12}{3:^30}".format(colValues[0], colValues[1], colValues[2], colValues[3]))
userFile.write('     ')
userFile.write(str(colValues[4]))
userFile.write('\n')
userFile.write('\n')
textData = ''
for index, row in allData.iterrows(): #https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
    userFile.write("{0:^40}{1:^30}{2:^20}{3:^12}".format(row['User_Name'], row['User_ID'], str(row['Creation_Time']), row['Retweets']))
    userFile.write('     ')
    textData = emoji.demojize(row['Text']).encode('unicode-escape').decode()
# https://pypi.org/project/emoji/
# https://stackoverflow.com/questions/2428117/casting-raw-strings-python
    '''
    I tried a few things to prevent the text wrap. Then I double checked the example...
    '''
    userFile.write(textData)
    userFile.write('\n')
userFile.close()
