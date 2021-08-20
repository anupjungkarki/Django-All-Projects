Hi! I'm Anup Karki and this is my Web Application for the Final Project of CS50 Web Programming with Python and JavaScript.

# OVERVIEW
EDUCAT SYSTEM  is an online content management system like UDEMY where the instructor can upload their courses contents and also they can Manage their
course Modules according to the need and demand. Those courses will be show to the users (i.e Students) and they can simply access those courses.Inorder
to access the available courses firstly student's should register their account and then login respectively and enroll their favourate courses.
Similary, for the instructor they should register their account inorder to Manage their modules and also to add new content.The main aim of this web
Application is to provide learning materials like Articles,Video Tutorials for Learners/Students.

# TECHNOLOGY USED
I use HTML/CSS/Bootstrap for fontend in the application templates , Python and Django technology is use for  backend development
in this application, and a little of Javascript is used to create a dropdown and interactive menu.This Web-Application is completely
Responsive in design which means Responsive  with all kind of devices such as Mobile,Ipad and different types of Monitors.

# LOGIN FOR  SUERUSER
  username:educat and
  password:Simkharka5

In this project I have create 2 additional Apps inside the main App such as Students and Courses respectively
## Students App
 Students App includes the template rendering for student interfaec and fetching data from the database for student to preview course list
 and access course after enrolled.Student registration form is created for registering the student credentials  so that later  on they can login
 through those credentials.In this section only the student enrolled course will be seen while clicking the my courses menu bar.
 ### FILES
    1.views.py
       * template_name: The path of the template to render for this view
       * form_class: The form for creating objects, which has to be a ModelForm.
       * success_url: The URL to redirect the user to when the form is successfully submitted. 
       
    - StudentRegistrationView: This is the view that allows students to register in our site.
       * form_valid:The form_valid() method is executed when valid form data has been posted
    
    -StudentEnrollCourseView: It handles students enrolling in courses.This view is inherits from the LoginRequiredMixin
     so that only  logged in users can access the view.
       * get_success_url:The get_success_url() method returns the URL the user will be redirected to if the form was successfully submitted.
     
    -StudentCourseListView: This is the view for students to list the courses they are enrolled in.This is also inherits from 
     LoginRequiredMixin so that only logged in users can access the view.
       *get_queryset():get_queryset() method for retrieving only the courses the user is enrolled in.
     
    -StudentCourseDetailView: This is the views to navigate through modules inside a course by students.
       * get_queryset: get_queryset() method to limit the base QuerySet to courses in which the user is enrolled.
       * get_context_data:get_context_data() method to set a course module in the context if the module_id URL parameter is given
       
    2.templates/
       * registration.html:To display registration form.
     
    -templates/students/course
      * list.html:This template displays the courses the user is enrolled in.
      * detail.html:This is the template for enrolled students to access a course contents.
 
    3.form.py
      * CourseEnrollForm: This form for students to enroll in courses.
      
    4.urls.py
      * Mapping between URL path expressions to this application functions and views
 
 

## Courses App
 Course app consist of rendering various template for login,registration,managing course modules ,viewing the list of courses for instructor and creating new
 course with various operation related to course management.Superuser who have rights to controll over the entire system once the user is register then
 superuser should give permission to user.If the register user is student then he/she only get permission to enrolled and access the course they are
 not able to modify the instructor course and also they won't get permisson to create the new course.But if the user want to become the instructor
 then superuser should give permission to particular user as a active instructor and he/she can create their own course and manage everything in their courses.
 
 ### FILES
    1.models.py: This file contain all the models of EDUCAT SYSTEM such as,
      *Subject
      *Course
      *Content
      *Modules and other inherit models.
      
    2.admin.py:This is use for registering the all models so that we can see the data in database.
    
    3.fields.py:It allows us to specify an order for objects.
    
    4. templates
        * base.html:This is the common interface structure where base template that will be extended by the rest of the templates
        
       - templates/registration/
        *login.html:Handles logging in the app.
        *logged_out.html:Handles logging out the app.
        
       - courses/manage/course/
        * list.html: Show the list the courses created by the current user.
        * form.html: It displays the form for the create and update course
        * delete.html: To delete the course.
        
        - courses/manage/module/
         * formset.html: To manage the hidden fields.
         * content_list.html: This is the template that displays all modules for a course and the contents for the selected modules.
         
        - courses/manage/content/
          * form.html : THis template for Adding new content.
          
        -courses/course/
          * list.html : This is the template for listing available courses.
          * detail.html : It will display the overview and details for a single course.
     5.static/ 
       -css/
         * style.css: It contain all the css code for this web application.
       - img/
         * It will contain all the saved image and video files.
       - js/
         * educat.js : It contain all the Ajax call methods.
         
     6.Bootstrap:Bootstrap  is used for making design responsive and CDN link of bootstrap 4.4.1 is used in this website.
         
        
     6.View.py
     -Common for all views
       * Model: The model used for QuerySets. Used by all views.
       * template_name: To specify the template path.
       
     - ManageCourseListView:This view is to retrieve only courses created by the current user.
        * fields: The fields of the model to build the model form of the CreateView and UpdateView views.
        * success_url: Used by CreateView and UpdateView to redirect the user after the form is successfully submitted.
        * get_queryset: get_queryset()method is for create, update, and delete views.
        
      -OwnerMixin and OwnerEditMixin mixins: We will use these mixins together with the ListView, CreateView, UpdateView, and DeleteView.
        * get_queryset: This method is used by the views to get the base QuerySet.
        * form_valid: To valid the form fields.
      
      -LoginRequiredMixin: Replicates the login_required decorator's functionality.
      
      -PermissionRequiredMixin: Grants access to the view to users that have a specific permission.
      
      -CourseModuleUpdateView: This view handles the formset to add, update, and delete modules for a specific course.
        * get_formset: This method is to avoid repeating the code.
        * dispatcher: This method is provided by the View class.
        * get: Executed for GET requests.
        * post: Executed for POST requests.
        
       - ContentCreateUpdateView : It will allow us to create and update contents of different models
       
       - ContentDeleteView: It retrieves the Content object with the given id, it deletes the related contents.
       
       -  ModuleContentListView: This view gets the Module object with the given id  that belongs to the current user and renders a template with the given module.
       
       - CourseListView: It will retrive all the list of course in home page.
       
       - CourseDetailView: It will display the detail of the course for user.

      
      8.urls.py
       * Mapping between URL path expressions to this application functions and views
    
      
     
 
# Features
Since this is a Web Application so, it provides few functions which performs the following tasks:
 ### 1.Authentication
 In this web app Django Authentication is used which is built in features and also
 Authentication process includes filling Registration form
 and then After this process you can easily log in.

### 2.Permission and role base access
 If the particular login user is student or reader he/she can only enroll and access the course but if the permission is granted as a instructor
 by superuser then he/she can create the new course and manage the course module according to them.

### 3.Responsive Design
 This web application is responsive in design so it is device friendly .It is reponsive in all types of mobile,ipad and other monitors having different
 resolution.

### 4.Dynamic Content Management
 Courses content can be dynamically manage by the instructor itself all the course content are dynamically created in this Web Application.
 
### 5.Easy to get access on Courses:
 Students/Learner

## why to believe my project?
In this particular project I have implement the advance concept of django to complete the entire project such as Model Inheritance,Creating Custom model fields,
class based views and mixins, manage group and permisssions and also formsets.This project is completely based on class based views inspite of using fuctional views
I tried to compile some of the activities done during the course in this last project and make them as tedious as I can, that's why I think this web application is more
complex than the other project that I did during the course.
