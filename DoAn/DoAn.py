from tkinter import filedialog
from tkinter import *
import cv2 as cv
import tkinter
from PIL import Image,ImageTk
import numpy as np
import PIL
s=""
img2=np.zeros((5,5))
def UploadAction():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    img=cv.imread(filename)
    global s
    s =filename
    cimg=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
    global w,h
    print (w,h)
    lcanvas.create_image(0,0,image=cimg,anchor=tkinter.NW)
    lcanvas.pack()
    lcanvas.image = cimg


def amBan():
    img=cv.imread(s,1)
    img=~img
    cimg = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
    rcanvas.create_image(0, 0, image=cimg, anchor=tkinter.NW)
    rcanvas.pack()
    rcanvas.image = cimg
def Log():
    img = cv.imread(s)
    return
def luythua():
    return

def histogram():
    img=cv.imread(s,0)
    img=cv.equalizeHist(img)
    cimg = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
    rcanvas.create_image(0, 0, image=cimg, anchor=tkinter.NW)
    rcanvas.pack()
    rcanvas.image = cimg



win = Tk()
win.state('zoomed')
menu = Menu(win)
win.config(menu=menu)
###Image
imgfile=Menu(menu)
menu.add_cascade(label="Open",menu=imgfile)
imgfile.add_command(label="Open Image",command=(UploadAction))
imgfile.add_separator()
imgfile.add_command(label="Exit",command=win.quit)


##Chương 3
feature = Menu(menu)
menu.add_cascade(label="Chương 3", menu=feature)
feature.add_command(label="Âm bản",command=amBan)
feature.add_command(label="Log",command=Log)
feature.add_command(label="Lũy thừa")
feature.add_command(label="Cân bằng Histogram",command=histogram)
feature.add_separator()

##Chương 4
C4 = Menu(menu)
menu.add_cascade(label="Chương 4", menu=C4)
C4.add_command(label="Lọc trung bình" )
C4.add_command(label="Lọc trung vị")
C4.add_command(label="Lũy thứ tự")
C4.add_command(label="Lọc Gaussian")
C4.add_command(label="Lọc Hight-boost")
C4.add_command(label="Làm sắc net ảnh bằng Laplacian")
C4.add_command(label="Làm sắc net ảnh bằng Hight-boost")
C4.add_command(label="Làm sắc net ảnh bằng Unsharp")
C4.add_separator()

##Chương 5

C5 = Menu(menu)
menu.add_cascade(label="Chương 5", menu=C5)

C5.add_separator()


helpmenu=Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Call to Thanh" )

win.update_idletasks()
#------------------------------------#------------------------------------#

lframe = Frame(win,width=win.winfo_width()/2,heigh=win.winfo_height()*3/4, bg ='gray')
lframe.pack(side=LEFT,expand=1, anchor=N)

rframe = Frame(win,width=win.winfo_width()/2,heigh=win.winfo_height()*3/4, bg ='gray')
rframe.pack( side = RIGHT,expand=1, anchor=N)

lcanvas = Canvas(lframe,width=win.winfo_width()/2,heigh=win.winfo_height()*3/4, bg ='white')
lcanvas.pack(side=LEFT,expand=YES,fill=BOTH)

w=width=win.winfo_width()/2
h=heigh=win.winfo_height()*3/4

rcanvas = Canvas(rframe,width=win.winfo_width()/2,heigh=win.winfo_height()*3/4, bg ='white')
rcanvas.pack(side=RIGHT,expand=YES,fill=BOTH)


mainloop()