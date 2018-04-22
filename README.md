# Face-Recognition-using-openCV

This project is about face recognition for autonomous attendance system.

# Before starting:
We have used android smartphone's camera as input to the program. For this you have to install 'IP webcam' app from playstore (https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en).

# Step 1:
The final.py file asks for ID and name to enter. After that it starts to detect face and assigns the ID to that particular face (this is dataset creater hence only one face should be exposed before camera) and saves these .jpg file in a seperate folder named dataSet (folder should be created prior running the script) in the same directory.

# Step 2:
The trainer.py file trains the model on the present data and creates trainingData.yml file in recognizer folder (folder should be created prior running the script). You will see IDs of dataset which are being trained in the consol of your python IDE.

# Step 3:
Now what you have to do is make changes to student.xls file as per your requirement.As the dataset has been trained you can now test it by running detector+excel.py file. This file will recognize the faces which has been trained and write attendance to the student.xls file of those IDs which have been recognized by the model.

# Step 4:
Now that IDs have been written to student.xls file its time to play with this data. For displaying a histogram of attendance of all students just enter option '1' and see the magic!

# Note:
This model has been tested on windows 10, python 3.6 and opencv 3.4 and has efficiency of about 67%.
