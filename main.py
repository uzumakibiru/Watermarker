from tkinter import *
from Upload import *
from ImageWater import ImageWaterMaker

window= Tk()
window.title("Watermarker")
# window.geometry("400x600")
window.config(padx=20,pady=20)
def text_water():
    UploadImage()
    text.destroy()  
    image.destroy()
    label.destroy()

def image_water():
    ImageWaterMaker()
    image.destroy()
    text.destroy() 
    label.destroy()

label= Label(text="Choose one of the fetaure: ",font=("Helvetica", 10, "bold"))
label.grid(row=0,column=0,columnspan=3)

text=Button(text="Text",command=text_water,width=25)
text.grid(row=1,column=0,columnspan=3,padx=50,pady=20)

image=Button(text="Image",command=image_water,width=25)
image.grid(row=2,column=0,columnspan=3)

window.mainloop()