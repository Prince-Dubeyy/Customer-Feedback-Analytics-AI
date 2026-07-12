import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Ensure resources are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # Retain important negations for sentiment context
        negations = {'not', 'no', 'nor', 'neither', 'never', 'none', 'cannot', 'doesn', "doesn't", 'isn', "isn't", 'wasn', "wasn't", 'shouldn', "shouldn't", 'wouldn', "wouldn't", 'couldn', "couldn't", 'won', "won't", 'haven', "haven't", 'hasn', "hasn't", 'hadn', "hadn't", 'aren', "aren't", 'don', "don't", 'didn', "didn't"}
        self.stop_words = self.stop_words - negations
        
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        # Lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        # Remove HTML
        text = re.sub(r'<[^>]+>', '', text)
        # Remove Mentions
        text = re.sub(r'@\w+', '', text)
        # Remove Hashtags
        text = re.sub(r'#\w+', '', text)
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def preprocess_text(self, text):
        cleaned = self.clean_text(text)
        if not cleaned:
            return ""
        # Tokenize
        tokens = cleaned.split()
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        return " ".join(tokens)

preprocessor = TextPreprocessor()
