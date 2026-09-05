from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


class AIModelComparison:

    def __init__(self):

        self.training_text = [
            "hello friend how are you",
            "meeting scheduled for tomorrow",
            "please find the report attached",
            "your package has been delivered",
            "thank you for your message",
            "the project meeting is at ten",
            "your account has been compromised",
            "click this link immediately",
            "urgent action required",
            "send your password",
            "send your verification code",
            "your bank account is locked",
            "you have won a prize",
            "claim your reward now",
            "security alert unusual login"
        ]

        self.training_labels = [
            "safe",
            "safe",
            "safe",
            "safe",
            "safe",
            "safe",
            "dangerous",
            "dangerous",
            "dangerous",
            "dangerous",
            "dangerous",
            "dangerous",
            "dangerous",
            "dangerous",
            "dangerous"
        ]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english"
        )

        features = self.vectorizer.fit_transform(
            self.training_text
        )

        self.naive_bayes = MultinomialNB()

        self.logistic_regression = LogisticRegression(
            max_iter=1000
        )

        self.random_forest = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        self.naive_bayes.fit(
            features,
            self.training_labels
        )

        self.logistic_regression.fit(
            features,
            self.training_labels
        )

        self.random_forest.fit(
            features,
            self.training_labels
        )

    def predict(self, text):

        features = self.vectorizer.transform([text])

        models = {
            "Naive Bayes": self.naive_bayes,
            "Logistic Regression": self.logistic_regression,
            "Random Forest": self.random_forest
        }

        results = {}

        for name, model in models.items():

            prediction = str(
                model.predict(features)[0]
            )

            probabilities = model.predict_proba(
                features
            )[0]

            classes = model.classes_

            probability_map = dict(
                zip(classes, probabilities)
            )

            results[name] = {
                "prediction": prediction,
                "safe_probability": float(
                    probability_map.get("safe", 0)
                ),
                "dangerous_probability": float(
                    probability_map.get("dangerous", 0)
                )
            }

        return results

    def final_decision(self, text):

        results = self.predict(text)

        predictions = [
            result["prediction"]
            for result in results.values()
        ]

        dangerous_votes = predictions.count(
            "dangerous"
        )

        safe_votes = predictions.count(
            "safe"
        )

        if dangerous_votes > safe_votes:
            decision = "dangerous"
        else:
            decision = "safe"

        return {
            "models": results,
            "final_decision": decision,
            "dangerous_votes": dangerous_votes,
            "safe_votes": safe_votes
        }