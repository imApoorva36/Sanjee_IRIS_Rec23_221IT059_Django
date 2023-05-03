# IRIS_Rec23_221IT059_Django

<br>

#### This is a project done for the recruitment of IRIS Web team. Here is the deatiled report of this project.
<br>

### Installation instructions to set up the project from scratch :
1. To run this project you need to install ***Django*** as this project is made by django framework.
   In the command promt or terminal give the command ***pip install django***
2. After the installation has completed, you can verify your Django installation by executing ***django-admin --version*** in the command prompt or terminal.

### Steps to run the project :
1. Once you install django then either you have to clone this repository or you need to fork it. If you want to clone this repository then run the command ***git clone https://github.com/sanjeevholla26/IRIS_Rec23_221IT059_Django.git*** in the terminal or command promt.
2. After cloning the repository change the directory to the project directory. For that give the command ***cd IRIS_Rec23_221IT059_Django***.
3. In order to apply all the migrations to the database run the following two commands
<br>

    python3 manage.py makemigrations
   
  <br>
  
    python3 manage.py migrate
   
   <br>
   
   [***NOTE*** : If the version of python in your pc is 3 then only give python3 int the command or else just give python.]
   <br>
   
4. In order to start the project run the command 
<br>

    python3 manage.py runserver
