# What is this application? 

This is a web application created using Flask, a Python microframework for creating streamlined and simple web 
applications. It uses a local SQLite database to create and read data such as job applications, accounts, roles, and so
on. It implements basic security to verify the current user's (if any) permissions, requiring a password authenticated 
login page to sign in. 

# Account Permissions 

There are two types of accounts, Users and Admins. Admins have full permissions to access any page on the site. Users
may only access the submit application page. Anyone can sign up an account to submit an application, but only an admin 
may add another admin. Before being stored, passwords are encrypted using the BCrypt library.

# Modules

There are three main modules in this application, emailing.py, main.py, and repository.py. The first, emailing.py, 
allows for the sending of emails to any job applicants, provided the correct app password is provided through an 
environment variable on the running machine. The second, repository.py, provides functions which handle all the 
operations performed on the applications main SQLite database. 

The final module, main.py, provides the entirety of the applications routing and logic. It is the module from which the 
rest of the application is run. 

# Static Files 

Static files, such as styles/styles.css and scripts/add_user.js, are contained in the static folder of the application. 
These files are responsible for the style rules used throughout the site, as well as the client side JavaScript used in 
the sign-up page for adding roles to a user. 

# Template Files 

The template files used to generate HTML pages are stored and access by Flask in the templates folder. These templates 
use the Jinja templating engine to create dynamic pages in response to the data passed into them. The base_template.html
file is used as the template for all other pages, with each additional page customizing specific blocks in the 
base_template.html file.

# Persistence

Data is stored in the local instance/data.db file, which is an SQLite database. The schema for this database is provided
in the instance/schema.sql file. 

# Requirements 

In addition to a modern Python installation, this application requires a number of packages to be installed. To install 
these packages, it is recommended to create a new virtual environment using python -m venv env. To use this virtual 
environment on Windows, run env/Scripts/activate.bat on the command line, or on Linux, run source env/bin/activate. 

To install the neccessary packages into this virtual environment, run pip install -m requirements.txt on the command 
line or terminal.

# Default Users 

The two main users by default are admin and root. The password for each is identical to the username. Admin provides 
admin access to the entire site, and root provides user access to the entire site. Additional users may be added through 
the add_users page.

# Disclaimer 
The application is intended as a mockup for programming demonstration only, and should not be used as the basis of a real-world application for
a similar purpose. 