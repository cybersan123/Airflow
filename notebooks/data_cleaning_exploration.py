# -*- coding: utf-8 -*-
"""data_cleaning_exploration.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jU6I53BYSZ2kX-qcxcWP_1bPNYWvB24f

# Data Cleaning

Data cleaning is the process of detecting and removing errors and inconsistencies from the data to improve its quality. Improper data cleaning process can lead to errors, faulty analysis, distortion in dataset and eventually incompatible datasets for machine learning purposes. There is no absolute way to prescribe the exact steps in the data cleaning process because the processes will vary from dataset to dataset. My data cleaning process includes:

* Check the data types
* Check for duplicates - Primary key ('tweets.id')
* Check missing values
* Make text all lower case
* Remove links and images
* Remove hashtags
* Remove @ mentions
* Remove emojis
* Remove stop words
* Remove punctuation
* Get rid of stuff like "what's" and making it "what is'
* Stemming / lemmatization
"""

from google.colab import drive
drive.mount('/content/drive')

import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "ftfy"])
pip install -qqq ftfy

## Import required libraries

## warnings
import warnings
warnings.filterwarnings("ignore")

## for data
import numpy as np
import pandas as pd

## for plotting
import matplotlib.pyplot as plt
import seaborn as sns

## for processing
import nltk
import re
import ftfy
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

## for opening, manipulating, and saving many different image file f
from PIL import Image 

## WordCloud - Python linrary for creating image wordclouds
from wordcloud import WordCloud
from nltk import pos_tag ## For Parts of Speech tagging
import random ## generating random numbers

"""## Load the datasets"""

depressive_tweets_df = pd.read_csv("/content/drive/MyDrive/NLP/Depression_Detection/Data_fetch_API/output/depressive_tweets.csv")
random_tweets_df = pd.read_csv("/content/drive/MyDrive/NLP/Depression_Detection/Depression_tweets_Data/Data1/Sentiment Analysis Dataset 2.csv", 
                               encoding = "ISO-8859-1", usecols = range(0,4), nrows = 40000)

depressive_tweets_df

random_tweets_df

## Slicing the random tweets to have sentiment == 1 
new_rand_df = random_tweets_df[random_tweets_df.Sentiment == 1]
new_rand_df.reset_index(inplace=True)

new_rand_df.shape

new_rand_df.head()

"""20952 random tweets with sentiment == 1

## Data Cleaning-Processing:
"""

print(depressive_tweets_df.shape)
print(new_rand_df.shape)

## Check the data type of each column
depressive_tweets_df.dtypes.to_frame().rename(columns={0:'data_type'})

## Check the data type of each column
new_rand_df.dtypes.to_frame().rename(columns={0:'data_type'})

## Drop unnecessary columns
depressive_tweets_df.drop(columns=['Unnamed: 0'], inplace=True)
new_rand_df.drop(columns=['ï»¿ItemID', 'index','Sentiment', 'SentimentSource'], inplace=True)

"""Since we are mostly dealing with the tweets in our datasets, it is not necessary to change the data types at this stage."""

## Finding unique values in each column
for col in depressive_tweets_df:
    print("There are ", len(depressive_tweets_df[col].unique()), "unique values in ", col)

"""By considering **tweet.id** as our primary key, we have **18190** unique tweets, so we need to get rid of the duplicates."""

## Finding unique values in each column
for col in new_rand_df:
    print("There are ", len(new_rand_df[col].unique()), "unique values in ", col)

"""No duplicates in random tweets dataset"""

## drop duplicate values in tweet.id
depressive_tweets_df.drop_duplicates(subset=['tweet.id'], inplace=True)

depressive_tweets_df.reset_index(inplace=True)

depressive_tweets_df.shape

## Find the number of Null values in each columns
depressive_tweets_df.isnull().sum().to_frame().rename(columns={0:'Null values'})

"""There are **6384** Null values in the **location** columns but since location will not be used in our analysis or as a feature in our model, we don't need to replace them."""

## Find the number of Null values in each columns
new_rand_df.isnull().sum().to_frame().rename(columns={0:'Null values'})

"""No Null values in random tweets dataset."""

## Drop all the columns except index, tweet.id and text
new_dep_df = depressive_tweets_df[['text']]

## Add label to both datasets (0 is non-depressive and 1 is depressive)
new_dep_df['label'] = pd.Series([1 for x in range(len(new_dep_df.index))])
new_rand_df['label'] = pd.Series([0 for x in range(len(new_rand_df.index))])

new_dep_df

## Change the column name to be aligned with depressive dataset
new_rand_df.rename(columns={'SentimentText': 'text'}, inplace=True)

new_rand_df

## Combine two dataframes together
df_all = pd.concat([new_dep_df, new_rand_df], ignore_index=True)

df_all

# Expand Contraction
cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text)

## Function to perform stepwise cleaning process
def tweets_cleaner(tweets):
  cleaned_tweets = []
  for tweet in tweets:
    tweet = tweet.lower() #lowercase
    
    # if url links then don't append to avoid news articles
    # also check tweet length, save those > 5 
    if re.match("(\w+:\/\/\S+)", tweet) == None and len(tweet) > 5:
    
      #remove hashtag, @mention, emoji and image URLs
      tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\#[A-Za-z0-9]+)|(<Emoji:.*>)|(pic\.twitter\.com\/.*)", " ", tweet).split())

      #fix weirdly encoded texts
      tweet = ftfy.fix_text(tweet)

      #expand contraction
      tweet = expandContractions(tweet)


      #remove punctuation
      tweet = ' '.join(re.sub("([^0-9A-Za-z \t])", " ", tweet).split())

      #stop words and lemmatization
      stop_words = set(stopwords.words('english'))
      word_tokens = nltk.word_tokenize(tweet)

      lemmatizer=WordNetLemmatizer()
      filtered_sentence = [lemmatizer.lemmatize(word) for word in word_tokens if not word in stop_words]
      # back to string from list
      tweet = ' '.join(filtered_sentence) # join words with a space in between them

      cleaned_tweets.append(tweet)

  return cleaned_tweets

"""## Word Cloud:

To get the most common words used in depressive and random datasets, the POS-tag (Parts of Speech tagging) module in the NLTK library was used. Using the WordCloud library, one can generate a Word Cloud based on word frequency and superimpose these words on any image. In this case, I used the Twitter logo and Matplotlib to display the image. The Word Cloud shows the words with higher frequency in bigger text size while the "not-so" common words are in smaller text sizes.
"""

depressive_tweets_arr = [x for x in new_dep_df['text']]
random_tweets_arr = [x for x in new_rand_df['text']]
X_d = tweets_cleaner(depressive_tweets_arr)
X_r = tweets_cleaner(random_tweets_arr)

## function to obtain adjectives from tweets
def getadjectives(tweet):
    tweet = nltk.word_tokenize(tweet)  # convert string to tokens
    tweet = [word for (word, tag) in pos_tag(tweet)
             if tag == "JJ"]  # pos_tag module in NLTK library
    return " ".join(tweet)  # join words with a space in between them

"""### Depressive Tweets Exploration"""

## Apply getadjectives function to the processed tweets 
## Extract all tweets into one long string with each word separate with a "space"
tweets_long_string = [getadjectives(x) for x in X_d]
tweets_long_string = " ".join(tweets_long_string)

# Import Twitter Logo
image = np.array(Image.open('/content/drive/MyDrive/NLP/Depression_Detection/data_cleaning/logo.jpeg'))
    
fig = plt.figure() # Instantiate the figure object
fig.set_figwidth(14) # set width
fig.set_figheight(18) # set height

plt.imshow(image, cmap=plt.cm.gray, interpolation='bilinear') # Display data as an image
plt.axis('off') # Remove axis
plt.show() # Display image

## Create function to generate the blue colour for the Word CLoud

def blue_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(210, 100%%, %d%%)" % random.randint(50, 70)

## Instantiate the Twitter word cloud object
twitter_wc = WordCloud(background_color='white', max_words=1500, mask=image)

## generate the word cloud
twitter_wc.generate(tweets_long_string)

## display the word cloud
fig = plt.figure()
fig.set_figwidth(14)  # set width
fig.set_figheight(18)  # set height

plt.imshow(twitter_wc.recolor(color_func=blue_color_func, random_state=3),
           interpolation="bilinear")
plt.axis('off')
plt.show()

twitter_wc.to_file("/content/drive/MyDrive/NLP/Depression_Detection/data_cleaning/wordcloud.png") #save to a png file

"""**Analyzing Top Words in the Word Cloud for depressive dataset**"""

## Combine all words in depressive into a list
tweets_long_string = [getadjectives(x) for x in X_d]
tweets_list=[]
for item in tweets_long_string:
    item = item.split()
    for i in item:
        tweets_list.append(i)

# Use the Built-in Python Collections module to determine Word frequency
from collections import Counter
counts = Counter(tweets_list)
df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
df.columns = ['Words', 'Count']
df.sort_values(by='Count', ascending=False, inplace=True)

df.head(10)  # Check dataframe first 10 rows

"""### Random Tweets Exploration

"""

## Apply getadjectives function to the processed tweets 
## Extract all tweets into one long string with each word separate with a "space"
tweets_long_string_rand = [getadjectives(x) for x in X_r]
tweets_long_string_rand = " ".join(tweets_long_string_rand)

# Import Twitter Logo
image = np.array(Image.open('/content/drive/MyDrive/NLP/Depression_Detection/data_cleaning/logo.jpeg'))
    
fig = plt.figure() # Instantiate the figure object
fig.set_figwidth(14) # set width
fig.set_figheight(18) # set height

plt.imshow(image, cmap=plt.cm.gray, interpolation='bilinear') # Display data as an image
plt.axis('off') # Remove axis
plt.show() # Display image

## Create function to generate the blue colour for the Word CLoud

def blue_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(210, 100%%, %d%%)" % random.randint(50, 70)

## Instantiate the Twitter word cloud object
twitter_wc = WordCloud(background_color='white', max_words=1500, mask=image)

## generate the word cloud
twitter_wc.generate(tweets_long_string_rand)

## display the word cloud
fig = plt.figure()
fig.set_figwidth(14)  # set width
fig.set_figheight(18)  # set height

plt.imshow(twitter_wc.recolor(color_func=blue_color_func, random_state=3),
           interpolation="bilinear")
plt.axis('off')
plt.show()

twitter_wc.to_file("/content/drive/MyDrive/NLP/Depression_Detection/data_cleaning/wordcloud_rand.png") #save to a png file

"""**Analyzing Top Words in the Word Cloud for random dataset**"""

## Combine all words in depressive into a list
tweets_long_string_rand = [getadjectives(x) for x in X_r]
tweets_list_rand=[]
for item in tweets_long_string_rand:
    item = item.split()
    for i in item:
        tweets_list_rand.append(i)

## Use the Built-in Python Collections module to determine Word frequency
from collections import Counter
counts = Counter(tweets_list_rand)
df_rand = pd.DataFrame.from_dict(counts, orient='index').reset_index()
df_rand.columns = ['Words', 'Count']
df_rand.sort_values(by='Count', ascending=False, inplace=True)

df_rand.head(10)  # Check dataframe first 10 rows

"""## Data Analysis:"""

## distribution of classes for prediction
def create_distribution(dataFile):
  return sns.countplot(x='label', data=dataFile, palette='hls')

create_distribution(df_all)

"""Depreesive and random (Non-depressive) tweets are almost evenly distributed.

**Finding distribution of tweet lengths**
"""

dep_line_lengths = [len(statement) for statement in new_dep_df['text']]
plt.plot(dep_line_lengths)
plt.show()

rand_line_lengths = [len(statement) for statement in new_rand_df['text']]
plt.plot(dep_line_lengths)
plt.show()

"""From the distributions above, it is clear that there is no outliers in our depressive and random datasets.

## Cleaning combined dataset and save it
"""

tweets_arr = [x for x in df_all['text']]

corpus = tweets_cleaner(tweets_arr)

corpus[:10]

## Adding clean tweets as a new column
df_all['clean_text'] = corpus

"""We have to remove those rows with tweets that has been completely deleted in the cleaning process."""

# replace field that's entirely space (or empty) with NaN
df_all.replace(r'^\s*$', np.nan, regex=True, inplace=True)

df_all[df_all['clean_text'].isnull()]

## Deleting the rows with nan 
df_all.dropna(subset=['clean_text'], inplace=True)

## Double_check for nan
df_all[df_all['clean_text'].isnull()]

## Save cleaned_dataset
df_all.to_csv('/content/drive/MyDrive/NLP/Depression_Detection/data_cleaning/processed_data/processed_data.csv',
              sep='\t', encoding='utf-8',index=False)