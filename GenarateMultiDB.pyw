from tkinter import Label, Button
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage, StringVar, SUNKEN, W, X, BOTTOM
from os import path
import MultiDBProcessing
import threading, sys

class GUI_COntroller:
    '''
	   This class initialize the required controls for TkInter GUI
	'''
    def __init__(self,TkObject):
 
 
	    #Load company image
        Imageloc=tk.PhotoImage(file='alstom_logo.gif')		
        label3=Label(image=Imageloc,)
        label3.image = Imageloc		
        label3.place(x=200,y=30)
		
	
	    #SAEntry = Entry(root,takefocus=False,justify=tk.CENTER,font=50,)

        global TkObject_ref

        TkObject_ref =  TkObject       

		
        #label
        global label1		
        label1 = Label(TkObject,bd=7, text="MultiDB generation from individual territories", bg="orange", fg="black",width=60, font=200)	
        label1.place(x=100,y=130)
        label1.config(font=('helvetica',12,'bold'))		

        #select file
        global 	button1	
        button1=Button(TkObject,activebackground='green',borderwidth=5, text='Click here to select multiDB path',width=25, command=GUI_COntroller.selectDirectory)
        button1.place(x=200,y=230)
        button1.config(font=('helvetica',12,'bold'))

        #Exit Window
        global button2		
        button2=Button(TkObject,activebackground='green',borderwidth=5, text='Close Window', command=GUI_COntroller.exitWindow)
        button2.place(x=530,y=230)	
        button2.config(font=('helvetica',12,'bold'))		

    def exitWindow():
            TkObject_ref.destroy()

    def selectDirectory():
            global selectedDir
            selectedDir = filedialog.askdirectory(initialdir = "/")
            if not path.isdir(selectedDir):
                messagebox.showerror('Error','Please select a valid directory!')				
            else:
                label1.destroy()
                button1.destroy()	

                label4= Label(TkObject_ref,bg='orange',text='Selected Directory: '+selectedDir,font=40)
                label4.place(x=100,y=130)				
			 
                button5 = Button(TkObject_ref,text='Convert to MultiDB',font=10,bd=5,command=MultiDB.RunTest)
                button5.place(x=200,y=230)	
                button5.config(font=('helvetica',12,'bold'))				
	
class MultiDB:
    def RunTest(): 

        global thread,statusBarText	
	
        statusBarText = StringVar()		
        StatusLabel = Label(TkObject_ref, textvariable=statusBarText, fg="green", bd=1,relief=SUNKEN,anchor=W) 
        StatusLabel.config(font=('helvetica',11,'bold'))
        StatusLabel.pack(side=BOTTOM, fill=X)
        statusBarText.set("DB conversion in progress...")
		
        thread = threading.Thread(target=MultiDBProcessing.script_exe, args = (selectedDir,TkObject_ref,statusBarText))
        thread.start()

if __name__ == '__main__':	
	
       root = tk.Tk()
       
       #Change the background window color
       root.configure(background='gray')     
       
       #Set window parameters
       root.geometry('850x500')
       root.title('MultiDB generation from individual territories')
       
       #Removes the maximizing option
       root.resizable(0,0)
       
       ObjController = GUI_COntroller(root)
       
       #keep the main window is running
       root.mainloop()
       sys.exit()
