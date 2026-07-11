import os
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Pre-load NLTK data (should be downloaded during pipeline setup, but safe to try)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

class MLService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self._load_models()

    def _load_models(self):
        """Loads the pre-trained vectorizer and logistic regression model from the models directory."""
        # Find the path to the models directory relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        models_dir = os.path.join(base_dir, 'models')
        
        vectorizer_path = os.path.join(models_dir, 'tfidf_vectorizer.joblib')
        model_path = os.path.join(models_dir, 'sentiment_model.joblib')
        
        if os.path.exists(vectorizer_path) and os.path.exists(model_path):
            self.vectorizer = joblib.load(vectorizer_path)
            self.model = joblib.load(model_path)
            print("[MLService] Successfully loaded sentiment models.")
        else:
            print("[MLService WARNING] Models not found. Run the ML pipeline first.")

    def preprocess_text(self, text):
        """Must EXACTLY MATCH the preprocessing pipeline from 02_nlp_preprocessing.ipynb"""
        if not isinstance(text, str):
            return ""
        
        # Lowercase
        text = text.lower()
        # Remove HTML
        text = re.sub(r'<[^>]+>', '', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Special characters removal
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize (simple split)
        tokens = text.split()
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        return " ".join(tokens)

    def predict_sentiment(self, text):
        """Predicts the sentiment of a given text."""
        if not self.model or not self.vectorizer:
            print("[MLService] Using fallback: Models not loaded.")
            return "neutral"
            
        processed_text = self.preprocess_text(text)
        if not processed_text:
            return "neutral" # Default for empty
            
        vec = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(vec)
        return str(prediction[0]).lower().strip()

ml_service = MLService()
