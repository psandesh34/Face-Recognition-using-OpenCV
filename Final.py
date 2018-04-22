import cv2
import numpy as np
import urllib.request as ur
from xlutils.copy import copy
import xlrd
from datetime import date
import sqlite3
import matplotlib.pyplot as plt
import xlsxwriter
from tkinter import *
import tkinter as tk
from tkinter.ttk import Separator,Style
from PIL import Image
import os




#all declarations
global students
students = {1:16141201}
global rollno
rollno =[]
global hist_data
hist_data = []*80
global present
#initialize list of 23 elements

def add():# creates array of 80 students
    keyword=16141200
    for i in range(80):
        students[i]=keyword+i
        rollno.append(i)
        
def datasetcreater(): # This function captures the images from the Camera input(In this case:Android)
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def insert(ID,Name):#stores the name and ID of student in a database file
        conn=sqlite3.connect("FaceBase.db")
        cmd="SELECT * FROM People Where ID="+str(ID)
        cursor=conn.execute(cmd)
        doesRecordExist=0
        for row in cursor:
            doesRecordExist=1
        if(doesRecordExist==1):
            cmd="UPDATE People SET Name="+str(Name)+"WHERE ID="+str(ID)
        else:
            cmd="INSERT INTO People(ID,Name) Values("+str(ID)+","+str(Name)+")"
        conn.execute(cmd)
        conn.commit()
        conn.close()
        
    url='http://192.168.43.1:8080/shot.jpg'
    imgr=ur.urlopen(url)
    sampleNum=0;
    ID=input('enter user id : ')
    Name=input('enter your name : ')
    #Age=input('Enter Age : ')
    insert(ID, Name)
    while True:# Captures the images and saves them in specified path
        imgr=ur.urlopen(url)
        imgnp=np.array(bytearray(imgr.read()),dtype=np.uint8)
        img=cv2.imdecode(imgnp,-1)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            sampleNum=sampleNum+1
            cv2.imwrite("dataSet/User."+str(ID)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.waitKey(3);
        cv2.imshow("Face",img);
        cv2.waitKey(10);
        if(sampleNum>40):
            break
    cv2.destroyAllWindows()
    
    
def trainer():#Trains the Captured Images.. 
    recognizer=cv2.face.LBPHFaceRecognizer_create();#displays path of all captured images
    path='dataset'#relative path
    
    
    def getImagesWithID(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)]#lists all directories in dataset folder
        faces=[]
        IDs=[]
        for imagePath in imagePaths:
            faceImg=Image.open(imagePath).convert('L');#this creates image in PIL format
            faceNp=np.array(faceImg,'uint8')
            ID=int(os.path.split(imagePath)[-1].split('.')[1])#splits the paths of the images
            faces.append(faceNp)
            print(ID)
            IDs.append(ID)
            cv2.imshow("training",faceNp)
            cv2.waitKey(40)
        return IDs, faces        
    
    
    
    
    IDs,faces = getImagesWithID(path)    
    recognizer.train(faces,np.array(IDs))
    recognizer.write('recognizer/trainingData.yml')
    cv2.destroyAllWindows()   
    
def detector():#Detects a recognized face
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    rec=cv2.face.LBPHFaceRecognizer_create();
    rec.read("recognizer/trainingData.yml")
    ID=0
    font=cv2.FONT_HERSHEY_SIMPLEX
    url='http://192.168.43.1:8080/shot.jpg'
    imgr=ur.urlopen(url)
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT c FROM Counter"
    cursor = conn.execute(cmd)
    c=cursor.fetchone()
    cnt=c[0]
    #print(str(cnt))    
    cmd="UPDATE Counter SET c ="+str(cnt+1)
    conn.execute(cmd)
    conn.commit()
    conn.close()
    date1= date.today()
    rb= xlrd.open_workbook('student.xls')
    wb= copy(rb)
    
    w_sheet=wb.get_sheet(0)
    w_sheet.write(0,cnt,str(date1))
    
    while True:
        imgr=ur.urlopen(url)
        imgnp=np.array(bytearray(imgr.read()),dtype=np.uint8)
        img=cv2.imdecode(imgnp,-1)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,165,0),4)
            ID,conf=rec.predict(gray[y:y+h,x:x+w])
            if conf<40:
                cv2.putText(img,str(ID)+str(round(conf)),(x,y+h),font,3,(255,255,255),4,cv2.LINE_AA);
                w_sheet.write(ID,cnt,'P')
                wb.save('student.xls') 
        cv2.imshow("Face",img);
        if(cv2.waitKey(1)==ord('q')):
            break;
    cv2.destroyAllWindows()


def excel():#Writes the attendance in the specified Excel Sheet
    conn=sqlite3.connect("FaceBase.db")

    r=0
    #retrieve value of c from db
    cmd="SELECT c FROM Counter"
    cursor = conn.execute(cmd)
    c=cursor.fetchone()
    cnt=c[0]
    print(str(cnt))
     #reset value in counter to '2'
    cmd="UPDATE Counter SET c ="+str(2)    
    #cmd="UPDATE Counter SET c ="+str(cnt+1)
    conn.execute(cmd)
    conn.commit()
    conn.close()
    date1= date.today()
    rb= xlrd.open_workbook('student.xls')
    wb= copy(rb)
    
    w_sheet=wb.get_sheet(0)
   
    r+=1
    pre = present
   
    wb.save('student.xls')     
 
def display_plot():#Used to display the bar graph which consist of roll no. wise Attendance
           
        rb= xlrd.open_workbook('student.xls')
        worksheet = rb.sheet_by_index(0)
        rows= worksheet.nrows
        cols=worksheet.ncols
        global result_data
        result_data=[]
        #global row_data
        #row_data=[]
        for cur_r in range(1,rows,1):
            row_data=[]
            
            for cur_c in range(2,cols,1):
                data = worksheet.cell_value(cur_r,cur_c)
                row_data.append(data)
            result_data.append(row_data)
        pre_cnt=[]
        for d in result_data:
            cnt=0
            for a in d: 
                if a=='P':
                    cnt+=1
            pre_cnt.append(cnt)
        
        count=0
        for i in pre_cnt :
            hist_data.append(int((i/(cols-2))*100)) #calculating percentage
            count+=1
        
        
        #print(str(hist_data))
        a = np.asarray(hist_data)
        xtick=[]
        for i in range(1,rows):
            xtick.append(i)
        ytick=[]
        for i in range(10,110,10):
            ytick.append(i)

        plt.xlabel("Roll Number")
        plt.ylabel("Attendence(%)")
        plt.bar(rollno,pre_cnt)
        plt.show()
        
            
def detain():#Creates an Excel sheet of Detained students(Attendance<75%) with their attendance Percentage
     #this is imported from xlrd package
    rb= xlrd.open_workbook('student.xls')
    worksheet = rb.sheet_by_index(0)
    
    #this is imported from xlsxwriter package
    workbook = xlsxwriter.Workbook('demo.xlsx')
    worksheet1 = workbook.add_worksheet()

    #detained_students=[]
    cnt=0;
    c_cnt=1
    no_students=True
    for data in hist_data:
        cnt+=1
        if data<75:
            no_students=False
            #add name of student from respective column
            #detained_students[cnt]= worksheet.cell_value(cnt,1)
            col='A'+str(c_cnt)  #count of rows
            worksheet1.write(col,worksheet.cell_value(cnt,1)) #getting name of student and printing in detained student's list
            col='B'+str(c_cnt-1)
            worksheet1.write(col,str(data)+"%")
            c_cnt+=1
    if no_students:
        worksheet1.write('A1',"No student is detained!")
        
    workbook.close()   

    
def box():#This is the GUI which calls all of the above functions.. It is designed using Tkinter
    root = Tk()
    root.geometry('1000x700+270+50')
    root.title('face recognition for attendance system')
    canvas = Canvas(root , width=1000,height=800)
    canvas.place(x=0,y=0)
    
    line_hor = canvas.create_line(0,200,1000,200)
    
    line_ver =canvas.create_line(300,200,300,800)
    
    canvas.create_text(500,80,fill="darkblue",font="Times 40 italic bold",
                     text="Attendance System")
    
  
    #Dataset creater button
    cbutton1 = Button(root, text = "Create Dataset", command = datasetcreater, anchor = W)
    cbutton1.configure(width = 13,height=2, activebackground = "#33B5E5", relief = RAISED,font="Bradley 20 ",anchor=CENTER)
    #button1.place(x=)
    cbutton1_window = canvas.create_window(520, 280, anchor=NW, window=cbutton1)
    
    #trainer button
    tbutton1 = Button(root, text = "Train ", command = trainer, anchor = W)
    tbutton1.configure(width = 13,height=2, activebackground = "#33B5E5", relief = RAISED,font="Bradley 20 ",anchor=CENTER)
    #button1.place(x=)
    tbutton1_window = canvas.create_window(520, 400, anchor=NW, window=tbutton1)
        
    #detector button
    button1 = Button(root, text = "Detect ", command = detector, anchor = W)
    button1.configure(width = 13,height=2, activebackground = "#33B5E5", relief = RAISED,font="Bradley 20 ",anchor=CENTER)
    #button1.place(x=)
    button1_window = canvas.create_window(520, 520, anchor=NW, window=button1)
    
    #features
    canvas.create_text(70,240,fill="darkblue",font="Times 25 italic bold",
                     text="Features")
    
    
    #bar graph 
    bgbutton = Button(root, text = "Bar graph ", command = display_plot, anchor = W)
    bgbutton.configure(width = 15,height=2, activebackground = "#33B5E5", relief = RAISED,font="Bradley 13 ",anchor=CENTER)
    #button1.place(x=)
    button1_window = canvas.create_window(120, 280, anchor=NW, window=bgbutton)
    
    #detained students
    dsbutton = Button(root, text = "Detained Students", command = detain, anchor = W)
    dsbutton.configure(width = 15,height=2, activebackground = "#33B5E5", relief = RAISED,font="Bradley 13 ",anchor=CENTER)
    #button1.place(x=)
    button1_window = canvas.create_window(120, 380, anchor=NW, window=dsbutton)
    
    root.mainloop()


add()
box()

