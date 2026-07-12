# %% [markdown]
# # Model Training & Benchmarking
# Train and compare multiple models on optimized TF-IDF features.

# %%
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# Load Data
df = pd.read_csv('../data/processed/preprocessed_reviews.csv')
df.dropna(subset=['processed_text', 'sentiment'], inplace=True)

# %%
# Train-Test Split
X = df['processed_text']
y = df['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Training set: {len(X_train)} samples")
print(f"Testing set: {len(X_test)} samples")

# %%
# TF-IDF Optimization (Phase 4)
print("Extracting features with optimized TF-IDF...")
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),  # Bigrams are essential for negations
    max_features=15000,
    min_df=3,
    max_df=0.90
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# %%
# Model Benchmarking (Phase 5) & Class Balancing (Phase 6)
print("Benchmarking Models...")
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced'),
    "Linear SVM": LinearSVC(max_iter=2000, class_weight='balanced'),
    "Multinomial NB": MultinomialNB() # NB doesn't have class_weight directly, but handles it natively via priors
}

best_model_name = ""
best_model = None
best_f1 = 0

with open('../reports/model_comparison.md', 'w') as f:
    f.write("# Model Comparison Report\n\n")
    f.write("| Model | Accuracy | Precision | Recall | F1 Score |\n")
    f.write("|---|---|---|---|---|\n")
    
    for name, clf in models.items():
        print(f"Training {name}...")
        clf.fit(X_train_vec, y_train)
        y_pred = clf.predict(X_test_vec)
        
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        
        f.write(f"| {name} | {acc:.4f} | {prec:.4f} | {rec:.4f} | {f1:.4f} |\n")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = clf
            best_model_name = name

print(f"Best model selected: {best_model_name}")

# %%
# Evaluation of Best Model (Phase 10)
y_pred = best_model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')

with open('../reports/model_performance.md', 'w') as f:
    f.write(f"# Final Model Performance Report ({best_model_name})\n\n")
    f.write(f"- **Accuracy**: {accuracy:.4f}\n")
    f.write(f"- **Precision (weighted)**: {precision:.4f}\n")
    f.write(f"- **Recall (weighted)**: {recall:.4f}\n")
    f.write(f"- **F1 Score (weighted)**: {f1:.4f}\n\n")
    f.write("## Classification Report\n")
    f.write("```\n")
    f.write(classification_report(y_test, y_pred))
    f.write("\n```\n")

# %%
# Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels=['negative', 'neutral', 'positive'])
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=['negative', 'neutral', 'positive'], yticklabels=['negative', 'neutral', 'positive'], cmap='Blues')
plt.title(f'Confusion Matrix ({best_model_name})')
plt.xlabel('Predicted')
plt.ylabel('Actual')
os.makedirs('../reports/figures', exist_ok=True)
plt.savefig('../reports/figures/confusion_matrix.png')
plt.close()

# %%
# Save artifacts (Phase 11)
# Note: Since LinearSVC doesn't support predict_proba, if LinearSVC wins, we must calibrate it or use LogisticRegression.
# Let's override best_model if it's LinearSVC and we need predict_proba, OR we just use LogisticRegression anyway if it's close.
# Actually, since Phase 8 requires confidence scores (predict_proba), Logistic Regression is the safest bet for production.
if not hasattr(best_model, "predict_proba"):
    print(f"Warning: {best_model_name} does not support predict_proba natively.")
    print("Falling back to Logistic Regression for production confidence scores.")
    best_model = models["Logistic Regression"]

os.makedirs('../models', exist_ok=True)
joblib.dump(vectorizer, '../models/tfidf_vectorizer.joblib')
joblib.dump(best_model, '../models/sentiment_model.joblib')
print("Model and vectorizer saved to ../models/")
