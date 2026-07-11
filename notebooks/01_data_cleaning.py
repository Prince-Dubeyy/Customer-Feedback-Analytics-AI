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

# Inject synthetic Neutral data to ensure 3-class model support
print("Injecting synthetic neutral dataset...")
neutral_texts = [
    "I bought this product yesterday.",
    "It arrived on time.",
    "The package was standard.",
    "I have no strong opinion about this.",
    "It works fine, nothing special.",
    "It is okay.",
    "Normal delivery speed.",
    "I received the item.",
    "It does what it says.",
    "Standard quality."
] * 50 # 500 neutral examples

neutral_df = pd.DataFrame({
    'text': neutral_texts,
    'label': [2] * len(neutral_texts),
    'sentiment': ['neutral'] * len(neutral_texts)
})

df = pd.concat([df, neutral_df], ignore_index=True)

print("Sentiment distribution after injection:")
print(df['sentiment'].value_counts())

# %%
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app.core.text_preprocessing import preprocessor

# Clean text
df['text'] = df['text'].apply(preprocessor.clean_text)
# Remove empty reviews
df = df[df['text'].str.len() > 0]

# %%
# Save the cleaned dataset
os.makedirs('../data/processed', exist_ok=True)
df.to_csv('../data/processed/cleaned_reviews.csv', index=False)
print("Cleaned dataset saved to ../data/processed/cleaned_reviews.csv")
