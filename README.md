# IRIS_Rec23_221IT059_Django

<br>

#### This is a project done for the recruitment of IRIS Web team. I have choosen the 1st task i.e Career Development Module. Here is the detailed report of this project.
<br>

### Video Recordings of the project.
https://drive.google.com/drive/folders/1SzOOmXtxMVB43iVEcOy6--zfimJMzExF?usp=sharing
In the above google drive there are 8 videos :
1. Video on the Overview of the whole application.
2. User registration video.
3. How different access can be given to different users by Admin.
4. How Admins can see all the applications.
5. How Admins can add company and posts.
6. How the poc of a company can edit the details of that company.
7. ***Security of the application from backend***
8. How a student can apply for a company. 
<br>

### Installation instructions to set up the project from scratch :
1. To run this project you need to install ***Django*** as this project is made by django framework.
   In the command promt or terminal give the following command 
   <br>
   
         pip install django
      
   <br>
2. After the installation has completed, you can verify your Django installation by executing the following command in the    command prompt or terminal.
   <br>
   
         django-admin --version
      
   <br>


### Steps to run the project :
1. Once you install django then either you have to clone this repository or you need to fork it. If you want to clone this repository then run the command following command in the terminal or command promt
   <br>

         git clone https://github.com/sanjeevholla26/IRIS_Rec23_221IT059_Django.git

   <br>

2. After cloning the repository change the directory to the project directory. For that give the command 
   <br>
   
         cd IRIS_Rec23_221IT059_Django/irisrec23
      
   <br>
   
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
    
   <br>
5. After you run the command then go to any web browser and go to the url ***"http://127.0.0.1:8000/"*** to see the website. 

<br>
   
   ### Features Implemented in the project 
   

1. ***User Registration and login*** : In this web application only the authorized users can use it. So a user need to register himself to use this account. If he had an account already then he wants to login with that account.
2. ***Using sessions*** : Sessions have been used in order to keep the user loged in to the application. So there is no need for the user to again and again login to the website each times he visit it.
3. ***Making Profile*** : Once a user is registered then he has to build his profile by giving all the necessary details like his roll number, branch, cgpa etc.
4. ***Adding Resume*** : In the profile user can add his resume which will be automatically attached with the application which the user writes for a post.
5. ***There are 3 types of users*** : A user registered into this application will be registered as a normal student. There is a provision for the Superuser to give admin access to any user and admins and superuser can make any user as POC so that he can be assaigned with a company.
6. ***Searching for a user with his roll number*** : While giving some special access to a user, Its difficult to search the required user out of so many users present. In order to solve this issue I gave a provision for searching a user with his roll number.
7. ***Adding a company*** : Admins have the access to add a company which will do its recruitment.
8. ***Adding posts for the company*** : Once a company is added then there is a provision for adding different posts for the company. Any number of posts can be added for a company. Each post will be open for some particular branches and for each branch there will be a seperate cgpa cutoff.
9. ***Giving the timeline for the post*** : Each post will be having its own time line. If the deadline to apply for the company is over then that company will be deactivated automatically.
10. ***Editing the posts and company*** : Only admins and POC of that company can edit that company and the posts of that company.
11. ***viewing the list of eligible companies*** : Once a user is registered he will be able to see all the list of posts that he is eligible to apply for. i.e that post should be open for the branch in which user is in and the user should pass the cgpa cutoff for his branch.
12. ***Applying for a post of a company*** : A user can apply for a post of a company for which he is eligible for. His details like fullname, branch, roll number, ***resume***, cgpa, will be taken from his profile while writing the application. 
13. ***Seeing the list of applied posts*** : A user can see the list of applied posts and can view the application written by him for that post.
<br>

### Planned features :
<br>

1. I want to improve the front end of the website.
2. Add the feature of giving a provision for the users to edit their applications before the deadline of the company.(wasn not able to do beacause of the shortage of time).
3. Password change provision.
4. Users can add more resume's and can select any one of them while applying for a perticular post.
<br>

### References used :
<br>

1. Google is the main source of reference.
2. For frontend I have used ***Bootstrap***.
