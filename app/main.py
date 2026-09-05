import tkinter as tk
from tkinter import messagebox
import os

from PIL import Image, ImageTk

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
    # CHARACTER SPRITE SETTINGS
    # ============================================================

    # Your character PNGs are sprite sheets.
    # Each individual frame is assumed to be 64 x 64 pixels.
    FRAME_WIDTH = 64
    FRAME_HEIGHT = 64

    # Front-facing row.
    # Change this to 0, 1, 2, etc. if your sprite sheet
    # has the front-facing character on another row.
    FRONT_ROW = 2

    # First frame from the row.
    FRONT_COLUMN = 0

    # Preview size on the home screen.
    CHARACTER_SIZE = 400

    # Number of animation frames.
    ANIMATION_FRAME_COUNT = 4

    # Animation speed in milliseconds.
    ANIMATION_DELAY = 180

    # ============================================================
    # LEVEL CHARACTER SETTINGS
    # ============================================================

    # Size of the character shown on level/game screens.
    # This does NOT affect the home screen character.
    LEVEL_CHARACTER_SIZE = 250

    # Animation speed for the level character.
    LEVEL_CHARACTER_DELAY = 180
    FINAL_CHARACTER_DELAY = 120
        # ============================================================
    # LEVEL-SPECIFIC CHARACTER DIALOGUES
    # ============================================================

    CHARACTER_DIALOGUES = {

    "FLINN": {
        1: "Something feels off here... Let's examine the evidence.",
        2: "We've uncovered another clue. Stay sharp, Detective!",
        3: "The investigation is getting interesting. Keep going!",
        4: "Another case, another mystery. Let's find the truth.",
        5: "We're halfway through. Don't miss the hidden clues!",
        6: "The evidence is getting more suspicious. Stay sharp!",
        7: "We're getting close to the truth. Trust your instincts!",
        8: "Only a few cases remain. Keep investigating!",
        9: "Almost there, Detective. One more step toward the truth!",
        10: "This is the final case. Let's crack it!"
    },

    "PIXIE": {
        1: "Hmm... I think there's a hidden threat in this evidence.",
        2: "Interesting! The clues are getting more suspicious.",
        3: "The mystery is getting deeper. Let's investigate!",
        4: "Something doesn't add up here. Look closely!",
        5: "We're halfway there. Keep your detective senses sharp!",
        6: "I have a feeling we're getting closer to the truth.",
        7: "The evidence is pointing somewhere. Let's follow it!",
        8: "We're almost there. Don't overlook anything!",
        9: "Just one more case after this. We've got this!",
        10: "Final investigation! Trust your instincts, Detective!"
    }
}

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, root):

        self.root = root

        self.root.title("AI QUEST — Intelligent Detective")
        self.root.attributes("-fullscreen", True)

        self.root.bind(
            "<Escape>",
            lambda event: self.root.attributes(
                "-fullscreen",
                False
            )
        )

        self.root.configure(bg=self.BG)

        self.game = None

        self.data_manager = DataManager()
        self.threat_detector = ThreatDetector()
        self.model_comparison = AIModelComparison()

        self.active_mission_id = None

        # Character selection
        self.selected_character = None
        self.selected_character_name = None

        # Keep PhotoImage objects alive.
        self.character_preview_images = {}

        # Keep animation frames alive.
        self.character_animation_frames = {}

        # Keep animation jobs.
        self.animation_jobs = {}

        # Buttons for character selection
        self.character_buttons = {}

        self.setup_home_screen()

    # ============================================================
    # BASIC UI HELPERS
    # ============================================================

    def clear_screen(self):

        # --------------------------------------------------------
        # Stop any currently running character animations.
        # --------------------------------------------------------

        for job in self.animation_jobs.values():

            try:
                self.root.after_cancel(job)
            except Exception:
                pass

        self.animation_jobs = {}

        for widget in self.root.winfo_children():
            widget.destroy()

        self.character_preview_images = {}
        self.character_animation_frames = {}
        self.character_buttons = {}

    # ------------------------------------------------------------

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

    # ------------------------------------------------------------

    def make_button(
        self,
        parent,
        text,
        command,
        width=20,
        bg=None,
        fg=None,
        height=2
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 12, "bold"),
            width=width,
            height=height,
            bg=bg if bg else self.PANEL_LIGHT,
            fg=fg if fg else self.TEXT,
            activebackground=self.CYAN,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

    # ============================================================
    # CHARACTER IMAGE LOADER
    # ============================================================

    def load_character_preview(self, image_path):

        """
        Loads ONE character from a sprite sheet.

        Steps:
        1. Open PNG.
        2. Crop one 64x64 sprite frame.
        3. Remove transparent empty space.
        4. Resize the actual character.
        """

        if not os.path.exists(image_path):

            messagebox.showerror(
                "Character File Missing",
                f"Could not find:\n{image_path}"
            )

            return None

        try:

            image = Image.open(image_path).convert("RGBA")

            # ----------------------------------------------------
            # Make sure the requested frame exists.
            # ----------------------------------------------------

            left = self.FRONT_COLUMN * self.FRAME_WIDTH
            top = self.FRONT_ROW * self.FRAME_HEIGHT

            right = left + self.FRAME_WIDTH
            bottom = top + self.FRAME_HEIGHT

            if (
                right > image.width
                or bottom > image.height
            ):

                messagebox.showerror(
                    "Sprite Sheet Error",
                    (
                        f"The sprite sheet is too small.\n\n"
                        f"File: {image_path}\n"
                        f"Image size: "
                        f"{image.width} x {image.height}\n"
                        f"Required frame ends at: "
                        f"{right} x {bottom}"
                    )
                )

                return None

            # ----------------------------------------------------
            # Crop ONE sprite frame.
            # ----------------------------------------------------

            frame = image.crop(
                (
                    left,
                    top,
                    right,
                    bottom
                )
            )

            # ----------------------------------------------------
            # Automatically remove transparent empty space.
            # ----------------------------------------------------

            alpha = frame.getchannel("A")

            bbox = alpha.getbbox()

            if bbox:
                frame = frame.crop(bbox)

            # ----------------------------------------------------
            # Resize the actual character.
            # ----------------------------------------------------

            frame.thumbnail(
                (
                    self.CHARACTER_SIZE,
                    self.CHARACTER_SIZE
                ),
                Image.Resampling.NEAREST
            )

            # ----------------------------------------------------
            # Put character into a fixed-size transparent canvas.
            # This keeps both characters centered.
            # ----------------------------------------------------

            canvas = Image.new(
                "RGBA",
                (
                    self.CHARACTER_SIZE,
                    self.CHARACTER_SIZE
                ),
                (0, 0, 0, 0)
            )

            x = (
                self.CHARACTER_SIZE - frame.width
            ) // 2

            y = (
                self.CHARACTER_SIZE - frame.height
            ) // 2

            canvas.alpha_composite(
                frame,
                (x, y)
            )

            return ImageTk.PhotoImage(canvas)

        except Exception as error:

            messagebox.showerror(
                "Character Image Error",
                (
                    f"Could not load character image.\n\n"
                    f"{image_path}\n\n"
                    f"Error:\n{error}"
                )
            )

            return None

    # ============================================================
    # CHARACTER ANIMATION
    # ============================================================

    def get_character_frames(
        self,
        image_path,
        row,
        frame_count=4
    ):

        if not os.path.exists(image_path):
            return []

        try:

            image = Image.open(
                image_path
            ).convert("RGBA")

            frames = []

            for column in range(frame_count):

                left = column * self.FRAME_WIDTH
                top = row * self.FRAME_HEIGHT

                right = left + self.FRAME_WIDTH
                bottom = top + self.FRAME_HEIGHT

                if (
                    right > image.width
                    or bottom > image.height
                ):
                    break

                # ------------------------------------------------
                # Crop animation frame.
                # ------------------------------------------------

                frame = image.crop(
                    (
                        left,
                        top,
                        right,
                        bottom
                    )
                )

                # ------------------------------------------------
                # Remove transparent empty space.
                # ------------------------------------------------

                alpha = frame.getchannel("A")
                bbox = alpha.getbbox()

                if bbox:
                    frame = frame.crop(bbox)

                # ------------------------------------------------
                # Resize actual character.
                # ------------------------------------------------

                frame.thumbnail(
                    (
                        self.CHARACTER_SIZE,
                        self.CHARACTER_SIZE
                    ),
                    Image.Resampling.NEAREST
                )

                frame= frame.resize( (
                    int(frame.width * 1.8),
                    int(frame.height * 1.8)
                ),
                Image.Resampling.NEAREST )

                # ------------------------------------------------
                # Put character into fixed-size canvas.
                # ------------------------------------------------

                canvas = Image.new(
                    "RGBA",
                    (
                        self.CHARACTER_SIZE,
                        self.CHARACTER_SIZE
                    ),
                    (0, 0, 0, 0)
                )

                x = (
                    self.CHARACTER_SIZE - frame.width
                ) // 2

                y = (
                    self.CHARACTER_SIZE - frame.height
                ) // 2

                canvas.alpha_composite(
                    frame,
                    (x, y)
                )

                frames.append(
                    ImageTk.PhotoImage(canvas)
                )

            return frames

        except Exception as error:

            messagebox.showerror(
                "Animation Error",
                f"Could not load animation:\n\n{error}"
            )

            return []

    # ============================================================
    # CHARACTER ANIMATION PLAYER
    # ============================================================

    def animate_character(
        self,
        character_name,
        image_label,
        frames,
        frame_index=0
    ):

        if not frames:
            return

        try:

            image_label.configure(
                image=frames[frame_index]
            )

            self.character_animation_frames[
                character_name
            ] = frames

            next_frame = (
                frame_index + 1
            ) % len(frames)

            self.animation_jobs[
                character_name
            ] = self.root.after(
                self.ANIMATION_DELAY,
                lambda: self.animate_character(
                    character_name,
                    image_label,
                    frames,
                    next_frame
                )
            )

        except tk.TclError:

            return

    # ============================================================
    # LEVEL CHARACTER + DIALOGUE
    # ============================================================
        # ============================================================
    # GET CHARACTER DIALOGUE FOR CURRENT LEVEL
    # ============================================================

    def get_level_dialogue(self, level_id):

        selected_name = getattr(
            self.game,
            "selected_character",
            self.selected_character
        )

        if not selected_name:
            return "Let's investigate!"

        dialogues = self.CHARACTER_DIALOGUES.get(
            selected_name,
            {}
        )

        return dialogues.get(
            level_id,
            "Let's investigate!"
        )

    def show_level_character(
        self,
        dialogue="Let's investigate!"
    ):
        """
        Shows the currently selected character in the
        bottom-right corner of the current screen with
        an animated sprite and dialogue bubble.

        This is completely separate from the home-screen
        character animation.
        """

        if not self.game:
            return

        selected_name = getattr(
            self.game,
            "selected_character",
            self.selected_character
        )

        if not selected_name:
            return

        # --------------------------------------------------------
        # Character file
        # --------------------------------------------------------

        if selected_name == "PIXIE":

            image_filename = "girl.png"
            character_color = self.PURPLE

        else:

            image_filename = "boy.png"
            character_color = self.CYAN

        image_path = os.path.join(
            os.path.dirname(__file__),
            "characters",
            image_filename
        )

        if not os.path.exists(image_path):
            return

        # --------------------------------------------------------
        # Container
        # --------------------------------------------------------

        character_container = tk.Frame(
            self.root,
            bg=self.BG
        )

        character_container.place(
          relx=1.0,
          rely=1.0,
           anchor="se",
            x=-25,
            y=-20
)
        

        # --------------------------------------------------------
        # Dialogue bubble
        # --------------------------------------------------------

        bubble_frame = tk.Frame(
            character_container,
            bg=self.WHITE,
            padx=14,
            pady=10,
            highlightthickness=2,
            highlightbackground=character_color
        )

        bubble_frame.pack(
            anchor="e",
            padx=(0, 5),
            pady=(0, 2)
        )

        dialogue_label = tk.Label(
            bubble_frame,
            text=dialogue,
            font=("Segoe UI", 11, "bold"),
            fg=self.BG,
            bg=self.WHITE,
            wraplength=240,
            justify="left"
        )

        dialogue_label.pack()

        # --------------------------------------------------------
        # Character image
        # --------------------------------------------------------

        image_label = tk.Label(
            character_container,
            bg=self.BG
        )

        image_label.pack(
            anchor="e",
            padx=0,
            pady=0
        )

        # --------------------------------------------------------
        # Load animation frames.
        #
        # Temporarily change CHARACTER_SIZE only while loading
        # these level frames.
        #
        # The original CHARACTER_SIZE is restored immediately
        # afterwards, so the home page remains unchanged.
        # --------------------------------------------------------

        old_size = self.CHARACTER_SIZE

        try:

            self.CHARACTER_SIZE = self.LEVEL_CHARACTER_SIZE

            frames = self.get_character_frames(
                image_path,
                self.FRONT_ROW,
                self.ANIMATION_FRAME_COUNT
            )

        finally:

            self.CHARACTER_SIZE = old_size

        if not frames:
            return

        # --------------------------------------------------------
        # Keep references alive.
        # --------------------------------------------------------

        animation_key = (
            f"LEVEL_CHARACTER_{selected_name}"
        )

        self.character_animation_frames[
            animation_key
        ] = frames

        # --------------------------------------------------------
        # Start animation.
        # --------------------------------------------------------

        self.animate_level_character(
            animation_key,
            image_label,
            frames
        )

    # ============================================================

    def animate_level_character(
        self,
        character_name,
        image_label,
        frames,
        frame_index=0
    ):
        """
        Animation player for characters shown on level screens.

        This is separate from the existing home-page animation.
        """

        if not frames:
            return

        try:

            image_label.configure(
                image=frames[frame_index]
            )

            self.character_animation_frames[
                character_name
            ] = frames

            next_frame = (
                frame_index + 1
            ) % len(frames)

            self.animation_jobs[
                character_name
            ] = self.root.after(
                self.LEVEL_CHARACTER_DELAY,
                lambda: self.animate_level_character(
                    character_name,
                    image_label,
                    frames,
                    next_frame
                )
            )

        except tk.TclError:

            return

    # ============================================================
    # HOME SCREEN
    # ============================================================

    def setup_home_screen(self):

        self.clear_screen()

        self.game = None
        self.active_mission_id = None

        self.selected_character = None
        self.selected_character_name = None

        # ========================================================
        # HEADER
        # ========================================================

        header = tk.Frame(
            self.root,
            bg=self.BG
        )

        header.pack(
            fill="x",
            pady=(25, 0)
        )

        self.make_label(
            header,
            "⚡ AI QUEST ⚡",
            34,
            True,
            self.CYAN
        ).pack()

        self.make_label(
            header,
            "THE INTELLIGENT DETECTIVE",
            15,
            True,
            self.TEXT
        ).pack(
            pady=(3, 0)
        )

        self.make_label(
            header,
            "AI-POWERED DIGITAL THREAT INVESTIGATION",
            9,
            False,
            self.MUTED
        ).pack(
            pady=(5, 0)
        )

        # ========================================================
        # MAIN PANEL
        # ========================================================

        panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=850,
            height=560
        )

        panel.pack(
            pady=18
        )

        panel.pack_propagate(False)

        self.make_label(
            panel,
            "CHOOSE YOUR DETECTIVE",
            21,
            True,
            self.GOLD
        ).pack(
            pady=(18, 3)
        )

        self.make_label(
            panel,
            "Select your character before beginning the investigation.",
            10,
            False,
            self.MUTED
        ).pack()

        # ========================================================
        # CHARACTER SELECTION AREA
        # ========================================================

        characters_frame = tk.Frame(
            panel,
            bg=self.PANEL
        )

        characters_frame.pack(
            pady=8
        )

        # ========================================================
        # FLINN CARD
        # ========================================================

        flinn_frame = tk.Frame(
            characters_frame,
            bg=self.PANEL_LIGHT,
            width=340,
            height=275,
            cursor="hand2"
        )

        flinn_frame.pack(
            side="left",
            padx=18
        )

        flinn_frame.pack_propagate(False)

        self.make_label(
            flinn_frame,
            "FLINN",
            18,
            True,
            self.CYAN
        ).pack(
            pady=(10, 2)
        )

        flinn_image_path = os.path.join(
            os.path.dirname(__file__),
            "characters",
            "boy.png"
        )

        flinn_photo = self.load_character_preview(
            flinn_image_path
        )

        if flinn_photo:

            self.character_preview_images[
                "FLINN"
            ] = flinn_photo

            flinn_image_label = tk.Label(
                flinn_frame,
                image=flinn_photo,
                bg=self.PANEL_LIGHT,
                cursor="hand2"
            )

            flinn_image_label.pack(
                pady=(0, 2)
            )

            flinn_image_label.bind(
                "<Button-1>",
                lambda event:
                self.select_character("FLINN")
            )

            # ----------------------------------------------------
            # Load animation frames.
            # ----------------------------------------------------

            flinn_frames = self.get_character_frames(
                flinn_image_path,
                self.FRONT_ROW,
                self.ANIMATION_FRAME_COUNT
            )

            if flinn_frames:

                self.character_animation_frames[
                    "FLINN"
                ] = flinn_frames

                self.animate_character(
                    "FLINN",
                    flinn_image_label,
                    flinn_frames
                )

        # --------------------------------------------------------
        # Make the WHOLE FLINN card clickable.
        # --------------------------------------------------------

        flinn_frame.bind(
            "<Button-1>",
            lambda event:
            self.select_character("FLINN")
        )

        self.character_buttons[
            "FLINN"
        ] = flinn_frame

        # ========================================================
        # PIXIE CARD
        # ========================================================

        pixie_frame = tk.Frame(
            characters_frame,
            bg=self.PANEL_LIGHT,
            width=340,
            height=275,
            cursor="hand2"
        )

        pixie_frame.pack(
            side="left",
            padx=18
        )

        pixie_frame.pack_propagate(False)

        self.make_label(
            pixie_frame,
            "PIXIE",
            18,
            True,
            self.PURPLE
        ).pack(
            pady=(10, 2)
        )

        pixie_image_path = os.path.join(
            os.path.dirname(__file__),
            "characters",
            "girl.png"
        )

        pixie_photo = self.load_character_preview(
            pixie_image_path
        )

        if pixie_photo:

            self.character_preview_images[
                "PIXIE"
            ] = pixie_photo

            pixie_image_label = tk.Label(
                pixie_frame,
                image=pixie_photo,
                bg=self.PANEL_LIGHT,
                cursor="hand2"
            )

            pixie_image_label.pack(
                pady=(0, 2)
            )

            pixie_image_label.bind(
                "<Button-1>",
                lambda event:
                self.select_character("PIXIE")
            )

            # ----------------------------------------------------
            # Load animation frames.
            # ----------------------------------------------------

            pixie_frames = self.get_character_frames(
                pixie_image_path,
                self.FRONT_ROW,
                self.ANIMATION_FRAME_COUNT
            )

            if pixie_frames:

                self.character_animation_frames[
                    "PIXIE"
                ] = pixie_frames

                self.animate_character(
                    "PIXIE",
                    pixie_image_label,
                    pixie_frames
                )

        # --------------------------------------------------------
        # Make the WHOLE PIXIE card clickable.
        # --------------------------------------------------------

        pixie_frame.bind(
            "<Button-1>",
            lambda event:
            self.select_character("PIXIE")
        )

        self.character_buttons[
            "PIXIE"
        ] = pixie_frame

        # ========================================================
        # SELECTED CHARACTER MESSAGE
        # ========================================================

        self.character_status = self.make_label(
            panel,
            "SELECT A CHARACTER",
            11,
            True,
            self.MUTED
        )

        self.character_status.pack(
            pady=(4, 3)
        )

        # ========================================================
        # NAME
        # ========================================================

        self.make_label(
            panel,
            "ENTER YOUR DETECTIVE NAME",
            11,
            True,
            self.CYAN
        ).pack(
            pady=(2, 4)
        )

        self.name_entry = tk.Entry(
            panel,
            font=("Segoe UI", 13),
            width=28,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            insertbackground=self.CYAN,
            relief="flat",
            justify="center"
        )

        self.name_entry.pack(
            ipady=7
        )

        # ========================================================
        # START BUTTON
        # ========================================================

        self.start_button = self.make_button(
            panel,
            "🚀 START INVESTIGATION",
            self.start_game,
            27,
            self.CYAN,
            self.BG,
            height=2
        )

        self.start_button.pack(
            pady=8
        )

    # ============================================================
    # CHARACTER SELECTION
    # ============================================================

    def select_character(self, character_name):

        self.selected_character = character_name
        self.selected_character_name = character_name

        # --------------------------------------------------------
        # Reset both card borders.
        # --------------------------------------------------------

        for name, frame in self.character_buttons.items():

            frame.configure(
                highlightthickness=0
            )

        # --------------------------------------------------------
        # Highlight selected character.
        # --------------------------------------------------------

        selected_frame = self.character_buttons.get(
            character_name
        )

        if selected_frame:

            selected_frame.configure(
                highlightthickness=3,
                highlightbackground=(
                    self.CYAN
                    if character_name == "FLINN"
                    else self.PURPLE
                ),
                highlightcolor=(
                    self.CYAN
                    if character_name == "FLINN"
                    else self.PURPLE
                )
            )

        # --------------------------------------------------------
        # Status text.
        # --------------------------------------------------------

        if character_name == "FLINN":

            self.character_status.config(
                text="✓ SELECTED DETECTIVE  •  FLINN",
                fg=self.CYAN
            )

        else:

            self.character_status.config(
                text="✓ SELECTED DETECTIVE  •  PIXIE",
                fg=self.PURPLE
            )

    # ============================================================
    # START GAME
    # ============================================================

    def start_game(self):

        name = self.name_entry.get().strip()

        # --------------------------------------------------------
        # Character required.
        # --------------------------------------------------------

        if not self.selected_character:

            messagebox.showwarning(
                "Character Required",
                "Please select FLINN or PIXIE before starting."
            )

            return

        # --------------------------------------------------------
        # Name required.
        # --------------------------------------------------------

        if not name:

            messagebox.showwarning(
                "Name Required",
                "Please enter your detective name."
            )

            return

        # --------------------------------------------------------
        # Create game.
        # --------------------------------------------------------

        self.game = GameEngine(name)

        # Store selected character.
        self.game.selected_character = (
            self.selected_character
        )

        self.show_dashboard()

    # ============================================================
    # DASHBOARD + LEVEL PANEL
    # ============================================================

    def show_dashboard(self):

        if not self.game:
            return

        if not self.game.has_more_missions():

            self.show_final_screen()
            return

        self.clear_screen()

        stats = self.game.get_player_stats()
        current_mission = self.game.get_current_mission()

        self.active_mission_id = current_mission["id"]

        total_levels = self.game.get_total_missions()
        current_level = current_mission["id"]

        # ========================================================
        # HEADER
        # ========================================================

        self.make_label(
            self.root,
            "🕵️ AI QUEST",
            30,
            True,
            self.CYAN
        ).pack(
            pady=(25, 2)
        )

        self.make_label(
            self.root,
            "DETECTIVE DASHBOARD",
            14,
            True,
            self.MUTED
        ).pack()

        # ========================================================
        # LEVEL PANEL
        # ========================================================

        level_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=950,
            height=150
        )

        level_panel.pack(
            pady=15
        )

        level_panel.pack_propagate(False)

        self.make_label(
            level_panel,
            "🎮 LEVEL PROGRESS",
            14,
            True,
            self.GOLD
        ).pack(
            pady=(12, 8)
        )

        levels_frame = tk.Frame(
            level_panel,
            bg=self.PANEL
        )

        levels_frame.pack()

        # --------------------------------------------------------
        # Create game-style level buttons
        # --------------------------------------------------------

        for level in range(1, total_levels + 1):

            if level < current_level:

                # Completed level
                text = f"✓\n{level}"
                bg = self.GREEN
                fg = self.BG

            elif level == current_level:

                # Current level
                text = f"★\n{level}"
                bg = self.CYAN
                fg = self.BG

            else:

                # Locked level
                text = f"🔒\n{level}"
                bg = self.PANEL_LIGHT
                fg = self.MUTED

            level_button = tk.Label(
                levels_frame,
                text=text,
                font=("Segoe UI", 10, "bold"),
                width=5,
                height=2,
                bg=bg,
                fg=fg,
                relief="flat"
            )

            level_button.pack(
                side="left",
                padx=3
            )

        # ========================================================
        # LEVEL TEXT
        # ========================================================

        self.make_label(
            level_panel,
            f"LEVEL {current_level} OF {total_levels}",
            10,
            True,
            self.CYAN
        ).pack(
            pady=(5, 0)
        )

        # ========================================================
        # DETECTIVE INFORMATION
        # ========================================================

        info_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=950,
            height=95
        )

        info_panel.pack(
            pady=8
        )

        info_panel.pack_propagate(False)

        self.make_label(
            info_panel,
            f"DETECTIVE  •  {stats['name']}",
            13,
            True,
            self.TEXT
        ).pack(
            pady=(13, 5)
        )

        stats_text = (
            f"SCORE  {stats['score']}     •     "
            f"ACCURACY  {stats['accuracy']:.1f}%     •     "
            f"MISSIONS  "
            f"{stats['missions_completed']}/{total_levels}"
        )

        self.make_label(
            info_panel,
            stats_text,
            11,
            False,
            self.CYAN
        ).pack()

        # ========================================================
        # CHARACTER
        # ========================================================

        selected_name = getattr(
            self.game,
            "selected_character",
            self.selected_character
        )

        character_color = (
            self.PURPLE
            if selected_name == "PIXIE"
            else self.CYAN
        )

        self.make_label(
            self.root,
            f"DETECTIVE CHARACTER  •  {selected_name}",
            10,
            True,
            character_color
        ).pack(
            pady=4
        )

        # ========================================================
        # CURRENT LEVEL PANEL
        # ========================================================

        mission_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=950,
            height=260
        )

        mission_panel.pack(
            pady=8
        )

        mission_panel.pack_propagate(False)
        

        self.make_label(
            mission_panel,
            f"LEVEL {current_level}",
            15,
            True,
            self.GOLD
        ).pack(
            pady=(20, 3)
        )

        self.make_label(
            mission_panel,
            current_mission["title"],
            24,
            True,
            self.TEXT
        ).pack(
            pady=5
        )

        self.make_label(
            mission_panel,
            f"DIFFICULTY  •  "
            f"{current_mission['difficulty']}",
            11,
            True,
            self.PURPLE
        ).pack(
            pady=4
        )

        self.make_label(
            mission_panel,
            f"🏆 REWARD  •  "
            f"{current_mission['points']} POINTS",
            11,
            False,
            self.MUTED
        ).pack(
            pady=4
        )

        self.make_button(
            mission_panel,
            "🔎  INVESTIGATE EVIDENCE",
            self.start_mission,
            32,
            self.CYAN,
            self.BG
        ).pack(
            pady=14
        )

      

        # ========================================================
        # LEVEL CHARACTER
        # ========================================================

        self.show_level_character(
            self.get_level_dialogue(current_level)
        )

    # ============================================================
    # START MISSION
    # ============================================================

    def start_mission(self):

        if not self.game:
            return

        if not self.game.has_more_missions():

            self.show_final_screen()
            return

        mission = self.game.get_current_mission()

        self.active_mission_id = mission["id"]

        self.clear_screen()

        # ========================================================
        # HEADER
        # ========================================================

        self.make_label(
            self.root,
            f"MISSION {mission['id']}",
            15,
            True,
            self.GOLD
        ).pack(
            pady=(25, 5)
        )

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
        ).pack(
            pady=5
        )

        # ========================================================
        # EVIDENCE PANEL
        # ========================================================

        evidence_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=850,
            height=280
        )

        evidence_panel.pack(
            pady=20
        )

        evidence_panel.pack_propagate(False)

        self.make_label(
            evidence_panel,
            "📁 DIGITAL EVIDENCE",
            14,
            True,
            self.GOLD
        ).pack(
            pady=(18, 8)
        )

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

        evidence_box.config(
            state="disabled"
        )

        evidence_box.pack()

        self.make_label(
            self.root,
            "Analyze the evidence before making your final decision.",
            11,
            False,
            self.MUTED
        ).pack(
            pady=5
        )

        self.make_button(
            self.root,
            "🧠  ANALYZE WITH AI",
            lambda: self.analyze_evidence(
                mission["evidence"],
                mission["id"]
            ),
            28,
            self.PURPLE,
            self.WHITE
        ).pack(
            pady=15
        )

        # ========================================================
        # LEVEL CHARACTER
        # ========================================================

        self.show_level_character(
            self.get_level_dialogue(mission["id"])
        )

    # ============================================================
    # AI ANALYSIS
    # ============================================================

    def analyze_evidence(
        self,
        evidence,
        mission_id
    ):

        if not self.game:
            return

        current_mission = (
            self.game.get_current_mission()
        )

        if mission_id != current_mission["id"]:
            return

        result = self.model_comparison.final_decision(
            evidence
        )

        final_prediction = result["final_decision"]

        models = result["models"]

        self.clear_screen()

        # ========================================================
        # HEADER
        # ========================================================

        self.make_label(
            self.root,
            "🧠 AI ANALYSIS",
            28,
            True,
            self.CYAN
        ).pack(
            pady=(25, 3)
        )

        self.make_label(
            self.root,
            "THREAT DETECTION • MODEL COMPARISON",
            11,
            True,
            self.MUTED
        ).pack()

        # ========================================================
        # MODELS PANEL
        # ========================================================

        models_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=850,
            height=280
        )

        models_panel.pack(
            pady=25
        )

        models_panel.pack_propagate(False)

        self.make_label(
            models_panel,
            "AI MODEL RESULTS",
            15,
            True,
            self.GOLD
        ).pack(
            pady=(18, 10)
        )

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

            row.pack(
                pady=4
            )

            self.make_label(
                row,
                f"{icon} {model_name}",
                12,
                True,
                self.TEXT
            ).pack(
                side="left",
                padx=10
            )

            self.make_label(
                row,
                prediction,
                12,
                True,
                color
            ).pack(
                side="left",
                padx=10
            )

            self.make_label(
                row,
                f"{confidence:.1f}% confidence",
                11,
                False,
                self.MUTED
            ).pack(
                side="left",
                padx=10
            )

        # ========================================================
        # CONSENSUS
        # ========================================================

        dangerous_votes = result["dangerous_votes"]

        self.make_label(
            self.root,
            f"AI CONSENSUS  •  "
            f"{dangerous_votes}/3 MODELS DETECTED DANGER",
            14,
            True,
            self.GOLD
        ).pack(
            pady=5
        )

        decision_color = (
            self.RED
            if final_prediction == "dangerous"
            else self.GREEN
        )

        self.make_label(
            self.root,
            f"FINAL AI DECISION  •  "
            f"{final_prediction.upper()}",
            21,
            True,
            decision_color
        ).pack(
            pady=8
        )

        self.make_label(
            self.root,
            "MAKE YOUR FINAL DETECTIVE DECISION",
            12,
            True,
            self.TEXT
        ).pack(
            pady=(8, 5)
        )

        # ========================================================
        # DECISION BUTTONS
        # ========================================================

        buttons = tk.Frame(
            self.root,
            bg=self.BG
        )

        buttons.pack(
            pady=10
        )

        dangerous_button = self.make_button(
            buttons,
            "🚨  DANGEROUS",
            lambda: self.submit_decision(
                "dangerous",
                final_prediction,
                result,
                mission_id
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
                result,
                mission_id
            ),
            20,
            self.GREEN,
            self.BG
        )

        safe_button.pack(
            side="left",
            padx=15
        )

        # ========================================================
        # LEVEL CHARACTER
        # ========================================================

        self.show_level_character(
            self.get_level_dialogue(mission_id)
        )

   
      # ============================================================
    # SUBMIT DECISION
    # ============================================================

    def submit_decision(
        self,
        answer,
        prediction,
        ai_result,
        mission_id
    ):

        if not self.game:
            return

        # --------------------------------------------------------
        # Make sure this is still the mission being answered.
        # --------------------------------------------------------

        if not self.game.has_more_missions():
            self.show_final_screen()
            return

        current_mission = self.game.get_current_mission()

        if current_mission["id"] != mission_id:
            return

        # --------------------------------------------------------
        # Save the mission BEFORE GameEngine moves to next mission.
        # --------------------------------------------------------

        answered_mission = current_mission

        result = self.game.submit_answer(
            answer,
            prediction
        )

        # --------------------------------------------------------
        # Add AI information.
        # --------------------------------------------------------

        result["ai_prediction"] = prediction

        result["mission_id"] = answered_mission["id"]

        model_results = ai_result["models"]

        result["naive_bayes_probability"] = (
            model_results["Naive Bayes"]["dangerous_probability"]
        )

        result["logistic_regression_probability"] = (
            model_results["Logistic Regression"]["dangerous_probability"]
        )

        result["random_forest_probability"] = (
            model_results["Random Forest"]["dangerous_probability"]
        )

        result["dangerous_votes"] = (
            ai_result["dangerous_votes"]
        )

        # --------------------------------------------------------
        # SAVE RESULT
        # --------------------------------------------------------

        self.data_manager.save_result(
            self.game.player.name,
            result
        )

        # --------------------------------------------------------
        # CLEAR CURRENT SCREEN
        # --------------------------------------------------------

        self.clear_screen()

        # ========================================================
        # RESULT STATUS
        # ========================================================

        if result["correct"]:

            result_color = self.GREEN
            result_icon = "✓"
            result_title = "MISSION SUCCESS"

            result_message = (
                "Excellent detective work!"
            )

        else:

            result_color = self.RED
            result_icon = "✕"
            result_title = "MISSION FAILED"

            result_message = (
                "The evidence led to the wrong conclusion."
            )

        # ========================================================
        # RESULT HEADER
        # ========================================================

        self.make_label(
            self.root,
            result_icon,
            45,
            True,
            result_color
        ).pack(
            pady=(45, 5)
        )

        self.make_label(
            self.root,
            result_title,
            28,
            True,
            result_color
        ).pack(
            pady=5
        )

        self.make_label(
            self.root,
            result_message,
            12,
            False,
            self.MUTED
        ).pack(
            pady=3
        )

        # ========================================================
        # RESULT PANEL
        # ========================================================

        result_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=700,
            height=350
        )

        result_panel.pack(
            pady=25
        )

        result_panel.pack_propagate(False)

        # --------------------------------------------------------
        # Player decision
        # --------------------------------------------------------

        self.make_label(
            result_panel,
            "YOUR DECISION",
            11,
            True,
            self.MUTED
        ).pack(
            pady=(25, 3)
        )

        self.make_label(
            result_panel,
            answer.upper(),
            20,
            True,
            self.CYAN
        ).pack(
            pady=2
        )

        # --------------------------------------------------------
        # Correct answer
        # --------------------------------------------------------

        self.make_label(
            result_panel,
            "CORRECT CLASSIFICATION",
            11,
            True,
            self.MUTED
        ).pack(
            pady=(12, 3)
        )

        correct_answer = answered_mission["answer"].upper()

        correct_color = (
            self.GREEN
            if result["correct"]
            else self.RED
        )

        self.make_label(
            result_panel,
            correct_answer,
            18,
            True,
            correct_color
        ).pack(
            pady=2
        )

        # --------------------------------------------------------
        # AI consensus
        # --------------------------------------------------------

        self.make_label(
            result_panel,
            (
                f"AI CONSENSUS  •  "
                f"{ai_result['dangerous_votes']}/3 "
                f"MODELS DETECTED DANGER"
            ),
            11,
            True,
            self.GOLD
        ).pack(
            pady=(15, 3)
        )

        # --------------------------------------------------------
        # AI prediction
        # --------------------------------------------------------

        ai_color = (
            self.RED
            if prediction == "dangerous"
            else self.GREEN
        )

        self.make_label(
            result_panel,
            f"AI DECISION  •  {prediction.upper()}",
            12,
            True,
            ai_color
        ).pack(
            pady=3
        )

        # --------------------------------------------------------
        # Points + score
        # --------------------------------------------------------

        score_frame = tk.Frame(
            result_panel,
            bg=self.PANEL
        )

        score_frame.pack(
            pady=(15, 5)
        )

        self.make_label(
            score_frame,
            f"+{result['points']} POINTS",
            12,
            True,
            self.GREEN
        ).pack(
            side="left",
            padx=25
        )

        self.make_label(
            score_frame,
            f"TOTAL SCORE  •  {result['score']}",
            12,
            True,
            self.GOLD
        ).pack(
            side="left",
            padx=25
        )

        # ========================================================
        # NEXT MISSION BUTTON
        # ========================================================

        if self.game.has_more_missions():

            self.make_button(
                self.root,
                "➡  NEXT MISSION",
                self.show_dashboard,
                30,
                self.CYAN,
                self.BG,
                height=2
            ).pack(
                pady=10
            )

        else:

            self.make_button(
                self.root,
                "🏆  VIEW FINAL RESULTS",
                self.show_final_screen,
                30,
                self.GOLD,
                self.BG,
                height=2
            ).pack(
                pady=10
            )

        # ========================================================
        # CHARACTER
        # ========================================================

        if self.game.has_more_missions():

            next_mission = self.game.get_current_mission()

            self.show_level_character(
                self.get_level_dialogue(
                    next_mission["id"]
                )
            )
       # ============================================================
    # FINAL SCREEN
    # ============================================================

    def animate_final_running_character(
        self,
        character_name,
        image_label,
        frames,
        frame_index=0
    ):

        if not frames:
            return

        try:

            image_label.configure(
                image=frames[frame_index]
            )

            self.character_animation_frames[
                character_name
            ] = frames

            next_frame = (
                frame_index + 1
            ) % len(frames)

            self.animation_jobs[
                character_name
            ] = self.root.after(
                self.FINAL_CHARACTER_DELAY,
                lambda: self.animate_final_running_character(
                    character_name,
                    image_label,
                    frames,
                    next_frame
                )
            )

        except tk.TclError:

            return

    # ============================================================
    # FINAL SCREEN RUNNING CHARACTER
    # ============================================================

    def show_final_running_character(self):

        selected_name = getattr(
            self.game,
            "selected_character",
            self.selected_character
        )

        if not selected_name:
            return

        if selected_name == "PIXIE":
            image_filename = "girl.png"
        else:
            image_filename = "boy.png"

        image_path = os.path.join(
            os.path.dirname(__file__),
            "characters",
            image_filename
        )

        if not os.path.exists(image_path):
            return

        character_container = tk.Frame(
            self.root,
            bg=self.BG,
            padx=0,
            pady=0
        )

        character_container.place(
            relx=0.97,
            rely=0.98,
            anchor="se",
            x=0,
            y=0
        )

        image_label = tk.Label(
            character_container,
            bg=self.BG,
            padx=0,
            pady=0,
            borderwidth=0,
            highlightthickness=0
        )

        image_label.pack(
            padx=0,
            pady=0
        )

        # Running animation row
        RUNNING_ROW = 1

        old_size = self.CHARACTER_SIZE

        try:

            self.CHARACTER_SIZE = 250

            frames = self.get_character_frames(
                image_path,
                RUNNING_ROW,
                self.ANIMATION_FRAME_COUNT
            )

        finally:

            self.CHARACTER_SIZE = old_size

        if not frames:
            return

        animation_key = (
            f"FINAL_RUNNING_{selected_name}"
        )

        self.character_animation_frames[
            animation_key
        ] = frames

        self.animate_final_running_character(
            animation_key,
            image_label,
            frames
        )

    # ============================================================
    # ACTUAL FINAL SCREEN
    # ============================================================

    def show_final_screen(self):

        if not self.game:
            return

        self.clear_screen()

        stats = self.game.get_player_stats()

        # ========================================================
        # HEADER
        # ========================================================

        self.make_label(
            self.root,
            "🎉",
            42,
            True,
            self.GOLD
        ).pack(
            pady=(35, 0)
        )

        self.make_label(
            self.root,
            "INVESTIGATION COMPLETE",
            30,
            True,
            self.CYAN
        ).pack(
            pady=5
        )

        self.make_label(
            self.root,
            "ALL DIGITAL CASES HAVE BEEN SOLVED",
            11,
            True,
            self.MUTED
        ).pack()

        # ========================================================
        # RESULTS PANEL
        # ========================================================

        panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            width=720,
            height=350
        )

        panel.pack(
            pady=30
        )

        panel.pack_propagate(False)

        self.make_label(
            panel,
            f"CONGRATULATIONS, DETECTIVE "
            f"{stats['name'].upper()}!",
            17,
            True,
            self.TEXT
        ).pack(
            pady=(30, 15)
        )

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

        self.make_label(
            panel,
            f"ACCURACY  •  "
            f"{stats['accuracy']:.1f}%",
            15,
            True,
            self.CYAN
        ).pack(
            pady=5
        )

        self.make_label(
            panel,
            f"MISSIONS COMPLETED  •  "
            f"{stats['missions_completed']}/{self.game.get_total_missions()}",
            12,
            False,
            self.TEXT
        ).pack(
            pady=5
        )

        self.make_label(
            panel,
            f"CORRECT DECISIONS  •  "
            f"{stats['correct_answers']}/{stats['attempts']}",
            12,
            False,
            self.GREEN
        ).pack(
            pady=5
        )

        self.make_label(
            panel,
            "You successfully completed the AI Quest investigation.",
            10,
            False,
            self.MUTED
        ).pack(
            pady=12
        )

        self.make_button(
            panel,
            "🔄  NEW INVESTIGATION",
            self.setup_home_screen,
            28,
            self.CYAN,
            self.BG
        ).pack(
            pady=15
        )

        # ========================================================
        # RUNNING CHARACTER
        # ========================================================

        self.show_final_running_character()


# =================================================================
# MAIN
# =================================================================

def main():

    root = tk.Tk()

    app = AIQuest(root)

    root.mainloop()


if __name__ == "__main__":
    main()