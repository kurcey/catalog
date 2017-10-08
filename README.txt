# This project is for Kurt Wanliss to be used in the Udacity FullStack Web course.

#Purpose of this project:

Develop an application that provides a list of items within a variety of 
categories as well as provide a user registration and authentication 
system. Registered users will have the ability to post, edit and delete 
their own items.

#Requirements of this project:
* 1. The project implements a JSON endpoint that serves the same information as displayed in the HTML endpoints for an arbitrary item in the catalog. 
* 2. Website reads category and item information from a database.
* 3. Website includes a form allowing users to add new items and correctly processes submitted forms.
* 4. Website does include a form to edit/update a current record in the database table and correctly processes submitted forms.
* 5. Website does include a function to delete a current record.
* 6. Create, delete and update operations do consider authorization status prior to execution.
* 7. Page implements a third-party authentication & authorization service (like Google Accounts or Mozilla Persona) instead of implementing its own authentication & authorization spec.
* 8. Make sure there is a 'Login' and 'Logout' button/link in the project. The aesthetics of this button/link is up to the discretion of the student.
* 9. Code is ready for personal review and neatly formatted and compliant with the Python PEP 8 style guide.
* 10. Comments are present and effectively explain longer code procedures.
* 11. README file includes details of all the steps required to successfully run the application

## Instructions and pre-requisite to run the program:

*    Load Udacity's vagrant virtual machine [here:](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc    51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
(this has the psql database running in the background)

*    Downlad the data files [here:](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

* On the running vagrant virtual machine in the folder that has the above downloaded file run the following from your psql command line (this will extrac    t and instal the three news tables):
    * psql -d news -f newsdata.sql

* Switch to the directory that this README.md file is located

* Run this code by typeing the following python 3 command:
     * python3 application.py

* Bask in the beauty of the output!!!


#This Project has the following files and folders:

Catelog Directory
* 1 application.py
* 2 categories.db
* 3 client_secreats.json
* 4 database_setup.py
* 5 database_setup.pyc
* 6 lotsofCategory.py
* 7 README.txt
* 8 static (directory)
* 9 templates (directory)

static Directory
* 1 styles.css

templates Directory
* 1 categoryShow.html
* 2 createItem.html
* 3 deleteCategory.html
* 4 descriptionShow.html
* 5 editItem.html
* 6 index.html
* 7 login.html
* 8 mainTemplate.html

Functions of each file
##application.py

    This file is the main RESTful web application using the Python 
framework Flask along with implementing third-party OAuth 
authentication. You will then learn when to properly use the various 
HTTP methods available to you and how these methods relate to CRUD 
(create, read, update and delete) operations.

##categories.db

    This is the database that is created when the python program 
lotsofCategory.py is exicuted initally to create an initial database
of Categories and items.

##client_secreats.json

    This is the json file that contains the google login in secreats
that enable the project to login the end user.

##database_setup.py

    This is the python file that is used to give the parameters that
we requre for the two psql tables Categories and Items.

##database_setup.pyc
    
    This is the file that is created as a result of runnin the python
file database_setup.py.

##lotsofCategory.py

    This file is used to create the inital database of items that 
prepoulate the database.

##README.txt

    This readme file.

##styles.css

    This contains all the CSS cascadeing style sheets for the project.

##categoryShow.html

    This is the html template that is used to show all the categories 
to the person viewing the webpage if logged in or not logged in.

##createItem.html

    This is the html template that is used to create new items
in the database only logged in users has this abillity.

##deleteCategory.html
   This is the html template that is used to delete new items
in the database only logged in users has this abillity.

##descriptionShow.html
   This is the html template that is used to show the description
of items in the database both logged in and non logged in users 
has the abillity to see this screen but logged in users will have
the added ablility to select links to edit or delete the description.

##editItem.html
   This is the html template that is used to edit items
in the database only logged in users has this abillity.

##index.html
   This is the main html template that is used to view most recent
items in the database and all categories only both logged in and
non logged in users has this abillity but looged in users has the 
added abliltiy to add additional items by the add link.

##login.html
   This is the html template that is used to log users in via there
google account.

##mainTemplate.html
   This is the main html template that is used to as a primary layout
for all the other templates.
