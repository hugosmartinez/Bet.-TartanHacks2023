
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hugom\build\assets\frame4")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("390x790")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 790,
    width = 390,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        34.0,
        113.0,
        144.0,
        223.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        34.0,
        241.0,
        190.0,
        279.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        319.0,
        40.0,
        357.0,
        78.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        34.0,
        321.0,
        356.0,
        407.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        34.0,
        417.0,
        190.0,
        503.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        200.0,
        417.0,
        356.0,
        503.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        34.0,
        609.0,
        190.0,
        695.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        200.0,
        609.0,
        356.0,
        695.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        34.0,
        513.0,
        190.0,
        599.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        200.0,
        513.0,
        356.0,
        599.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        200.0,
        241.0,
        356.0,
        279.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        168.0,
        161.0,
        anchor="nw",
        text="Net Earning",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        221.0,
        210.0,
        anchor="nw",
        text="Accuracy",
        fill="#000000",
        font=("Inter", 8 * -1)
    )

    canvas.create_text(
        312.0,
        210.0,
        anchor="nw",
        text="Wins-loses",
        fill="#000000",
        font=("Inter", 8 * -1)
    )

    canvas.create_text(
        266.0,
        161.0,
        anchor="nw",
        text="Friends",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        168.0,
        125.0,
        anchor="nw",
        text="250",
        fill="#000000",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        34.0,
        41.0,
        anchor="nw",
        text="username",
        fill="#000000",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        221.0,
        186.0,
        anchor="nw",
        text="90%",
        fill="#000000",
        font=("Inter", 20 * -1)
    )

    canvas.create_text(
        312.0,
        186.0,
        anchor="nw",
        text="14-9",
        fill="#000000",
        font=("Inter", 20 * -1)
    )

    canvas.create_text(
        259.0,
        125.0,
        anchor="nw",
        text="450",
        fill="#000000",
        font=("Inter", 30 * -1)
    )

    canvas.create_rectangle(
        168.0,
        253.0,
        183.0,
        268.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        0.0,
        711.0,
        390.0,
        798.0,
        fill="#B6B6B6",
        outline="")

    canvas.create_text(
        28.0,
        745.0,
        anchor="nw",
        text="Home",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        80.0,
        745.0,
        anchor="nw",
        text="Current Bets",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        319.0,
        745.0,
        anchor="nw",
        text="Profile",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        182.0,
        745.0,
        anchor="nw",
        text="Post",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        227.0,
        745.0,
        anchor="nw",
        text="Leaderboard",
        fill="#000000",
        font=("Inter", 12 * -1)
    )
window.resizable(False, False)
window.mainloop()
