import tkinter as tk
import os
from character import DetectiveCharacter

def main():

    root = tk.Tk()

    root.title("AI QUEST — Character Test")
    root.geometry("1000x650")
    root.configure(bg="#0b1020")

    canvas = tk.Canvas(
        root,
        width=1000,
        height=650,
        bg="#0b1020",
        highlightthickness=0
    )

    canvas.pack()

    # ============================================================
    # TITLE
    # ============================================================

    canvas.create_text(
        500,
        40,
        text="AI QUEST — DETECTIVE CHARACTER TEST",
        fill="#00e5ff",
        font=("Segoe UI", 22, "bold")
    )

    canvas.create_text(
        500,
        75,
        text="Choose your detective",
        fill="#9aa4bf",
        font=("Segoe UI", 11)
    )

    # ============================================================
    # BOY
    # ============================================================

    boy = DetectiveCharacter(
    canvas,
    os.path.join(os.path.dirname(__file__), "characters", "boy.png"),
    x=300,
    y=330,
    name="FINN"
)
    # ============================================================
    # GIRL
    # ============================================================

    girl = DetectiveCharacter(
    canvas,
    os.path.join(os.path.dirname(__file__), "characters", "girl.png"),
    x=700,
    y=330,
    name="PIXIE"
)

    # ============================================================
    # BUTTONS
    # ============================================================

    button_frame = tk.Frame(
        root,
        bg="#0b1020"
    )

    button_frame.place(
        x=0,
        y=560,
        width=1000
    )

    tk.Button(
        button_frame,
        text="BOY",
        command=lambda: boy.say(
            "Let's solve this case. 🔎"
        ),
        font=("Segoe UI", 11, "bold"),
        bg="#1d2742",
        fg="#00e5ff",
        activebackground="#00e5ff",
        activeforeground="#0b1020",
        relief="flat",
        width=15,
        height=2
    ).pack(
        side="left",
        padx=30
    )

    tk.Button(
        button_frame,
        text="GIRL",
        command=lambda: girl.say(
            "Something suspicious is going on... 🕵️"
        ),
        font=("Segoe UI", 11, "bold"),
        bg="#1d2742",
        fg="#00e5ff",
        activebackground="#00e5ff",
        activeforeground="#0b1020",
        relief="flat",
        width=15,
        height=2
    ).pack(
        side="right",
        padx=30
    )

    # ============================================================
    # MOVE CHARACTERS
    # ============================================================

    def move_boy():

        boy.move(5, 0)

        if boy.x < 900:
            root.after(80, move_boy)

    def move_girl():

        girl.move(-5, 0)

        if girl.x > 100:
            root.after(80, move_girl)

    # Start movement
    root.after(1000, move_boy)
    root.after(1000, move_girl)

    root.mainloop()


if __name__ == "__main__":
    main()