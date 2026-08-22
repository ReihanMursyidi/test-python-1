import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
import joblib
import os

def train():
   print("Loading dataset...")
   # Load dataset
   df = pd.read_csv('incidents_training.csv')

   X = df['text']
   y = df['category']

   # Train/Test Split
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

   # Pipeline
   print("Melatih model...")
   model = make_pipeline(TfidfVectorizer(stop_words='english'), MultinomialNB())

   # Training
   model.fit(X_train, y_train)

   # Evaluasi
   y_pred = model.predict(X_test)
   print("\n=== Laporan Evaluasi Model ===")
   print(classification_report(y_test, y_pred))

   # Simpan Model
   os.makedirs('app/core', exist_ok=True)
   joblib.dump(model, 'app/core/incident_classifier.pkl')
   print("\nModel berhasil disimpan di app/core/incident_classifier.pkl")

if __name__ == "__main__":
   train()