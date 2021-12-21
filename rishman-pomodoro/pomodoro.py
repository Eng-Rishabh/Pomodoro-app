from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

"""units are in munutes"""
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
NO_OF_SLOT = 4

"""unit is in second"""
WINDOW_SHOWING_TIME = 30

UNIT_CONVERTER = 1000
# ---------------------------- TIMER RESET ------------------------------- #

id_for_cancellation = None
work_min = WORK_MIN * 60
short_break_min = SHORT_BREAK_MIN * 60
long_break = LONG_BREAK_MIN * 60
count = 0


def reset_the_timer():
    global count
    count = (work_min + short_break_min) * NO_OF_SLOT + long_break
    h = int(count / 3600)
    m = int((count % 3600) / 60)
    s = int(((count % 60) % 60))
    canvas1.itemconfig(text_timer, text=f"{h:02}:{m:02}:{s:02}")
    window.attributes("-topmost", 0)
# ---------------------------- TIMER MECHANISM ------------------------------- #


labels = []
i = 0
controller = NO_OF_SLOT * 2 - 1


def start_the_timer():
    global count
    global i
    global controller
    if count != 0:
        count = 0
        window.after_cancel(id_for_cancellation)
        i = 0
        for k in range(0, len(labels)):
            labels[k].config(text="✔", fg=YELLOW)
        controller = NO_OF_SLOT * 2 - 1
        window.attributes("-topmost", 0)
    if controller == 0 and i < len(labels):
        count_down(long_break)
        upper_label.config(text="L-Break", fg=RED)
        labels[i].config(fg=GREEN)
        i += 1
    elif controller % 2 != 0:
        count_down(work_min)
        upper_label.config(text=" Work ", fg=GREEN)
        if i > 0:
            labels[i-1].config(text="✔✔")
    elif controller % 2 == 0 and i < len(labels):
        count_down(short_break_min)
        upper_label.config(text="Break", fg=PINK)
        labels[i].config(fg=GREEN)
        i += 1


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(given_count):
    global controller
    global id_for_cancellation
    global count
    global i
    count = given_count
    h = int(count / 3600)
    m = int((count % 3600) / 60)
    s = int(((count % 60) % 60))
    canvas1.itemconfig(text_timer, text=f"{h:02}:{m:02}:{s:02}")
    if count < WINDOW_SHOWING_TIME:
        window.attributes('-topmost', 1)
    if count == 0:
        window.attributes("-topmost", 0)
    if count > 0:
        id_for_cancellation = window.after(UNIT_CONVERTER, count_down, count - 1)
    else:
        if controller > 0:
            controller -= 1
            start_the_timer()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Rishman Pomodoro")
window.geometry("500x600")
window.resizable(0, 0)
window.config(padx=100, pady=50, bg=YELLOW)

# bg = PhotoImage(file="tomato.png")
# background_label = Label(window, image=bg)
# background_label.place(x=0, y=0)
upper_label = Label(text="Timer", font=(FONT_NAME, 55), fg=GREEN, bg=YELLOW)
upper_label.grid(column=1, row=0)

"""canvas allows us to do the things on top of each other"""
canvas1 = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas1.create_image(100, 112, image=tomato_img)
text_timer = canvas1.create_text(100, 130, text="00:00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas1.grid(column=1, row=2)
# canvas1.pack()


button_left = Button(text="Start", command=start_the_timer, bg=YELLOW, highlightthickness=0)
# button_left.pack(side="left")
button_left.grid(column=0, row=3)

button_right = Button(text="Reset", command=reset_the_timer, bg=YELLOW, highlightthickness=0)
# button_right.pack(side="right")
button_right.grid(column=2, row=3)


for j in range(0, NO_OF_SLOT):
    check_label = Label(text="✔", font=(FONT_NAME, 35, "bold"), fg=YELLOW, bg=YELLOW)
    check_label.grid(column=1, row=4 + j)
    labels.append(check_label)
window.mainloop()
