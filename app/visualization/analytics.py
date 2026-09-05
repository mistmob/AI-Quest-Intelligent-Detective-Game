import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class GameAnalytics:

    def __init__(self, data_file="datasets/game_data.csv"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            return pd.DataFrame()

        df = pd.read_csv(self.data_file)

        if df.empty:
            return df

        return df

    def get_summary(self):
        if self.data.empty:
            return {
                "total_attempts": 0,
                "correct_answers": 0,
                "accuracy": 0,
                "average_score": 0
            }

        total_attempts = len(self.data)

        correct_answers = int(
            self.data["correct"].sum()
        )

        accuracy = (
            correct_answers / total_attempts
        ) * 100

        average_score = float(
            self.data["score"].mean()
        )

        return {
            "total_attempts": total_attempts,
            "correct_answers": correct_answers,
            "accuracy": accuracy,
            "average_score": average_score
        }

    def get_score_array(self):
        if self.data.empty:
            return np.array([])

        return np.array(
            self.data["score"]
        )

    def create_performance_chart(
        self,
        output_file="screenshots/performance_chart.png"
    ):

        if self.data.empty:
            return None

        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        plt.figure(figsize=(10, 6))

        plt.plot(
            range(1, len(self.data) + 1),
            self.data["score"],
            marker="o"
        )

        plt.title(
            "AI Quest - Player Performance"
        )

        plt.xlabel("Investigation Attempt")
        plt.ylabel("Score")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(output_file)

        plt.close()

        return output_file

    def create_accuracy_chart(
        self,
        output_file="screenshots/accuracy_chart.png"
    ):

        if self.data.empty:
            return None

        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        accuracy_values = (
            self.data["correct"]
            .astype(int)
            .cumsum()
            /
            np.arange(1, len(self.data) + 1)
        ) * 100

        plt.figure(figsize=(10, 6))

        plt.plot(
            accuracy_values,
            marker="o"
        )

        plt.title(
            "AI Quest - Accuracy Progress"
        )

        plt.xlabel("Investigation Attempt")
        plt.ylabel("Accuracy (%)")

        plt.ylim(0, 100)

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(output_file)

        plt.close()

        return output_file

    def create_threat_distribution(
        self,
        output_file="screenshots/threat_distribution.png"
    ):

        if self.data.empty:
            return None

        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        plt.figure(figsize=(8, 6))

        sns.countplot(
            data=self.data,
            x="ai_prediction"
        )

        plt.title(
            "AI Threat Classification Distribution"
        )

        plt.xlabel("Classification")
        plt.ylabel("Number of Cases")

        plt.tight_layout()

        plt.savefig(output_file)

        plt.close()

        return output_file