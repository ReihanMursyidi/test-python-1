import joblib
import os

class ClassificationService:
    def __init__(self, model_path: str = "app/core/incident_classifier.pkl"):
        self.model_path = model_path
        self.model = None
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)

    def predict(self, text: str) -> str:
        if not self.model:
            return "OTHER"
        
        prediction = self.model.predict([text])[0]

        probabilities = self.model.predict_proba([text])[0]
        max_confidence = max(probabilities)

        if max_confidence < 0.40:
            return "OTHER"
            
        return prediction