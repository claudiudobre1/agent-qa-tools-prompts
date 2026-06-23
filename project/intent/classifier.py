from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from project.intent.training_data import TRAINING_EXAMPLES


class IntentClassifier:
    def __init__(self) -> None:
        self.model = Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer()),
                ("classifier", LogisticRegression(max_iter=1000)),
            ]
        )

        texts = [text for text, label in TRAINING_EXAMPLES]
        labels = [label for text, label in TRAINING_EXAMPLES]

        self.model.fit(texts, labels)

    def predict(self, text: str) -> str:
        return self.model.predict([text])[0]