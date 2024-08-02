from tkinter import *
import subprocess

window = Tk()
window.geometry("700x300")
window.title("download")
def click():
    link = entry1.get()
    name = entry2.get()
    link = f'ffmpeg -i "{link}" -c copy {name}.ts'
    entry1.delete(0, len(entry1.get()))
    entry2.delete(0, len(entry2.get()))
    subprocess.run(link)


label1 = Label(window, text="link")
label1.place(x=30, y=10)
entry1 = Entry(window)
entry1.place(x=70, y=10, width=250, height=25)

button = Button(window, text="download", width=8, height=3, command=click)
button.place(x=330, y=10)

label2 = Label(window, text="name")
label2.place(x=30, y=40)
entry2 = Entry(window)
entry2.place(x=70, y=40, width=250, height=25)


window.mainloop()