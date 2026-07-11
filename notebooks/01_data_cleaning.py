# %% [markdown]
# # Data Cleaning Pipeline
# This notebook downloads a sample of the Amazon Customer Reviews dataset from the UCI Machine Learning Repository and performs cleaning.

# %%
import pandas as pd
import urllib.request
import zipfile
import os
import re

# %%
# Download the dataset (UCI Sentiment Labelled Sentences - Amazon Reviews)
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00331/sentiment%20labelled%20sentences.zip"
zip_path = "../data/raw/sentiment.zip"

print(f"Downloading data from {url}...")
os.makedirs("../data/raw", exist_ok=True)
urllib.request.urlretrieve(url, zip_path)

print("Extracting dataset...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall("../data/raw/")

# %%
# Load the Amazon reviews dataset
txt_path = "../data/raw/sentiment labelled sentences/amazon_cells_labelled.txt"
print("Parsing dataset...")
df = pd.read_csv(txt_path, sep='\t', header=None, names=['text', 'label'])

# Check for missing values and duplicates
print("Missing values before:\n", df.isnull().sum())
df.dropna(subset=['text', 'label'], inplace=True)
print("Duplicates before:", df.duplicated().sum())
df.drop_duplicates(inplace=True)

# %%
# Define sentiment label (0: negative, 1: positive)
def map_sentiment(label):
    if label == 0:
        return 'negative'
    else:
        return 'positive'

df['sentiment'] = df['label'].apply(map_sentiment)
print("Sentiment distribution:")
print(df['sentiment'].value_counts())

# %%
# Basic text cleaning (lowercase, remove extra whitespace)
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'<[^>]+>', '', text) # remove HTML tags
    text = re.sub(r'\s+', ' ', text).strip() # normalize whitespace
    return text

df['text'] = df['text'].apply(clean_text)
# Remove empty reviews
df = df[df['text'].str.len() > 0]

# %%
# Save the cleaned dataset
os.makedirs('../data/processed', exist_ok=True)
df.to_csv('../data/processed/cleaned_reviews.csv', index=False)
print("Cleaned dataset saved to ../data/processed/cleaned_reviews.csv")
