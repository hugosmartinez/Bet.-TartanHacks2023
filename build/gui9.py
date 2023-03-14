
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hugom\build\assets\frame9")


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
        207.0,
        715.0,
        378.0,
        747.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        14.0,
        27.0,
        anchor="nw",
        text="x",
        fill="#000000",
        font=("Inter", 36 * -1)
    )

    canvas.create_text(
        230.0,
        722.0,
        anchor="nw",
        text="Post",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_rectangle(
        14.0,
        715.0,
        185.0,
        747.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        37.0,
        722.0,
        anchor="nw",
        text="Save",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_rectangle(
        12.0,
        98.0,
        378.0,
        689.0,
        fill="#D9D9D9",
        outline="")
window.resizable(False, False)
window.mainloop()
