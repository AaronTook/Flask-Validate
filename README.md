# Flask-Validate
A Web server and templates for a sample application demonstrating one method of connecting an email account or cell phone number to an account with Python and the Flask web framework.

This project is a Python and Flask system for validating possession of a email address or cell phone number. Designed to accept any email address and most major United States cell phone providers, this system will send an email with a validation code to the user, which when entered within five minutes of the send time, will pass. An incorrect or expired validation code will fail.

The purpose of this project is to provide a base of source code for similar applications or implementation of similar systems with Flask for web server development. The frontend is simply a basic sample that can be used to test the backend of this project.

--------------------------------
Project Requirements:
 1.  Must have Flask installed (https://flask.palletsprojects.com/)
 2.  Must have Flask-Mail installed (https://flask-mail.readthedocs.io/)
 3.  Must have a GMail account. This must be updated in the app.py file at line 47.
 4.  Must have a Google app password to allow Flask-Mail to safely log into your gmail account. Find out how to create one at https://support.google.com/accounts/answer/185833?hl=en. This must be updated in the app.py file at line 48.


Run the program file from the command line, your IDE, or any other usual method.

After program starts, open your browser to the URL displayed in the terminal launch of the application (usually http://127.0.0.1:5000/).
