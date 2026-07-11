# %% [markdown]
# # NLP Preprocessing
# Tokenization, stopword removal, and lemmatization.

# %%
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import os

# %%
# Download required NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# %%
# Load cleaned data
df = pd.read_csv('../data/processed/cleaned_reviews.csv')
print("Loaded cleaned reviews.")

# %%
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize (simple split for speed)
    tokens = text.split()
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# %%
print("Applying preprocessing...")
df['processed_text'] = df['text'].apply(preprocess_text)
df = df[df['processed_text'].str.len() > 0]
print("Preprocessing complete.")

# %%
# Save preprocessed data
df.to_csv('../data/processed/preprocessed_reviews.csv', index=False)
print("Preprocessed dataset saved to ../data/processed/preprocessed_reviews.csv")
