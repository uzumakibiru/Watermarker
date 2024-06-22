from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk,ImageGrab,ImageDraw,ImageFont
from tkinter import messagebox



class UploadImage():
    def __init__(self):
        # Create a canvas
        self.canvas=Canvas(height=300,width=300,bg="light blue")
        self.canvas.grid(row=0,column=0,columnspan=3)
        self.img_id=None
        
        #Upload button inside the canvas
        self.add_button()
        
    def upload(self):
        #Open a folder to select the image
        self.file_path=filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if self.file_path:
            self.display_image(self.file_path)

            #Create a area for file path to display
            self.file_path_label=Label(text="Add Your Watermark Text")
            self.file_path_label.grid(row=1,column=1,columnspan=1,pady=10)
            #Crete a text ENtry for the watermark
            self.entry= Entry(text="",width=50)
            self.entry.grid(row=2,column=0,columnspan=3)
            #Create a button to add the watermark on the image
            self.convert_button= Button(text="Apply",command=self.transform,width=20)
            self.convert_button.grid(row=4,column=0,columnspan=3,pady=10)
            #Create a change in mind button
            self.add_new=Button(text="New Image",command=self.add_button,width=20)
            self.add_new.grid(row=5,column=0,columnspan=3)
            #Slider
            self.slider()
    
    def display_image(self,file_path):
        # Remove the button from the canvas to display an image
        self.remove_button(self.upload_button)
        #Display image in the canvas by converting the image to photoimage that TKinter can process.
        img_path=Image.open(file_path)
        self.width_cv=300
        self.height_cv=300
       
        img_path = img_path.resize((300, 300), Image.BILINEAR)
        if self.img_id is None:
            # self.canvas.config(width=self.width_cv, height=self.height_cv)
            self.img=ImageTk.PhotoImage(img_path)
            self.img_id=self.canvas.create_image(self.width_cv//2,self.height_cv//2,image=self.img)

 # Function to add button on the canvas
    def add_button(self):
        if self.img_id is not None:
            try:
                UploadImage()
                self.file_path_label.destroy()
                self.entry.destroy()
                self.scale.destroy()
                self.remove_button(self.convert_button)
                self.remove_button(self.add_new)
                self.remove_button(self.download_button)
            except:
                print("No Tk object")
        
        self.upload_button= Button(self.canvas,text="Upload",command=self.upload)
        self.canvas.create_window(150,150,window=self.upload_button)

        #Remove the button from the canvas
    def remove_button(self,button):
        button.destroy()        

    def transform(self):
        #Brings the download button
        response= messagebox.askyesno("Save the changes")
        if response:
            self.file_path_label.destroy()
            self.entry.destroy()
            self.scale.destroy()
            self.remove_button(self.convert_button)

            self.download_button= Button(text="Download",command=self.download,width=20)
            self.download_button.grid(row=3,column=0,columnspan=3,pady=10)

    def create_transparent_text(self,text):
        x=75
        y=55
        transparency=self.scale.get()
        font = ImageFont.truetype("arial.ttf", 24)

        # Create a blank image with transparent background
        image = Image.new("RGBA", (300, 50), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Draw text with specified font and color
        draw.text((80, 0), text, font=font, fill=(0, 0, 0, transparency))
        rotated_image = image.rotate(45, expand=True)
        # Convert the image to a format compatible with Tkinter
        img_tk = ImageTk.PhotoImage(rotated_image)

        # Display the image on the canvas
        for _ in range(5):
            self.transparent_text_id=self.canvas.create_image(x, y, image=img_tk, anchor="center")
            y+=50
            x+=50

        # Keep a reference to the image to prevent it from being garbage collected
        self.canvas.image = img_tk
        
    #Fucntion to open the file location for download process
    def download(self):
        save_path= filedialog.asksaveasfile(defaultextension=".png",filetypes=[("PNG files","*.png")])
        if save_path:
            try:
                #Capture the content of the canvas as PNG
                x0=self.canvas.winfo_rootx()
                y0=self.canvas.winfo_rooty()
                x1=x0+self.canvas.winfo_width()
                y1=y0+self.canvas.winfo_height()

                image_grab=ImageGrab.grab(bbox=(x0,y0,x1,y1))
                image_grab.save(save_path.name)
                save_path.close()
                UploadImage()
                self.remove_button(self.add_new)
                self.remove_button(self.download_button)

            except Exception as e:
                print(f"Failed {str(e)}")

    #Add scale for the tranparency
    def slider(self):
        self.scale=Scale(from_=0,to=255,orient=HORIZONTAL,label="Transparency Level")
        self.scale.set(128)
        self.scale.grid(row=3,column=0,columnspan=3)
        self.scale.bind("<Motion>",self.update_text)

    def update_text(self, event=None):
        self.create_transparent_text(self.entry.get())