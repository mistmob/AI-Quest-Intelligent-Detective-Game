import csv
import os
from datetime import datetime


class DataManager:
    def __init__(self, filename=None):

        # Get the main project folder
        project_folder = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # Store dataset in the project's datasets folder
        if filename is None:
            filename = os.path.join(
                project_folder,
                "datasets",
                "game_data.csv"
            )

        self.filename = filename

        folder = os.path.dirname(self.filename)

        if folder:
            os.makedirs(folder, exist_ok=True)

        self._create_file()
    # ============================================================
    # CREATE DATASET FILE
    # ============================================================

    def _create_file(self):

        if not os.path.exists(self.filename):

            with open(
                self.filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "date_time",
                    "player",
                    "mission",
                    "answer",
                    "correct",
                    "points",
                    "score",
                    "ai_prediction",
                    "dangerous_votes",
                    "naive_bayes_probability",
                    "logistic_regression_probability",
                    "random_forest_probability"
                ])

    # ============================================================
    # SAVE GAME RESULT
    # ============================================================

    def save_result(self, player_name, result):

        with open(
            self.filename,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                player_name,

                result.get(
                    "mission_id",
                    ""
                ),

                result.get(
                    "answer",
                    ""
                ),

                result.get(
                    "correct",
                    False
                ),

                result.get(
                    "points",
                    0
                ),

                result.get(
                    "score",
                    0
                ),

                result.get(
                    "ai_prediction",
                    ""
                ),

                result.get(
                    "dangerous_votes",
                    0
                ),

                result.get(
                    "naive_bayes_probability",
                    0
                ),

                result.get(
                    "logistic_regression_probability",
                    0
                ),

                result.get(
                    "random_forest_probability",
                    0
                )
            ])