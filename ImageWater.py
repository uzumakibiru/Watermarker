from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk,ImageGrab,ImageDraw,ImageFont
from tkinter import messagebox



class ImageWaterMaker():
    def __init__(self):
        self.title=Label(text="Image Watermarker",font=("Helvetica", 12, "bold"))
        self.title.grid(row=0,column=1)

        self.change=Button(text="Try Text",command=self.textmaker)
        self.change.grid(row=0,column=3)
        # Create a canvas
        self.canvas=Canvas(height=300,width=300,bg="light blue")
        self.canvas.grid(row=1,column=1,columnspan=3)
        self.img_id=None
        

        
        #Upload button inside the canvas
        self.add_button()
        
    def upload(self):
        # Remove the button from the canvas to display an image
        self.remove_button(self.upload_button)
        #Open a folder to select the image
        self.file_path=filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if self.file_path:
            
            self.display_image(self.file_path)

            #Create a area for file path to display
            # self.file_path_label=Label(text="Upload Your Watermark Text")
            # self.file_path_label.grid(row=2,column=1,columnspan=3,pady=5)
            #Crete a text ENtry for the watermark
            self.entry= Button(text="Upload WatermarkLogo",command=self.upload_image)
            self.entry.grid(row=3,column=1,columnspan=3)
            #Create a button to add the watermark on the image
            self.convert_button= Button(text="Apply",command=self.transform,width=20)
            self.convert_button.grid(row=5,column=1,columnspan=3,pady=10)
            #Create a change in mind button
            self.add_new=Button(text="New Image",command=self.add_button,width=20)
            self.add_new.grid(row=6,column=1,columnspan=3)
            
    
    def display_image(self,file_path):
        
        
        #Display image in the canvas by converting the image to photoimage that TKinter can process.
        img_path=Image.open(file_path)
        self.width_cv=img_path.width
        self.height_cv=img_path.height
       
        # img_path = img_path.resize((300, 300), Image.BILINEAR)
        if self.img_id is None:
            print("Upload")
            self.canvas.config(width=self.width_cv, height=self.height_cv)
            self.img=ImageTk.PhotoImage(img_path)
            self.img_id=self.canvas.create_image(self.width_cv//2,self.height_cv//2,image=self.img)

 # Function to add button on the canvas
    def add_button(self):
        if self.img_id is not None:
            try:
                # ImageWaterMaker()
                self.canvas.config(width=300, height=300)
                self.canvas.delete(self.img_id)
                # self.file_path_label.destroy()
                self.entry.destroy()
                self.scale.destroy()
                self.remove_button(self.convert_button)
                self.remove_button(self.add_new)
                self.remove_button(self.download_button)
                
                
            except:
                print("No Tk object")
        self.img_id=None
        self.upload_button= Button(self.canvas,text="Upload",command=self.upload)
        self.canvas.create_window(150,150,window=self.upload_button)
        

        #Remove the button from the canvas
    def remove_button(self,button):
        button.destroy()        

    def transform(self):
        #Brings the download button
        response= messagebox.askyesno("Save the changes")
        if response:
            # self.file_path_label.destroy()
            self.entry.destroy()
            self.scale.destroy()
            self.remove_button(self.convert_button)

            self.download_button= Button(text="Download",command=self.download,width=20)
            self.download_button.grid(row=3,column=1,columnspan=3,pady=10)

    def upload_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        
        if file_path:
            # Open the image using Pillow
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.original_image = self.original_image.resize((50, 50), Image.BILINEAR)
            # Display the image initially with default transparency
            self.update_transparency(128)
            #Slider
            self.slider()

    def update_transparency(self, value):
        # Convert slider value to transparency alpha value (0-255)
        alpha = int(value)
        print(alpha)

        if self.original_image:
            # Make the image transparent (convert to RGBA if not already)
            self.transparent_image = self.make_transparent(self.original_image, alpha)

            # Convert the transparent image to Tkinter PhotoImage
            self.img_tk = ImageTk.PhotoImage(self.transparent_image)

            # Display the image on the canvas
            self.canvas.create_image(self.width_cv-40, self.height_cv-40, image=self.img_tk, anchor="center")

    def make_transparent(self, image,alpha):
        # Convert image to RGBA mode (if not already in RGBA)
        image = image.convert("RGBA")

        data = image.getdata()

        # Modify alpha channel to make image transparent
        transparent_data = [(r, g, b, alpha) for r, g, b, a in data]
        
        # Composite original image onto transparent background
        transparent_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
        transparent_image.putdata(transparent_data)

        return transparent_image


        
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
                self.canvas.config(width=300, height=300)
                ImageWaterMaker()
                self.remove_button(self.add_new)
                self.remove_button(self.download_button)

            except Exception as e:
                print(f"Failed {str(e)}")

    #Add scale for the tranparency
    def slider(self):
        self.scale=Scale(from_=0,to=255,orient=HORIZONTAL,label="Transparency Level",command=self.update_transparency)
        self.scale.set(128)
        self.scale.grid(row=4,column=1,columnspan=3)
        

    # def update_text(self, event=None):
    #     self.create_transparent_text()

    