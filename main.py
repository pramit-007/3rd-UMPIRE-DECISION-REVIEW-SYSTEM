import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time

stream = cv2.VideoCapture("video2.mp4")
flag = True

# Function to handle playback
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    frame1 = int(stream.get(cv2.CAP_PROP_POS_FRAMES))  
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)  

    grabbed, frame = stream.read()
    if not grabbed:
        window.quit()  # Fixed exit method
    
    frame = imutils.resize(frame, width=SET_WIDTH,height=SET_HEIGHT)  # Removed unsupported height argument
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    if flag:
        canvas.create_text(134, 26, fill="white", font="Times 26 bold", text="Decision Pending")
    flag = not flag  

def out():
    thread = threading.Thread(target=pending, args=("out", SET_WIDTH, SET_HEIGHT))  # Fixed args
    thread.daemon = 1
    thread.start()
    print("Player is OUT")

def not_out():
    thread = threading.Thread(target=pending, args=("not_out", SET_WIDTH, SET_HEIGHT))  # Fixed args
    thread.daemon = 1
    thread.start()
    print("Player is NOT OUT")


def pending(decision, w, h):
    frame = cv2.cvtColor(cv2.imread("DECISION PENDING PS.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=w)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    time.sleep(1)

    frame = cv2.cvtColor(cv2.imread("AD PS DRS.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=w)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    time.sleep(1.5)

    decisionImg = "OUT DESIGN PS.png" if decision == "out" else "NOT OUT DESIGN PS.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)  
    frame = imutils.resize(frame, width=w)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

def out():
    thread = threading.Thread(target=pending, args=("out", SET_WIDTH, SET_HEIGHT))
    thread.daemon = 1
    thread.start()
    print("Player is OUT")

def not_out():
    thread = threading.Thread(target=pending, args=("not_out", SET_WIDTH, SET_HEIGHT))
    thread.daemon = 1
    thread.start()
    print("Player is NOT OUT")

SET_WIDTH = 650
SET_HEIGHT = 368

# Initialize Tkinter window
window = tkinter.Tk()
window.title("Archiver 3rd Umpire Decision Review Kit")

# Load and process image
cv_img = cv2.cvtColor(cv2.imread("FINAL DRS FRONT.png"), cv2.COLOR_BGR2RGB)

# Create canvas
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

# Buttons for control playback
btn = tkinter.Button(window, text="<< Previous (Fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (Slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Forward >> (Slow)", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Forward >> (Fast)", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give OUT", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give NOT OUT", width=50, command=not_out)
btn.pack()

# Run main loop
window.mainloop()
