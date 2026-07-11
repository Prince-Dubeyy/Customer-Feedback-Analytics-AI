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
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app.core.text_preprocessing import preprocessor

# Apply preprocessing
print("Applying preprocessing...")
df['processed_text'] = df['text'].apply(preprocessor.preprocess_text)
df = df[df['processed_text'].str.len() > 0]
print("Preprocessing complete.")

# %%
# Save preprocessed data
df.to_csv('../data/processed/preprocessed_reviews.csv', index=False)
print("Preprocessed dataset saved to ../data/processed/preprocessed_reviews.csv")
