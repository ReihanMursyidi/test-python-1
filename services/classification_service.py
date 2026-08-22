class ClassificationService:
    def __init__(self, model_path: str = None):
        self.model_path = model_path

    def predict_category(self, title: str, description: str) -> str:

        return "ACCESS"