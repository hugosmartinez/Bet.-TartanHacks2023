
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hugom\build\assets\frame2")


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
    36.0,
    102.0,
    354.0,
    206.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    84.0,
    131.0,
    anchor="nw",
    text="2578 VS 390",
    fill="#000000",
    font=("Inter Regular", 36 * -1)
)

canvas.create_rectangle(
    0.0,
    221.0,
    390.0,
    721.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    45.0,
    264.0,
    anchor="nw",
    text="title",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

canvas.create_rectangle(
    36.0,
    660.0,
    354.0,
    698.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    45.0,
    389.0,
    anchor="nw",
    text="amount gain/lost",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

canvas.create_text(
    50.0,
    514.0,
    anchor="nw",
    text="account summary",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

canvas.create_rectangle(
    310.0,
    34.0,
    354.0,
    78.0,
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

canvas.create_rectangle(
    37.0,
    37.0,
    80.0,
    80.0,
    fill="#D9D9D9",
    outline="")
window.resizable(False, False)
window.mainloop()
