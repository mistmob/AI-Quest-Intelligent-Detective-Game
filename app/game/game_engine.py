import random

from .player import Player


class GameEngine:

    def __init__(self, player_name):

        self.player = Player(player_name)

        # Current level
        self.current_mission = 1

        # --------------------------------------------------------
        # QUESTION BANK
        # --------------------------------------------------------

        self.question_bank = [

            {
                "title": "THE PHANTOM MESSAGE",
                "difficulty": "Easy",
                "evidence": (
                    "URGENT SECURITY ALERT!\n\n"
                    "Your bank account has been compromised. "
                    "Click https://secure-check.example immediately "
                    "and enter your password to verify your identity."
                ),
                "answer": "dangerous",
                "points": 100
            },

            {
                "title": "THE MYSTERY EMAIL",
                "difficulty": "Medium",
                "evidence": (
                    "Congratulations! You have won a $5,000 prize.\n\n"
                    "Claim your reward immediately by sending your "
                    "account password and verification code."
                ),
                "answer": "dangerous",
                "points": 150
            },

            {
                "title": "THE NORMAL MEETING",
                "difficulty": "Easy",
                "evidence": (
                    "Hello Detective,\n\n"
                    "Our project meeting is scheduled for tomorrow "
                    "at 10 AM. Please bring the project report "
                    "and presentation."
                ),
                "answer": "safe",
                "points": 100
            },

            {
                "title": "THE FAKE DELIVERY",
                "difficulty": "Easy",
                "evidence": (
                    "Your package could not be delivered.\n\n"
                    "Pay a small redelivery fee by entering your "
                    "credit card number and OTP at the link below."
                ),
                "answer": "dangerous",
                "points": 100
            },

            {
                "title": "THE TEAM UPDATE",
                "difficulty": "Easy",
                "evidence": (
                    "Hi team,\n\n"
                    "The software testing session will begin at "
                    "2 PM in Lab 3. Please bring your laptops."
                ),
                "answer": "safe",
                "points": 100
            },

            {
                "title": "THE PASSWORD WARNING",
                "difficulty": "Medium",
                "evidence": (
                    "Your password is about to expire.\n\n"
                    "Verify your account immediately by entering "
                    "your current password and security code."
                ),
                "answer": "dangerous",
                "points": 150
            },

            {
                "title": "THE PROJECT REPORT",
                "difficulty": "Easy",
                "evidence": (
                    "Reminder:\n\n"
                    "Please submit your project report to the "
                    "department before Friday."
                ),
                "answer": "safe",
                "points": 100
            },

            {
                "title": "THE LOTTERY ALERT",
                "difficulty": "Hard",
                "evidence": (
                    "FINAL WINNER NOTICE!\n\n"
                    "You have been selected to receive $25,000. "
                    "Send your bank details and verification code "
                    "to claim your prize."
                ),
                "answer": "dangerous",
                "points": 200
            },

            {
                "title": "THE UNIVERSITY NOTICE",
                "difficulty": "Medium",
                "evidence": (
                    "University Notice\n\n"
                    "The internal assessment schedule has been "
                    "uploaded to the official student portal."
                ),
                "answer": "safe",
                "points": 150
            },

            {
                "title": "THE ACCOUNT LOCK",
                "difficulty": "Hard",
                "evidence": (
                    "SECURITY NOTICE!\n\n"
                    "Your account will be permanently locked unless "
                    "you confirm your password and OTP immediately."
                ),
                "answer": "dangerous",
                "points": 200
            }
        ]

        # --------------------------------------------------------
        # RANDOMIZE QUESTIONS
        # --------------------------------------------------------

        self.missions = random.sample(
            self.question_bank,
            len(self.question_bank)
        )

        # Give every selected mission a level number.
        for index, mission in enumerate(self.missions, start=1):
            mission["id"] = index

    # ============================================================
    # CURRENT MISSION
    # ============================================================

    def get_current_mission(self):

        return self.missions[
            self.current_mission - 1
        ]

    # ============================================================
    # SUBMIT ANSWER
    # ============================================================

    def submit_answer(
        self,
        answer,
        ai_prediction
    ):

        mission = self.get_current_mission()

        correct = (
            answer == mission["answer"]
        )

        if correct:
            points = mission["points"]
        else:
            points = 0

        self.player.record_attempt(
            correct,
            points
        )

        result = {

            "mission": mission["title"],

            "answer": answer,

            "correct": correct,

            "points": points,

            "score": self.player.score
        }

        self.current_mission += 1

        return result

    # ============================================================
    # PLAYER STATS
    # ============================================================

    def get_player_stats(self):

        return self.player.get_stats()

    # ============================================================
    # MORE MISSIONS?
    # ============================================================

    def has_more_missions(self):

        return (
            self.current_mission
            <= len(self.missions)
        )

    # ============================================================
    # TOTAL MISSIONS
    # ============================================================

    def get_total_missions(self):

        return len(self.missions)