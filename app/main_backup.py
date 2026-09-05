
import tkinter as tk
from tkinter import messagebox

from game.game_engine import GameEngine
from data.data_manager import DataManager
from ai.threat_detector import ThreatDetector
from ai.model_comparison import AIModelComparison


class AIQuest:

    def __init__(self, root):
        self.root = root

        self.root.title("AI QUEST - Intelligent Detective")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.game = None

        self.data_manager = DataManager()
        self.threat_detector = ThreatDetector()
        self.model_comparison = AIModelComparison()

        self.setup_home_screen()

    # ---------------------------------------------------------
    # CLEAR SCREEN
    # ---------------------------------------------------------

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # HOME SCREEN
    # ---------------------------------------------------------

    def setup_home_screen(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="⚡ AI QUEST ⚡",
            font=("Arial", 36, "bold")
        ).pack(pady=(70, 10))

        tk.Label(
            self.root,
            text="THE INTELLIGENT DETECTIVE",
            font=("Arial", 18)
        ).pack(pady=10)

        tk.Label(
            self.root,
            text=(
                "Investigate digital evidence using "
                "Artificial Intelligence."
            ),
            font=("Arial", 14)
        ).pack(pady=25)

        tk.Label(
            self.root,
            text="ENTER DETECTIVE NAME",
            font=("Arial", 13, "bold")
        ).pack(pady=(30, 5))

        self.name_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            width=30
        )

        self.name_entry.pack(pady=10)

        tk.Button(
            self.root,
            text="START INVESTIGATION",
            font=("Arial", 14, "bold"),
            padx=35,
            pady=12,
            command=self.start_game
        ).pack(pady=30)

    # ---------------------------------------------------------
    # START GAME
    # ---------------------------------------------------------

    def start_game(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Name Required",
                "Please enter your detective name."
            )
            return

        self.game = GameEngine(name)

        self.show_dashboard()

    # ---------------------------------------------------------
    # DASHBOARD
    # ---------------------------------------------------------

    def show_dashboard(self):
        self.clear_screen()

        stats = self.game.get_player_stats()

        tk.Label(
            self.root,
            text="AI QUEST — DETECTIVE DASHBOARD",
            font=("Arial", 26, "bold")
        ).pack(pady=30)

        tk.Label(
            self.root,
            text=f"Detective: {stats['name']}",
            font=("Arial", 15)
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"Score: {stats['score']}",
            font=("Arial", 15)
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"Accuracy: {stats['accuracy']:.1f}%",
            font=("Arial", 15)
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"Missions Completed: {stats['missions_completed']}",
            font=("Arial", 15)
        ).pack(pady=5)

        mission = self.game.get_current_mission()

        if self.game.has_more_missions():

            tk.Label(
                self.root,
                text=f"MISSION {mission['id']}",
                font=("Arial", 20, "bold")
            ).pack(pady=(40, 5))

            tk.Label(
                self.root,
                text=mission["title"],
                font=("Arial", 16)
            ).pack(pady=5)

            tk.Label(
                self.root,
                text=f"Difficulty: {mission['difficulty']}",
                font=("Arial", 12)
            ).pack(pady=5)

            tk.Button(
                self.root,
                text="INVESTIGATE EVIDENCE",
                font=("Arial", 14, "bold"),
                padx=30,
                pady=12,
                command=self.start_mission
            ).pack(pady=25)

        else:

            tk.Label(
                self.root,
                text="🎉 ALL MISSIONS COMPLETED!",
                font=("Arial", 20, "bold")
            ).pack(pady=50)

    # ---------------------------------------------------------
    # MISSION
    # ---------------------------------------------------------

    def start_mission(self):
        self.clear_screen()

        mission = self.game.get_current_mission()

        evidence = mission["evidence"]

        tk.Label(
            self.root,
            text=f"MISSION {mission['id']} — {mission['title']}",
            font=("Arial", 24, "bold")
        ).pack(pady=30)

        tk.Label(
            self.root,
            text=f"DIFFICULTY: {mission['difficulty']}",
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"REWARD: {mission['points']} POINTS",
            font=("Arial", 13, "bold")
        ).pack(pady=5)

        tk.Label(
            self.root,
            text="DIGITAL EVIDENCE",
            font=("Arial", 15, "bold")
        ).pack(pady=10)

        evidence_box = tk.Text(
            self.root,
            height=8,
            width=85,
            font=("Arial", 13),
            wrap="word"
        )

        evidence_box.insert("1.0", evidence)
        evidence_box.config(state="disabled")
        evidence_box.pack(pady=15)

        tk.Label(
            self.root,
            text=(
                "Analyze the evidence using the "
                "AI threat detection system."
            ),
            font=("Arial", 13)
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="🧠 ANALYZE WITH AI",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            command=lambda: self.analyze_evidence(evidence)
        ).pack(pady=20)

    # ---------------------------------------------------------
    # AI ANALYSIS
    # ---------------------------------------------------------

    def analyze_evidence(self, evidence):

        result = self.model_comparison.final_decision(
            evidence
        )

        final_prediction = result["final_decision"]

        models = result["models"]

        self.clear_screen()

        tk.Label(
            self.root,
            text="🧠 AI MODEL COMPARISON",
            font=("Arial", 26, "bold")
        ).pack(pady=25)

        tk.Label(
            self.root,
            text="THREAT ANALYSIS",
            font=("Arial", 15, "bold")
        ).pack(pady=5)

        for model_name, model_result in models.items():

            prediction = model_result["prediction"].upper()

            confidence = max(
                model_result["safe_probability"],
                model_result["dangerous_probability"]
            ) * 100

            tk.Label(
                self.root,
                text=(
                    f"{model_name}: "
                    f"{prediction} "
                    f"({confidence:.1f}%)"
                ),
                font=("Arial", 14)
            ).pack(pady=5)

        tk.Label(
            self.root,
            text="────────────────────────────",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(
            self.root,
            text=(
                f"AI CONSENSUS: "
                f"{result['dangerous_votes']} / 3 "
                f"dangerous"
            ),
            font=("Arial", 16, "bold")
        ).pack(pady=8)

        tk.Label(
            self.root,
            text=(
                f"FINAL AI DECISION: "
                f"{final_prediction.upper()}"
            ),
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        tk.Label(
            self.root,
            text="Make your final detective decision:",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="🚨 DANGEROUS",
            font=("Arial", 13, "bold"),
            width=20,
            command=lambda: self.submit_decision(
                "dangerous",
                final_prediction,
                result
            )
        ).pack(pady=8)

        tk.Button(
            self.root,
            text="✅ SAFE",
            font=("Arial", 13, "bold"),
            width=20,
            command=lambda: self.submit_decision(
                "safe",
                final_prediction,
                result
            )
        ).pack(pady=8)

    # ---------------------------------------------------------
    # SUBMIT DECISION
    # ---------------------------------------------------------

    def submit_decision(
        self,
        answer,
        prediction,
        ai_result
    ):

        result = self.game.submit_answer(
            answer,
            prediction
        )

        result["ai_prediction"] = prediction

        model_results = ai_result["models"]

        result["naive_bayes_probability"] = (
            model_results["Naive Bayes"]
            ["dangerous_probability"]
        )

        result["logistic_regression_probability"] = (
            model_results["Logistic Regression"]
            ["dangerous_probability"]
        )

        result["random_forest_probability"] = (
            model_results["Random Forest"]
            ["dangerous_probability"]
        )

        result["dangerous_votes"] = (
            ai_result["dangerous_votes"]
        )

        self.data_manager.save_result(
            self.game.player.name,
            result
        )

        if result["correct"]:

            messagebox.showinfo(
                "Correct Decision",
                (
                    "Excellent detective work!\n\n"
                    f"AI Consensus: "
                    f"{ai_result['dangerous_votes']}/3 "
                    "models detected danger.\n\n"
                    f"+{result['points']} points"
                )
            )

        else:

            messagebox.showwarning(
                "Incorrect Decision",
                (
                    "The AI consensus classified "
                    f"this evidence as "
                    f"{prediction.upper()}."
                )
            )

        self.show_dashboard()


# -------------------------------------------------------------
# PROGRAM ENTRY POINT
# -------------------------------------------------------------

def main():

    root = tk.Tk()

    AIQuest(root)

    root.mainloop()


if __name__ == "__main__":
    main()

