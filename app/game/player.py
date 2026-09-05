
class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.attempts = 0
        self.correct_answers = 0
        self.missions_completed = 0

    def record_attempt(self, correct, points):
        self.attempts += 1

        if correct:
            self.correct_answers += 1
            self.score += points

        self.missions_completed += 1

    def get_accuracy(self):
        if self.attempts == 0:
            return 0.0

        return (
            self.correct_answers / self.attempts
        ) * 100

    def get_stats(self):
        return {
            "name": self.name,
            "score": self.score,
            "accuracy": self.get_accuracy(),
            "missions_completed": self.missions_completed,
            "attempts": self.attempts,
            "correct_answers": self.correct_answers
        }

