import tkinter as tk
from tkinter import messagebox

from game.game_engine import GameEngine
from data.data_manager import DataManager
from ai.threat_detector import ThreatDetector
from ai.model_comparison import AIModelComparison


class AIQuest:

    # ============================================================
    # COLORS
    # ============================================================

    BG = "#0b1020"
    PANEL = "#151c32"
    PANEL_LIGHT = "#1d2742"
    CYAN = "#00e5ff"
    GREEN = "#00e676"
    RED = "#ff5252"
    GOLD = "#ffd740"
    TEXT = "#f5f7ff"
    MUTED = "#9aa4bf"
    WHITE = "#ffffff"
    PURPLE = "#9c7cff"

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, root):

        self.root = root

        self.root.title("AI QUEST — Intelligent Detective")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        self.game = None

        self.data_manager = DataManager()
        self.threat_detector = ThreatDetector()
        self.model_comparison = AIModelComparison()

        self.setup_home_screen()

    # ============================================================
    # BASIC UI HELPERS
    # ============================================================

    def clear_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def make_label(
        self,
        parent,
        text,
        size=12,
        bold=False,
        color=None
    ):

        font_style = "bold" if bold else "normal"

        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size, font_style),
            fg=color if color else self.TEXT,
            bg=parent.cget("bg"),
            justify="center"
        )

    def make_button(
        self,
        parent,
        text,
        command,
        width=20,
        bg=None,
        fg=None
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 12, "bold"),
            width=width,
            height=2,
            bg=bg if bg else self.PANEL_LIGHT,
            fg=fg if fg else self.TEXT,
            activebackground=self.CYAN,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

    # ============================================================
    # HOME SCREEN
    # ============================================================

    def setup_home_screen(self):

        self.clear_screen()

        header = tk.Frame(
            self.root,
            bg=self.BG
        )
        header.pack(fill="x", pady=(45, 0))

        self.make_label(
            header,
            "⚡ AI QUEST ⚡",
            38,
            True,
            self.CYAN
        ).pack()

        self.make_label(
            header,
            "THE INTELLIGENT DETECTIVE",
            17,
            True,
            self.TEXT
        ).pack(pady=(5, 0))

        self.make_label(
            header,
            "AI-POWERED DIGITAL THREAT INVESTIGATION",
            10,
            False,
            self.MUTED
        ).pack(pady=(8, 0))

        panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=700,
            height=390
        )

        panel.pack(pady=30)
        panel.pack_propagate(False)

        self.make_label(
            panel,
            "WELCOME, DETECTIVE",
            22,
            True,
            self.GOLD
        ).pack(pady=(35, 10))

        self.make_label(
            panel,
            "Investigate suspicious digital evidence.",
            13,
            False,
            self.TEXT
        ).pack(pady=5)

        self.make_label(
            panel,
            "Use AI-powered threat detection to uncover the truth.",
            11,
            False,
            self.MUTED
        ).pack(pady=5)

        self.make_label(
            panel,
            "ENTER DETECTIVE NAME",
            12,
            True,
            self.CYAN
        ).pack(pady=(30, 7))

        self.name_entry = tk.Entry(
            panel,
            font=("Segoe UI", 14),
            width=32,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            insertbackground=self.CYAN,
            relief="flat",
            justify="center"
        )

        self.name_entry.pack(ipady=9)

        self.make_button(
            panel,
            "🚀 START INVESTIGATION",
            self.start_game,
            28,
            self.CYAN,
            self.BG
        ).pack(pady=25)

    # ============================================================
    # START GAME
    # ============================================================

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

    # ============================================================
    # DASHBOARD
    # ============================================================

    def show_dashboard(self):

        self.clear_screen()

        stats = self.game.get_player_stats()

        current_mission = self.game.get_current_mission()

        # Header
        self.make_label(
            self.root,
            "🕵️ AI QUEST",
            30,
            True,
            self.CYAN
        ).pack(pady=(25, 2))

        self.make_label(
            self.root,
            "DETECTIVE DASHBOARD",
            14,
            True,
            self.MUTED
        ).pack()

        # Detective information
        info_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=850,
            height=100
        )

        info_panel.pack(pady=20)
        info_panel.pack_propagate(False)

        self.make_label(
            info_panel,
            f"DETECTIVE  •  {stats['name']}",
            13,
            True,
            self.TEXT
        ).pack(pady=(18, 5))

        stats_text = (
            f"SCORE  {stats['score']}     •     "
            f"ACCURACY  {stats['accuracy']:.1f}%     •     "
            f"MISSIONS  {stats['missions_completed']}/3"
        )

        self.make_label(
            info_panel,
            stats_text,
            11,
            False,
            self.CYAN
        ).pack()

        # Mission panel
        mission_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=850,
            height=330
        )

        mission_panel.pack(pady=5)
        mission_panel.pack_propagate(False)

        self.make_label(
            mission_panel,
            f"MISSION {current_mission['id']}",
            14,
            True,
            self.GOLD
        ).pack(pady=(25, 5))

        self.make_label(
            mission_panel,
            current_mission["title"],
            25,
            True,
            self.TEXT
        ).pack(pady=5)

        self.make_label(
            mission_panel,
            f"DIFFICULTY  •  {current_mission['difficulty']}",
            11,
            True,
            self.PURPLE
        ).pack(pady=5)

        self.make_label(
            mission_panel,
            f"REWARD  •  {current_mission['points']} POINTS",
            11,
            False,
            self.MUTED
        ).pack(pady=5)

        # BIG INVESTIGATE BUTTON
        self.make_button(
            mission_panel,
            "🔎  INVESTIGATE EVIDENCE",
            self.start_mission,
            32,
            self.CYAN,
            self.BG
        ).pack(pady=22)

    # ============================================================
    # START MISSION
    # ============================================================

    def start_mission(self):

        if not self.game:
            return

        # Safety check
        if not self.game.has_more_missions():
            self.show_final_screen()
            return

        self.clear_screen()

        mission = self.game.get_current_mission()

        # Header
        self.make_label(
            self.root,
            f"MISSION {mission['id']}",
            15,
            True,
            self.GOLD
        ).pack(pady=(25, 5))

        self.make_label(
            self.root,
            mission["title"],
            28,
            True,
            self.CYAN
        ).pack()

        self.make_label(
            self.root,
            f"DIFFICULTY  •  {mission['difficulty']}",
            10,
            True,
            self.MUTED
        ).pack(pady=5)

        # Evidence panel
        evidence_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=850,
            height=280
        )

        evidence_panel.pack(pady=20)
        evidence_panel.pack_propagate(False)

        self.make_label(
            evidence_panel,
            "📁 DIGITAL EVIDENCE",
            14,
            True,
            self.GOLD
        ).pack(pady=(18, 8))

        evidence_box = tk.Text(
            evidence_panel,
            height=7,
            width=88,
            font=("Consolas", 12),
            wrap="word",
            bg="#10172a",
            fg=self.TEXT,
            insertbackground=self.CYAN,
            relief="flat",
            padx=15,
            pady=12
        )

        evidence_box.insert(
            "1.0",
            mission["evidence"]
        )

        evidence_box.config(state="disabled")

        evidence_box.pack()

        self.make_label(
            self.root,
            "Analyze the evidence before making your final decision.",
            11,
            False,
            self.MUTED
        ).pack(pady=5)

        self.make_button(
            self.root,
            "🧠  ANALYZE WITH AI",
            lambda: self.analyze_evidence(
                mission["evidence"]
            ),
            28,
            self.PURPLE,
            self.WHITE
        ).pack(pady=15)

    # ============================================================
    # AI ANALYSIS
    # ============================================================

    def analyze_evidence(self, evidence):

        result = self.model_comparison.final_decision(
            evidence
        )

        final_prediction = result["final_decision"]

        models = result["models"]

        self.clear_screen()

        self.make_label(
            self.root,
            "🧠 AI ANALYSIS",
            28,
            True,
            self.CYAN
        ).pack(pady=(25, 3))

        self.make_label(
            self.root,
            "THREAT DETECTION • MODEL COMPARISON",
            11,
            True,
            self.MUTED
        ).pack()

        # Models panel
        models_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=850,
            height=280
        )

        models_panel.pack(pady=25)
        models_panel.pack_propagate(False)

        self.make_label(
            models_panel,
            "AI MODEL RESULTS",
            15,
            True,
            self.GOLD
        ).pack(pady=(18, 10))

        for model_name, model_result in models.items():

            prediction = str(
                model_result["prediction"]
            ).upper()

            confidence = max(
                model_result["safe_probability"],
                model_result["dangerous_probability"]
            ) * 100

            if prediction == "DANGEROUS":
                color = self.RED
                icon = "🚨"
            else:
                color = self.GREEN
                icon = "✅"

            row = tk.Frame(
                models_panel,
                bg=self.PANEL
            )

            row.pack(pady=4)

            self.make_label(
                row,
                f"{icon} {model_name}",
                12,
                True,
                self.TEXT
            ).pack(side="left", padx=10)

            self.make_label(
                row,
                prediction,
                12,
                True,
                color
            ).pack(side="left", padx=10)

            self.make_label(
                row,
                f"{confidence:.1f}% confidence",
                11,
                False,
                self.MUTED
            ).pack(side="left", padx=10)

        # Consensus
        dangerous_votes = result["dangerous_votes"]

        self.make_label(
            self.root,
            f"AI CONSENSUS  •  {dangerous_votes}/3 MODELS DETECTED DANGER",
            14,
            True,
            self.GOLD
        ).pack(pady=5)

        decision_color = (
            self.RED
            if final_prediction == "dangerous"
            else self.GREEN
        )

        self.make_label(
            self.root,
            f"FINAL AI DECISION  •  {final_prediction.upper()}",
            21,
            True,
            decision_color
        ).pack(pady=8)

        self.make_label(
            self.root,
            "MAKE YOUR FINAL DETECTIVE DECISION",
            12,
            True,
            self.TEXT
        ).pack(pady=(8, 5))

        # Decision buttons
        buttons = tk.Frame(
            self.root,
            bg=self.BG
        )

        buttons.pack(pady=10)

        dangerous_button = self.make_button(
            buttons,
            "🚨  DANGEROUS",
            lambda: self.submit_decision(
                "dangerous",
                final_prediction,
                result
            ),
            20,
            self.RED,
            self.WHITE
        )

        dangerous_button.pack(
            side="left",
            padx=15
        )

        safe_button = self.make_button(
            buttons,
            "✅  SAFE",
            lambda: self.submit_decision(
                "safe",
                final_prediction,
                result
            ),
            20,
            self.GREEN,
            self.BG
        )

        safe_button.pack(
            side="left",
            padx=15
        )

    # ============================================================
    # SUBMIT DECISION
    # ============================================================

    def submit_decision(
        self,
        answer,
        prediction,
        ai_result
    ):

        # IMPORTANT:
        # Prevent accidental extra submissions after Mission 3.
        if not self.game:
            return

        if not self.game.has_more_missions():
            return

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

        # Success message
        if result["correct"]:

            messagebox.showinfo(
                "MISSION SUCCESS",
                (
                    "Excellent detective work!\n\n"
                    f"AI Consensus: "
                    f"{ai_result['dangerous_votes']}/3 "
                    "models detected danger.\n\n"
                    f"+{result['points']} POINTS\n\n"
                    f"Total Score: {result['score']}"
                )
            )

        else:

            messagebox.showwarning(
                "MISSION FAILED",
                (
                    f"The correct classification was "
                    f"{self.game.missions[result['mission_index'] if 'mission_index' in result else self.game.current_mission - 2]['answer'].upper()}.\n\n"
                    f"AI classified it as "
                    f"{prediction.upper()}."
                )
            )

        # ========================================================
        # CRITICAL NAVIGATION
        # ========================================================

        if self.game.has_more_missions():

            # Missions 1 → 2 → 3
            self.show_dashboard()

        else:

            # Mission 3 → FINAL SCREEN
            self.show_final_screen()

    # ============================================================
    # FINAL SCREEN
    # ============================================================

    def show_final_screen(self):

        self.clear_screen()

        stats = self.game.get_player_stats()

        # Header
        self.make_label(
            self.root,
            "🎉",
            42,
            True,
            self.GOLD
        ).pack(pady=(35, 0))

        self.make_label(
            self.root,
            "INVESTIGATION COMPLETE",
            30,
            True,
            self.CYAN
        ).pack(pady=5)

        self.make_label(
            self.root,
            "ALL DIGITAL CASES HAVE BEEN SOLVED",
            11,
            True,
            self.MUTED
        ).pack()

        # Results panel
        panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=720,
            height=350
        )

        panel.pack(pady=30)
        panel.pack_propagate(False)

        self.make_label(
            panel,
            f"CONGRATULATIONS, DETECTIVE {stats['name'].upper()}!",
            17,
            True,
            self.TEXT
        ).pack(pady=(30, 15))

        # Score
        self.make_label(
            panel,
            "FINAL SCORE",
            11,
            True,
            self.MUTED
        ).pack()

        self.make_label(
            panel,
            str(stats["score"]),
            40,
            True,
            self.GOLD
        ).pack()

        # Accuracy
        self.make_label(
            panel,
            f"ACCURACY  •  {stats['accuracy']:.1f}%",
            15,
            True,
            self.CYAN
        ).pack(pady=5)

        # Missions
        self.make_label(
            panel,
            f"MISSIONS COMPLETED  •  "
            f"{stats['missions_completed']}/3",
            12,
            False,
            self.TEXT
        ).pack(pady=5)

        # Correct answers
        self.make_label(
            panel,
            f"CORRECT DECISIONS  •  "
            f"{stats['correct_answers']}/{stats['attempts']}",
            12,
            False,
            self.GREEN
        ).pack(pady=5)

        self.make_label(
            panel,
            "You successfully completed the AI Quest investigation.",
            10,
            False,
            self.MUTED
        ).pack(pady=12)

        self.make_button(
            panel,
            "🔄  NEW INVESTIGATION",
            self.setup_home_screen,
            28,
            self.CYAN,
            self.BG
        ).pack(pady=15)


# ================================================================
# MAIN
# ================================================================

def main():

    root = tk.Tk()

    app = AIQuest(root)

    root.mainloop()


if __name__ == "__main__":
    main()