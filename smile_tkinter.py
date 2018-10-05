from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import numpy as np
import dlib
import cv2
from tkinter import *
from PIL import Image,ImageTk
import time
import re
from tkinter import messagebox
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from threading import Thread

def mail(name,email):
    t = name+'.jpg'
    img_data = open(t, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Smiling Rajasthan'
    msg['From'] = 'nakulswims@gmail.com'
    msg['To'] = email


    image = MIMEImage(img_data, name=os.path.basename(t))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.ehlo()
    s.login('nakulswims@gmail.com', 'jaijaijaihanumanji')
    s.sendmail('nakulswims@gmail.com', email,msg.as_string())
    s.close()

def preview(name,email,root1):
    x = cv2.imread(name+'.jpg')
    cv2.namedWindow("preview", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    now = time.time() + 3
    while time.time()<now:
        cv2.imshow('preview',x)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    thankyou(name,email,root1)

def thankyou(name,email,root1):
    root1.destroy()    
    root = Tk()
    root.title('Smile_detector')
    p1 = Image.open('3.png')
    p1 = ImageTk.PhotoImage(p1)
    yscrollbar = Scrollbar(root,orient = VERTICAL)
    canvas = Canvas(root,width = 1080,height = 1920,yscrollcommand = yscrollbar.set)
    l = Label(canvas,image = p1)
    l.pack(fill = BOTH,expand = YES)
    yscrollbar.config(command=canvas.yview)
    yscrollbar.pack(side = RIGHT,fill = BOTH)
    canvas.pack(fill = BOTH,expand = True)
    root.after(2000,lambda:root.destroy())
    root.mainloop()

    t1 = Thread(target = letsgo).start()
    t2 = Thread(target = mail,args = (name,email)).start()
    
    
       



     
def smile(mouth):
    MAR = dist.euclidean(mouth[0], mouth[6])
    return MAR

def isValidEmail(email):
            if len(email) > 7:
                if re.search("[@.]",email) != None:
                    return True
            return False

def main(root1,name, email):
    flag = True
    name=name.get()
    email=email.get()

    if(name=='' and email==''):
        messagebox.showinfo("Alert", "Please enter your Name and Email. ")
    elif(email==''):
        messagebox.showinfo("Alert", "Please enter your Email. ")
    elif(name==''):
        messagebox.showinfo("Alert", "Please enter your Name. ")

    else:
        t = isValidEmail(email)
        if t == False:
            messagebox.showinfo("Alert", "Please enter your Correct Email. ")
    
        else:
                
            shape_predictor= "shape_predictor_68_face_landmarks.dat"
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor(shape_predictor)
            
            
            (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
            
            print("[INFO] starting video stream thread...")
            cap = cv2.VideoCapture(0)
            cv2.namedWindow("Smile-Detector", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Smile-Detector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            
            while flag:
                _,frame = cap.read()
                frame = imutils.resize(frame, width=600)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rects = detector(gray, 0)
                for rect in rects:
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    mouth = shape[mStart:mEnd]
                    MAR = smile(mouth)
                
                
                
                    if MAR >= 52 and MAR < 53:
                        cv2.putText(frame, '60%', (rect.right(), rect.bottom()), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    elif MAR >= 53 and MAR < 54:
                        cv2.putText(frame, '80%', (rect.right(), rect.bottom()), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    elif MAR >= 55:
                        cv2.putText(frame, '100%', (rect.right(), rect.bottom()), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        cv2.imwrite(name+'.jpg',frame)
                        flag = False
                        
                    elif MAR <49:
                        cv2.putText(frame, 'Not-Smiling', (rect.right(), rect.bottom()), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    elif MAR >50 and MAR < 51:
                        cv2.putText(frame, '40%', (rect.right(), rect.bottom()), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                if flag == False:
                    del cap
                    preview(name,email,root1)


                cv2.imshow("Smile-Detector", frame)
            
                key2 = cv2.waitKey(1) & 0xFF
                if key2 == ord('q'):
                    break
            
            
            cv2.destroyAllWindows()
    
def login(root):
    root.destroy()
    root1 = Tk()
    root1.title('Login Page')
    p2 = Image.open('2.png')
    p2 = ImageTk.PhotoImage(p2)
    btnimg1 = Image.open('7.jpg')
    btnimg1 = ImageTk.PhotoImage(btnimg1)


    yscrollbar = Scrollbar(root1,orient = VERTICAL)
    canvas = Canvas(root1,width = 1080,height = 1920,yscrollcommand = yscrollbar.set)
    canvas.create_image(542,970,image=p2)
    name = Entry(canvas, width=20, font=('Times', 18))
    id = canvas.create_window(655,760, window=name)
    email = Entry(canvas, width=20, font=('Times', 18))
    id = canvas.create_window(655,910, window=email)
    btn2 = Button(canvas,image = btnimg1,bg = 'white',padx=0,pady=0,command = lambda:main(root1,name,email))
    canvas.create_window(553,1057,window = btn2)
    yscrollbar.config(command=canvas.yview)
    yscrollbar.pack(side = RIGHT,fill = BOTH)
    canvas.pack()
    root1.mainloop()
    

def letsgo():

    root = Tk()
    root.title('Smile_detector')
    p1 = Image.open('1.png')
    p1 = ImageTk.PhotoImage(p1)
    btnimg = Image.open('6.jpg')
    btnimg = ImageTk.PhotoImage(btnimg)

    yscrollbar = Scrollbar(root,orient = VERTICAL)

    canvas = Canvas(root,width = 1080,height = 1920,yscrollcommand = yscrollbar.set)
    l = Label(canvas,image = p1)
    l.pack(fill = BOTH,expand = YES)
    btn1 = Button(canvas,image = btnimg,bg = 'white',padx=0,pady=0,bd = 0,command = lambda:login(root))
    canvas.create_window(273,1316,window = btn1)
    yscrollbar.config(command=canvas.yview)
    yscrollbar.pack(side = RIGHT,fill = BOTH)
    canvas.pack(fill = BOTH,expand = True)
    root.mainloop()
    
while 1:
    letsgo()
