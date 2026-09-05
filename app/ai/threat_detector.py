import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


class ThreatDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english"
        )

        self.model = MultinomialNB()

        self.training_text = [
            "hello friend how are you today",
            "meeting scheduled for tomorrow",
            "your package has been delivered",
            "thank you for your message",
            "please find the report attached",
            "your account has been compromised",
            "click this link immediately to verify your account",
            "urgent action required your password will expire",
            "you have won a prize claim your reward now",
            "send your password and verification code",
            "your bank account is locked click here",
            "security alert unusual login detected"
        ]

        self.training_labels = [
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
            "dangerous"
        ]

        self.train()

    def train(self):
        features = self.vectorizer.fit_transform(
            self.training_text
        )

        self.model.fit(
            features,
            self.training_labels
        )

    def find_suspicious_patterns(self, text):
        patterns = {
            "urgent_language": r"\b(urgent|immediately|asap|action required)\b",
            "credential_request": r"\b(password|otp|verification code|pin)\b",
            "suspicious_link": r"(https?://|www\.)",
            "financial_request": r"\b(bank|account|payment|money|prize|reward)\b"
        }

        matches = {}

        for name, pattern in patterns.items():
            found = re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            matches[name] = len(found)

        return matches

    def predict(self, text):
        features = self.vectorizer.transform([text])

        prediction = self.model.predict(features)[0]

        probabilities = self.model.predict_proba(
            features
        )[0]

        probability_map = dict(
            zip(
                self.model.classes_,
                probabilities
            )
        )

        regex_results = self.find_suspicious_patterns(text)

        return {
            "prediction": prediction,
            "safe_probability": probability_map.get(
                "safe",
                0
            ),
            "dangerous_probability": probability_map.get(
                "dangerous",
                0
            ),
            "regex_matches": regex_results
        }