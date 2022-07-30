# DevClub Assignment 5

## Heroku App
See  deployment for HoloLMS [here](https://hololms.herokuapp.com/).

### Features Implemented:
 - Users - Admin, Student, Instructor, Course. Admin, Student and Instructor are subclasses of the Django Custom User Model, edited as Member class.
 - Grades - Assignment model, which can be an ordinary Assignment or a Quiz
 - Documents - Docs model, which stores a file (won't work in Heroku because of `/media`)
 - Quizzes - Question, QuestionBank, Quiz models are implemented here
 - Messages - Messages, Forum Models are implemented here. Each message is a conversation, as it is a Node for a LinkedList. Forums are simply collections of Messages. All Users' models have a forum (for personal messaging, or in the case of a course, a course forum).

### Demostration:
1. We begin at the login page. In case you don't have an account, you can register for one. However, your year / semester / department will only be updated by the administrator. Only an instructor can add you to a course
![image](https://user-images.githubusercontent.com/15856849/181866869-06920df0-b63f-43c6-b22e-6c43e617912d.png)
2. The register page - 
![image](https://user-images.githubusercontent.com/15856849/181866901-6ead0e53-28bf-419c-bfb5-30fa7b57b86b.png)
3. Users can edit their profiles on the My Profile page. They can view and message other users through their profiles.
![image](https://user-images.githubusercontent.com/15856849/181867288-33327d63-30c8-44d6-b838-4b7cbaa4878b.png)
![image](https://user-images.githubusercontent.com/15856849/181867488-b2608e48-db99-4037-bcad-9856fbd3078b.png)
4. View your current grades on the Grades page
![image](https://user-images.githubusercontent.com/15856849/181867513-255a50d7-2262-461c-adf9-57bd39c9651e.png)
5. View and visit all your registered courses on the Courses tab
![image](https://user-images.githubusercontent.com/15856849/181867571-5af772e7-6a73-4e2e-9ad9-66f0c5229761.png)
6. Post, view announcements on the Course Forum. See all uploaded documents by the instructor, and view Assignments / Quizzes [This is how an instructor sees the page]
![image](https://user-images.githubusercontent.com/15856849/181867625-9bc842e6-848c-4b86-8327-f20519800c45.png)
![image](https://user-images.githubusercontent.com/15856849/181867763-0c166359-1e39-4626-8157-41d2117cfcc8.png)
![image](https://user-images.githubusercontent.com/15856849/181870172-4ee7bb45-4b91-43de-91bc-b2a7d496a38b.png)
7. Send and view messages via the Messages tab
![image](https://user-images.githubusercontent.com/15856849/181870305-37a8605f-425a-4370-91e5-c21229d2c228.png)
8. Only 1 Quiz can be taken at a time, the timer also maintains its value even after page reload / change. Assignments and Quiz submission will close after submitting / the end date.

You have learnt about backend engineering with Django in our session. Now use it to create a web application by yourself!
## DevClub LMS (Learning Management System)
You must have used **Moodle** in your courses, where both instructors and students login, and for each course, the instructor uses the platform to share resources, send announcements, release grades, conduct quizzes and what not!

Your task is to create your own such a learning management system using Django, where you can add functionalities as per your own creativity!

### We would recommend you to have these apps inside the project: 
- Users (to store auth logic, and models for `Instructor`, `Student`, `Course`, `Admin`)
- Grades (to store logic for sharing grades for any assessment, and models for let's say a class `Grade`)
- Documents (for Instructor to upload `Docs` like lecture notes for the course)
- Quizzes (this can have models for a `QuestionBank` containing `Question`'s which form a `Quiz`)
- Communication (to work on features like Course-wide `Announcements`, `Reply`ing in threads to announcements, sending personal `Messages`)

Try to implement as many features as you can, but make sure to plan the structure of the project and database schemas well!

### Bonus:
- Deploy on Heroku
- Create documentation for any RESTful APIs created with documenter on postman
- Markdown support for Communication
- Email: For registration, password reset, notifications, instructor custom message
- Bulk upload from CSV for grades, quizzes
- Generating PDF: Print digitally signed transcript
- Add security features for the quizzes

## Submission Instructions
- **FORK** this repository, by clicking the "Fork" button on top right
- `clone` the forked repo into your machine, and `cd` into the Repo Folder such that you are in same directory level as `manage.py`
- If on macOS, run `python3 -m venv env`, otherwise `python -m venv env`
- Now activate the virtual environment by `source env/bin/activate`
- See if the environment is correctly set by running `pip list`, it should be mostly empty
- Install dependencies with `pip install -r requirements.txt`
- We have already started a dummy project called `DevClubLMS` for you
- Now, you can use `python manage.py runserver` to start the dev server or `python manage.py startapp <appname>` to create a new app inside this project
- After completing the assignment, append instructions to run your project, along with explanation of features etc in this README
- It would be nice if you can host it on Heroku and also give a documentation of each endpoint through postman
- Finally submit with your details in the [Google Form](https://forms.gle/XSidrfbrsEZuDYfy6)
- You do NOT need to make any pull requests to this repo

# Resources
- [Slides used in the session](https://docs.google.com/presentation/d/e/2PACX-1vQbtDDGQonkIoGu68VrINL2s3sQcfiH5XVnk-iU26nk16DFBGsDabichsqhdtBvowPvpxaIbFLAV2h3/pub?slide=id.p)
- Introduction to Python and Django by [Programming With Mosh](https://youtu.be/_uQrJ0TkZlc)
- Detailed Django Tutorials by [Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
- [Mozilla's Tutorials](https://developer.mozilla.org/en-US/docs/Learn/Server-side) on Server Side Programming with Django
- [Django Official Docs](https://www.djangoproject.com/start/)
- [Talk](https://youtu.be/lx5WQjXLlq8) on how Instagram uses Django at production, and also [*the time when Justin Beiber almost crashed Instagram!*](https://youtu.be/lx5WQjXLlq8?t=715)
- Advice on Backend Engineering by [Hussein Nasser](https://www.youtube.com/c/HusseinNasser-software-engineering)
- Guide for Deploying Python apps on [Heroku](https://devcenter.heroku.com/categories/python-support)
- Guide for [Postman Documenter](https://learning.postman.com/docs/publishing-your-api/documenting-your-api/)
