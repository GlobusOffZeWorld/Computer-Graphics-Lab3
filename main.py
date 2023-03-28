import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from  PIL import ImageTk, Image
import os 

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("My Application")

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.select_button = tk.Button(self.button_frame, text="Select File", command=self.select_file, height=2, width=20)
        self.select_button.pack(side=tk.LEFT, padx=10)

        self.refresh_button = tk.Button(self.button_frame, text="Refresh", command=self.refresh, height=2, width=20)
        self.refresh_button.pack(side=tk.LEFT, padx=10)

        self.image_table = tk.Frame(self.master)
        self.image_table.pack(fill=tk.BOTH, expand=True)

        for i in range(2):
            self.image_table.rowconfigure(i, weight=1, minsize=300)
            for j in range(3):
                self.image_table.columnconfigure(j, weight=1, minsize=300)
                cell_label = tk.Label(self.image_table)
                cell_label.grid(row=i, column=j, sticky="nsew")

 
    def select_file(self):
        self.image_path = filedialog.askopenfilename()
        self.refresh()
                    
    def refresh(self):
        img = cv.imread(self.image_path, 1)
        blur = cv.GaussianBlur(img, (51, 51), 0)

        loc1 = local1(img)
        loc2 = local2(img)
        adapt1 = adaptive1(img)
        adapt2 = adaptive2(img)
      
        img = self.convertImage(img)
        
        blur = self.convertImage(blur)
        
        loc1 = self.convertImage(loc1)
        loc2 = self.convertImage(loc2)
        adapt1 = self.convertImage(adapt1)
        adapt2 = self.convertImage(adapt2)

        
        
        cell_1 = self.image_table.grid_slaves(row=0, column=0)[0]
        cell_1.configure(image=img, compound='top', text='img')
        cell_1.image = img

        cell_2 = self.image_table.grid_slaves(row=0, column=1)[0]
        cell_2.configure(image=blur, compound='top', text='blur')
        cell_2.image = blur

        cell_3 = self.image_table.grid_slaves(row=0, column=2)[0]
        cell_3.configure(image=loc1, compound='top', text='local1')
        cell_3.image = loc1

        cell_4 = self.image_table.grid_slaves(row=1, column=0)[0]
        cell_4.configure(image=loc2, compound='top', text='local2')
        cell_4.image = loc2

        cell_5 = self.image_table.grid_slaves(row=1, column=1)[0]
        cell_5.configure(image=adapt1, compound='top', text='adaptive1')
        cell_5.image = adapt1

        cell_6 = self.image_table.grid_slaves(row=1, column=2)[0]
        cell_6.configure(image=adapt2, compound='top', text='adaptive2')
        cell_6.image = adapt2

    def convertImage(self, img):
            cell_width = self.image_table.winfo_width() // 3
            cell_height = self.image_table.winfo_height() // 2
        
            width = img.shape[0]
            height = img.shape[1]
            max_size = 300
            if cell_width < cell_height:
                max_size = cell_width - 40
            else:
                max_size = cell_height - 40

            if width < height:
                ratio = max_size / width
            else:
                ratio = max_size / height
                
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = cv.resize(img, (new_height, new_width ))

            img = Image.fromarray(img)

            img = ImageTk.PhotoImage(img)
            return img


def local1(img):
    mean_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret2, th2 = cv.threshold(mean_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return th2

def local2(img): 
    mean_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret2, th2 = cv.threshold(mean_img, 0, 255, cv.THRESH_TRIANGLE)
    return th2

def adaptive1(img):
    mean_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    arr2 = cv.adaptiveThreshold(mean_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 5, 20)
    return arr2

def adaptive2(img):
    mean_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    arr2 = cv.adaptiveThreshold(mean_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 5, 20)
    return arr2

def main():
    root = tk.Tk()
    app = Application(master=root)

    app.mainloop()

if __name__ == '__main__':
    main()
