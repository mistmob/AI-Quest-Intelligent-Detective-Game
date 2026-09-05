class ScoringSystem:
    CORRECT_POINTS = 100
    BONUS_POINTS = 50

    @staticmethod
    def calculate_score(correct, attempts=1):
        if not correct:
            return 0

        score = ScoringSystem.CORRECT_POINTS

        if attempts == 1:
            score += ScoringSystem.BONUS_POINTS

        return score