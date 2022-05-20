import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo
import audioread
import os
import model
import soundfile as sf

window = tk.Tk()
window.title("Soundblend")
model = model.Model()

def vox():
    if model.y is not None:
        progresslabel.configure(text="loading...")
        progresslabel.configure(fg="black")
        model.osc_types = [osc1_option.get(), osc2_option.get(), osc3_option.get()]
        model.osc_levels = [osc1_level.get(), osc2_level.get(), osc3_level.get()]
        model.vox()
        progresslabel.configure(text="Soundblend complete.")
        progresslabel.configure(fg="green")
    else:
        showinfo("Soundblend incomplete.",  "Please upload a modulator file.")

def play():
    model.is_playing = not model.is_playing
    if model.is_playing and model.y is not None:
        play.configure(image = stop_tkimg)
        play.image = stop_tkimg
        model.play()
    elif model.y is None:
        showinfo("Soundblend incomplete.",  "Please upload a modulator file.")
    else:
        play.configure(image = play_tkimg)
        play.image = play_tkimg
        model.stop()

def updateFileLabel(filename):
    filename_trim = os.path.basename(filename)
    new_label = "Modulator file: " + filename_trim
    filelabel.configure(text = new_label)
    progresslabel.configure(text="Modulator file uploaded.\nPlay file or press soundblend button.")
    progresslabel.configure(fg="blue")

def download():
    if model.z is not None:
        filename = asksaveasfilename(defaultextension='wav')
        sf.write(filename, model.z, model.sr)
    else:
        showinfo("Soundblend incomplete.",  "Please soundblend a file.")

def uploadFile():
    invalid_file = True
    while invalid_file:
        try:
            filename = askopenfilename()
            if len(filename) == 0:
                showinfo("Exit",  "No file uploaded.")
                return
            model.loadFile(filename)
            updateFileLabel(filename)
            invalid_file = False
        except audioread.exceptions.NoBackendError:
            showinfo("Error",  "Invalid file type.")

download_img = Image.open("img/download.png")
download_img = download_img.resize((50,50))
download_tkimg = ImageTk.PhotoImage(download_img)

vox_img = Image.open("img/vox.png")
vox_img = vox_img.resize((75,75))
vox_tkimg = ImageTk.PhotoImage(vox_img)

play_img = Image.open("img/play.png")
play_img = play_img.resize((50,50))
play_tkimg = ImageTk.PhotoImage(play_img)

stop_img = Image.open("img/stop.png")
stop_img = stop_img.resize((50,50))
stop_tkimg = ImageTk.PhotoImage(stop_img)

osc1 = tk.Frame(master=window,highlightbackground="grey", highlightthickness=1)
osc2 = tk.Frame(master=window,highlightbackground="grey", highlightthickness=1)
osc3 = tk.Frame(master=window,highlightbackground="grey", highlightthickness=1)

osc1_title = tk.Label(master=osc1, text="Osc 1")
osc2_title = tk.Label(master=osc2, text="Osc 2")
osc3_title = tk.Label(master=osc3, text="Osc 3")

osc1_label = tk.Label(master=osc1, text="Level")
osc2_label = tk.Label(master=osc2, text="Level")
osc3_label = tk.Label(master=osc3, text="Level")

osc1_option = tk.StringVar(value="saw")
osc2_option = tk.StringVar(value="saw")
osc3_option = tk.StringVar(value="saw")

osc1_type = tk.OptionMenu(
    osc1,
    osc1_option,
    *model.osc_options,
)

osc2_type = tk.OptionMenu(
    osc2,
    osc2_option,
    *model.osc_options,
)

osc3_type = tk.OptionMenu(
    osc3,
    osc3_option,
    *model.osc_options,
)

osc1_level = tk.Scale(
    master=osc1, 
    orient="horizontal"
)
osc2_level = tk.Scale(
    master=osc2,
    orient="horizontal"
)
osc3_level = tk.Scale(
    master=osc3, 
    orient="horizontal"
)

progresslabel = tk.Label(master=window, text="Soundblend incomplete.", fg="red")
filelabel = tk.Label(master=window, text="Modulator file: (None)",)
buttonframe = tk.Frame(master=window)

vox = tk.Button(
    master = buttonframe,
    image=vox_tkimg,
    command=vox,
)

play = tk.Button(
    master = buttonframe,
    image=play_tkimg,
    command=play,
)

download = tk.Button(
    master = buttonframe,
    image=download_tkimg,
    command=download,
)

uploadFile = tk.Button(
    master=window,
    text="Upload File",
    command=uploadFile,
)

osc1.pack()
osc1_title.pack()
osc1_type.pack()
osc1_label.pack(side="left")
osc1_level.pack(side="left")
osc1_level.set(50)

osc2.pack()
osc2_title.pack()
osc2_type.pack()
osc2_label.pack(side="left")
osc2_level.pack(side="left")
osc2_level.set(50)

osc3.pack()
osc3_title.pack()
osc3_type.pack()
osc3_label.pack(side="left")
osc3_level.pack(side="left")
osc3_level.set(50)

progresslabel.pack()
filelabel.pack()
buttonframe.pack()
play.pack(side="left")
vox.pack(side="left")
download.pack(side="left")
uploadFile.pack()

window.mainloop()