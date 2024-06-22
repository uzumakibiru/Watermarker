from tkinter import *
from Upload import *

window= Tk()
window.title("Watermarker")
window.geometry("400x600")
window.config(padx=50,pady=50)

upload=UploadImage()


window.mainloop()