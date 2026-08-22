import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import re

def preprocess_text(text: str) -> str:
   text = text.lower()
   text = re.sub(r'[^a-z0-9\s]', '', text)
   return text

def train_and_save_model():
   df = pd.read_csv('incidents_training.csv')

   df['text'] = df['title'] + " " + df['description']
   df['text'] = df['text'].apply(preprocess_text)

   X = df['text']
   y = df['category']

   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

   pipeline = Pipeline([
      ('tfidf', TfidfVectorizer(stop_words='english')),
      ('clf', MultinomialNB())
   ])

   pipeline.fit(X_train, y_train)

   y_pred = pipeline.predict(X_test)
   print("Classification Report:")
   print(classification_report(y_test, y_pred))

   joblib.dump(pipeline, 'app/core/incident_classifier.pkl')

if __name__ == "__main__":
   train_and_save_model()