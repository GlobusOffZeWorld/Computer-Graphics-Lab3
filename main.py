import cv2 as cv
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("My Application")

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.select_button = tk.Button(
            self.button_frame, text="Select File", command=self.select_file, height=2, width=20)
        self.select_button.pack(side=tk.LEFT, padx=10)

        self.refresh_button = tk.Button(
            self.button_frame, text="Refresh", command=self.refresh, height=2, width=20)
        self.refresh_button.pack(side=tk.LEFT, padx=10)

        self.image_table = tk.Frame(self.master)
        self.image_table.pack(fill=tk.BOTH, expand=True)
        self.TABLE_SIZE = 6

        for i in range(2):
            self.image_table.rowconfigure(i, weight=1, minsize=300)
            for j in range(3):
                self.image_table.columnconfigure(j, weight=1, minsize=300)
                cell_label = tk.Label(self.image_table)
                cell_label.grid(row=i, column=j, sticky="nsew")

    def select_file(self):
        self.clear_images()
        self.image_path = filedialog.askopenfilename()
        self.refresh()

    def add_image(self, img, text):
        for i in range(self.TABLE_SIZE):
            cell_label = self.image_table.grid_slaves(
                row=i // 3, column=i % 3)[0]
            if not cell_label.cget("image"):
                cell_label.configure(image=img, compound='top', text=text)
                cell_label.image = img
                return

    def clear_images(self):
        for i in range(self.TABLE_SIZE):
            cell_label = self.image_table.grid_slaves(
                row=i // 3, column=i % 3)[0]
            cell_label.configure(image='', text='')

    def refresh(self):
        self.clear_images()
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

        self.add_image(img, 'img')
        self.add_image(blur, 'blur')
        self.add_image(loc1, 'local1')
        self.add_image(loc2, 'local2')
        self.add_image(adapt1, 'local1')
        self.add_image(adapt2, 'local2')

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
        img = cv.resize(img, (new_height, new_width))

        img = Image.fromarray(img)

        img = ImageTk.PhotoImage(img)
        return img


def local1(img):
    mean_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret2, th2 = cv.threshold(
        mean_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return th2


def local2(img):
    mean_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret2, th2 = cv.threshold(mean_img, 0, 255, cv.THRESH_TRIANGLE)
    return th2


def adaptive1(img):
    mean_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    arr2 = cv.adaptiveThreshold(
        mean_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 5, 20)
    return arr2


def adaptive2(img):
    mean_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    arr2 = cv.adaptiveThreshold(
        mean_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 5, 20)
    return arr2


def main():
    root = tk.Tk()
    app = Application(master=root)

    app.mainloop()


if __name__ == '__main__':
    main()
