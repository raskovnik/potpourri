from pickle import STOP
import regex
import pandas as pd
import numpy as np
import emoji
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import sys

def date_time(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result = regex.match(pattern, s)
    if result:
        return True
    return False

def find_author(s):
    s = s.split(":")
    if len(s) == 2:
        return True
    else:
        return False

def getDataPoint(line):
    splitline = line.split(" - ")
    dateTime = splitline[0]
    date, time = dateTime.split(", ")
    message = " ".join(splitline[1:])
    if find_author(message):
        splitmessage = message.split(": ")
        author = splitmessage[0]
        message = " ".join(splitmessage[1:])
    else:
        author = None

    return date, time, author, message

def prepareData(sys.argv):
    data = []
    try:
        conversation = sys.argv[1]
    except Exception:
        print("Pass the whatsapp chat name")
        return
    with open(conversation, encoding="utf-8") as fp:
        fp.readline()
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break

            line = line.strip()
            if date_time(line):
                if len(messageBuffer) > 0:
                    data.append([date, time, author, " ".join(messageBuffer)])
                messageBuffer.clear()
                date, time, author, message = getDataPoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)

    df = pd.DataFrame(data, columns=["Date", "Time", "Author", "Message"])
    df["Date"] = pd.to_datetime(df["Date"])
    analyze(df)


def split_count(text):
    emoji_list = []
    data = regex.findall(r"\X", text)
    for word in data:
        if any(emoji.is_emoji(char) for char in word):
            emoji_list.append(word)
    return emoji_list

def analyze(df):
    df['emoji'] = df['Message'].apply(split_count)
    media_messages_df = df[df['Message'] == '<Media omitted>']
    messages_df = df.drop(media_messages_df.index)
    messages_df['Letter_Count'] = messages_df['Message'].apply(lambda s: len(s))
    messages_df['Word_Count'] = messages_df['Message'].apply(lambda s: len(s.split(" ")))
    messages_df["MessageCount"] = 1
    l = [x for x in df.Author.unique()]
    print(f"Whatsapp Chat between {l[0]} and {l[1]}")
    print(f"Total messages: {df.shape[0]:>19}")
    print(f"Media messages: {df[df['Message']=='<Media omitted>'].shape[0]:>19}")
    print(f"Total emojis: {sum(df['emoji'].str.len()):>21}\n")

    for i in range(len(l)-1):
        req_df = messages_df[messages_df['Author'] == l[i]]

        print(f"Stats for {l[i]}")
        print(f"Messages sent: {req_df.shape[0]:>20}")
        print(f"Average words per message: {round((np.sum(req_df['Word_Count']))/req_df.shape[0],2):>8}")
        print(f"Media messages sent: {media_messages_df[media_messages_df['Author'] == l[i]].shape[0]:>14}")
        print(f"Emojis sent: {sum(req_df['emoji'].str.len()):>22}\n")

    total_emojis_list = list(set([a for b in messages_df.emoji for a in b]))
    total_emojis_list = list([a for b in messages_df.emoji for a in b])
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
    
    fig = px.pie(emoji_df, values='count', names='emoji')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()

    text = " ".join(review for review in messages_df.Message)
    print(f"There are {len(text)} words in all the messages")
    stopwords = set(STOPWORDS)

    wordcloud = WordCloud(scale=7,max_words=250,collocations=True,stopwords=stopwords, background_color="white").generate(text)
    plt.figure(figsize=(15,7))
    plt.plot()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Top Words for {l[0]} and {l[1]}")
    plt.show()
    for i in range(len(l) - 1):
        dummy_df = messages_df[messages_df['Author'] == l[i]]
        text = " ".join(review for review in dummy_df.Message)
        stopwords = set(STOPWORDS)
        wordcloud = WordCloud(scale=7,max_words=250,collocations=True,stopwords=stopwords, background_color="white").generate(text)

        plt.plot()
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.title(f"Top words for {l[i]}")
        plt.show()

if __name__ == "__main__":
    prepareData()
