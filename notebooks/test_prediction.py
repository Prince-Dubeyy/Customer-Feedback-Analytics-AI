import os
import sys

# Add backend to path so we can import ml_service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.services.ml_service import ml_service

test_cases = [
    "I absolutely loved this product, it works perfectly!", # Positive
    "It arrived on time, but I haven't used it much yet.", # Neutral
    "Terrible experience, it broke after one day and support ignored me.", # Negative
    "It's okay, nothing special but it gets the job done.", # Neutral
    "Wow, just wow. Best purchase I've ever made.", # Positive
    "Waste of money. Do not buy.", # Negative
    "The color is slightly different than the picture, but overall fine.", # Neutral
]

results = []
for text in test_cases:
    sentiment, conf = ml_service.predict_sentiment(text)
    results.append(f"Text: '{text}'\nPredicted: {sentiment.upper()} (Confidence: {conf:.2f})\n")

report_content = "# Real World Validation Testing\n\n" + "\n".join(results)

os.makedirs('../reports', exist_ok=True)
with open('../reports/real_world_testing.md', 'w') as f:
    f.write(report_content)

print(report_content)
print("Saved to ../reports/real_world_testing.md")
