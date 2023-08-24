from tkinter import *
from tkinter import colorchooser,messagebox
from PIL import Image, ImageTk
import keyboard
import pyautogui
import threading
import clipboard

class ColorTools:
    def __init__(self, root):
        self.root = root
        self.hexCode = ""
        self.rgbCode = ""

        self.colorPickerBtn = Button(self.root, text="Pick Color", command=self.getColorPalette).grid(padx=(12,20))

        self.colorDetectorBtn = Button(self.root, text="Detect Color", command=self.detectColor)
        self.colorDetectorBtn.grid(row=0, column=1)

        self.frame = Frame(self.root,highlightthickness=2, highlightbackground="black")
        self.frame.grid(row=1, columnspan=2, pady=(30), ipadx=10, ipady=10)

        self.hexLabel = Label(self.frame, text="Hex Code : ")
        self.hexLabel.grid(padx=(10,0), pady=10)
        self.hexCodeEntry = Entry(self.frame, text="", width=10)
        self.hexCodeEntry.grid(row=0, column=1, sticky=W, pady=10)
        self.copybtn1 = Button(self.frame, image=copyImg, command=self.copyHex)
        self.copybtn1.grid(row=0, column=2, padx=(10,0))

        self.rgbLabel = Label(self.frame, text="RGB Code : ")
        self.rgbLabel.grid(padx=(10,0))
        self.rgbCodeEntry = Entry(self.frame, text="", width=10)
        self.rgbCodeEntry.grid(row=1, column=1, sticky=W)
        self.copybtn2 = Button(self.frame, image=copyImg, command=self.copyRgb)
        self.copybtn2.grid(row=1, column=2, padx=(10,0))

    def copyHex(self):
        clipboard.copy(str(self.hexCode))

    def copyRgb(self):
        clipboard.copy(str(self.rgbCode))

    def detectColor(self):
        def show_notice():
            notice_text = "Press 'ctrl' key + move cursor to detect color..!!"
            messagebox.showinfo("Notice", notice_text)
        show_notice()
        t = threading.Thread(target=self.detect)
        t.daemon = True
        t.start()

    def detect(self):
        while 1:
            if keyboard.is_pressed("ctrl"):
                x, y = pyautogui.position()
                color = pyautogui.pixel(x, y)
                self.rgbCode = "{},{},{}".format(color[0], color[1], color[2])
                self.hexCode = "#{:02X}{:02X}{:02X}".format(color[0], color[1], color[2])
                self.updateColor()

    def getColorPalette(self):
        color = colorchooser.askcolor()
        c = color[0]
        self.rgbCode = "{},{},{}".format(c[0], c[1], c[2])
        self.hexCode = color[1]
        self.updateColor()

    def updateColor(self):
        self.hexCodeEntry.delete(0,END)
        self.hexCodeEntry.insert(0,self.hexCode)

        self.rgbCodeEntry.delete(0,END)
        self.rgbCodeEntry.insert(0,self.rgbCode)

        root.config(bg=self.hexCode)

def loadImage(image_path, size = (23,23)):
    image_pil = Image.open(image_path)
    image_pil = image_pil.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image_pil)

root = Tk()
root.title("Color Picker")
root.geometry("320x210")
root.iconbitmap("Icon.ico")
root.config(padx=20, pady=20)
copyImg = loadImage("copy.png")
ColorTools(root)
root.mainloop()