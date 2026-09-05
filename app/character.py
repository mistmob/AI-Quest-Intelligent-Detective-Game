import tkinter as tk
from PIL import Image, ImageTk
import os


class DetectiveCharacter:

    # ============================================================
    # LPC SPRITE SETTINGS
    # ============================================================

    FRAME_WIDTH = 64
    FRAME_HEIGHT = 64

    # Row 2 = FRONT-FACING
    FRONT_ROW = 2

    # Use ONE clean standing front-facing frame.
    # This prevents sideways/action poses.
    IDLE_FRAMES = [0,1,2,3]

    # Make pixel character larger on screen
    SCALE = 3

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        canvas,
        sprite_path,
        x,
        y,
        name="FLINN"
    ):

        self.canvas = canvas
        self.x = x
        self.y = y
        self.name = name

        self.frame_index = 0
        self.animation_running = True

        self.dialogue_after_id = None

        # --------------------------------------------------------
        # Load sprite sheet
        # --------------------------------------------------------

        self.sprite_path = os.path.abspath(sprite_path)

        if not os.path.exists(self.sprite_path):
            raise FileNotFoundError(
                f"Character sprite not found:\n{self.sprite_path}"
            )

        self.sprite_sheet = Image.open(
            self.sprite_path
        ).convert("RGBA")

        # --------------------------------------------------------
        # Create character image
        # --------------------------------------------------------

        self.photo = None

        self.image_id = self.canvas.create_image(
            self.x,
            self.y,
            anchor="center"
        )

        # Character name
        self.name_id = self.canvas.create_text(
            self.x,
            self.y + 125,
            text=self.name,
            fill="#00e5ff",
            font=("Segoe UI", 11, "bold")
        )

        self.update_sprite()

        self.animate()

    # ============================================================
    # GET SPRITE FRAME
    # ============================================================

    def get_frame(self):

        sprite_frame = self.IDLE_FRAMES[
            self.frame_index
        ]

        left = sprite_frame * self.FRAME_WIDTH
        top = self.FRONT_ROW * self.FRAME_HEIGHT

        right = left + self.FRAME_WIDTH
        bottom = top + self.FRAME_HEIGHT

        frame = self.sprite_sheet.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )

        # Scale pixel art without blur
        frame = frame.resize(
            (
                self.FRAME_WIDTH * self.SCALE,
                self.FRAME_HEIGHT * self.SCALE
            ),
            Image.Resampling.NEAREST
        )

        return frame

    # ============================================================
    # UPDATE SPRITE
    # ============================================================

    def update_sprite(self):

        frame = self.get_frame()

        self.photo = ImageTk.PhotoImage(frame)

        self.canvas.itemconfig(
            self.image_id,
            image=self.photo
        )

        self.canvas.coords(
            self.image_id,
            self.x,
            self.y
        )

        self.canvas.coords(
            self.name_id,
            self.x,
            self.y + 125
        )

    # ============================================================
    # ANIMATION
    # ============================================================

    def animate(self):

     if not self.animation_running:
        return

     self.update_sprite()

     self.canvas.after(
         180,
        self.animate
    )

    # ============================================================
    # MOVE
    # ============================================================

    def move(self, dx, dy):

        self.x += dx
        self.y += dy

        self.update_sprite()

        if hasattr(self, "dialogue_box"):
            self.update_dialogue_position()

    # ============================================================
    # SAY DIALOGUE
    # ============================================================

    def say(self, text):

        self.clear_dialogue()

        self.dialogue_box = self.canvas.create_rectangle(
            self.x - 180,
            self.y - 145,
            self.x + 180,
            self.y - 85,
            fill="#151c32",
            outline="#00e5ff",
            width=2
        )

        self.dialogue_text = self.canvas.create_text(
            self.x,
            self.y - 115,
            text=text,
            fill="#f5f7ff",
            font=("Segoe UI", 11, "bold"),
            width=330
        )

        self.dialogue_after_id = self.canvas.after(
            3500,
            self.clear_dialogue
        )

    # ============================================================
    # UPDATE DIALOGUE POSITION
    # ============================================================

    def update_dialogue_position(self):

        if not hasattr(self, "dialogue_box"):
            return

        self.canvas.coords(
            self.dialogue_box,
            self.x - 180,
            self.y - 145,
            self.x + 180,
            self.y - 85
        )

        self.canvas.coords(
            self.dialogue_text,
            self.x,
            self.y - 115
        )

    # ============================================================
    # CLEAR DIALOGUE
    # ============================================================

    def clear_dialogue(self):

        if self.dialogue_after_id:

            try:
                self.canvas.after_cancel(
                    self.dialogue_after_id
                )
            except:
                pass

            self.dialogue_after_id = None

        if hasattr(self, "dialogue_box"):

            self.canvas.delete(
                self.dialogue_box
            )

            self.canvas.delete(
                self.dialogue_text
            )

            del self.dialogue_box
            del self.dialogue_text

    # ============================================================
    # STOP ANIMATION
    # ============================================================

    def stop_animation(self):

        self.animation_running = False

    # ============================================================
    # START ANIMATION
    # ============================================================

    def start_animation(self):

        if not self.animation_running:

            self.animation_running = True
            self.animate()

    # ============================================================
    # DESTROY CHARACTER
    # ============================================================

    def destroy(self):

        self.animation_running = False

        self.canvas.delete(
            self.image_id
        )

        self.canvas.delete(
            self.name_id
        )

        self.clear_dialogue()