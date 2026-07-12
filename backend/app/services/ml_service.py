import os
import joblib
from app.core.text_preprocessing import preprocessor

class MLService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
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
        """Uses the shared preprocessing pipeline"""
        return preprocessor.preprocess_text(text)

    def predict_sentiment(self, text):
        """Predicts the sentiment of a given text and returns (sentiment, confidence)."""
        if not self.model or not self.vectorizer:
            print("[MLService] Using fallback: Models not loaded.")
            return "neutral", 0.0
            
        processed_text = self.preprocess_text(text)
        if not processed_text:
            return "neutral", 0.0 # Default for empty
            
        vec = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(vec)
        sentiment_label = str(prediction[0]).lower().strip()
        
        confidence = 0.0
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(vec)[0]
            confidence = float(max(probs))
            
        return sentiment_label, confidence

ml_service = MLService()
