"""
	Author: AaronTook (https://github.com/AaronTook/)
	Last modified : 1/20/2023
	Project name: Flask-Validate
	File name: app.py
	File description: This file contains the source code for the website backend.
"""

""" Import the required modules. """
import time, hashlib, math, secrets # Python Standard Library imports. 
from markupsafe import escape # Markupsafe imports.
from flask import Flask, render_template, request, session # Flask imports.
from flask_mail import Mail, Message # Flask-Mail imports.

def secrets_rand_range(start, stop):
	""" Generate a truly random (as opposed to the random module's pseudo-random generation) number between start and stop (inclusive). """
	return (secrets.choice(range((stop-start)+1))+start)
def get_time_in_minutes():
	""" Get the current time since the UNIX in minutes. """
	current_seconds = time.time()
	current_mins = math.ceil(current_seconds/60)
	return current_mins
def hash_string(to_hash):
	""" Create a hash of the passed string using the SHA 224 cryptographic hashing algorithm. """
	return (hashlib.sha224(str(to_hash).encode()).hexdigest())
def generate_access_code(num_ints):
	""" Generate a new access code. """
	access_code = ""
	for i in range(num_ints):
		access_code += str(secrets_rand_range(0,9))
	return access_code
def check_code_and_time_against_hash(code, timestamp, complete_hash):
	for i in range(6): # Ideally would be only 5, but to prevent errors upon quick responses, a higher time is necessary.
		"""print(timestamp+i, hash_string(timestamp + i -1))"""
		if (hash_string(code) + hash_string(timestamp + i ) == complete_hash):
			return True
	return False

""" Create the app. """
app = Flask(__name__) # Create the Flask app object.
app.config["DEBUG"] = False
app.secret_key = "YOUR SECRET KEY HERE" # Generate one with secrets.token_hex(64) and replace here.

""" Flask-mail config settings. """
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'YOUR EMAIL ADDRESS HERE'
app.config['MAIL_PASSWORD'] = 'YOUR GOOGLE APP PASSWORD' # Create a Google app password to allow flask-mail to safely log into your gmail account. Find out how at https://support.google.com/accounts/answer/185833?hl=en
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = False
mail = Mail(app) # Create the Mail object.

sms_email_gateways = { # List the SMS email gateways for various major cell phone service providers.
	"AT&T": "@txt.att.net",
	"Boost Mobile": "@myboostmobile.com",
	"Cricket": "@sms.mycricket.com",
	"Metro": "@mymetropcs.com",
	"Sprint": "@messaging.sprintpcs.com",
	"T-Mobile": "@tmomail.net",
	"U.S. Cellular": "@email.uscc.net",
	"Verizon": "@vtext.com",
	"Virgin Mobile": "@vmobl.com",
	"Spectrum":"@vtext.com"
}

""" The page view. This is not a production-ready web page, but is simply to be an example of how to make a functional email or phone number verification system. """
@app.route("/", methods=["GET","POST"])
def connect_method():
	if request.method=='POST': # The action is a form submission.
		try: # Submitted an email address.
			emailAddress = request.form["emailAddress"] # Retrieve the form input.
			new_code = generate_access_code(5) # Generate a 5-digit access code.
			new_code_hash = hash_string(new_code) # Hash the code.
			expiration_time_in_minutes = get_time_in_minutes() + 5 # Get the time at which 5 minutes is up.
			new_code_timestamp_hash = hash_string(expiration_time_in_minutes) # Hash the time.
			message = Message("Your new access code", sender= 'flaskdoggo@gmail.com', recipients=[str(emailAddress)]) # Create the email message with the validation code.
			message.body = f"Here is your new code: \n {new_code}" 
			mail.send(message) # Send the email message.
			complete_hash = new_code_hash + new_code_timestamp_hash # Combine the code and time hashes.
			session['complete_hash'] = complete_hash # Save the combined hash.
		except: # Not an email address.
			try: # Submitted a phone number and cell phone service provider.
				phoneNumber = request.form["cellPhone"] # Retrieve the form inputs.
				phoneProvider = request.form["myProvider"]
				try:
					smsGateway = sms_email_gateways[phoneProvider] # Get the SMS email gateway
				except: # The provider is not in the dictionary of SMS email gateways.
					return render_template("message.html", message = "Unsupported cell phone provider!")
				emailAddress = phoneNumber + smsGateway # Get the complete email address for the phone number. 
				new_code = generate_access_code(5) # Generate a 5-digit access code.
				new_code_hash = hash_string(new_code) # Hash the code.
				expiration_time_in_minutes = get_time_in_minutes() + 5 # Get the time at which 5 minutes is up.
				new_code_timestamp_hash = hash_string(expiration_time_in_minutes) # Hash the time.
				message = Message("Your new access code", sender= 'flaskdoggo@gmail.com', recipients=[str(emailAddress)]) # Create the email message with the validation code.
				message.body = f"Here is your new code: \n {new_code}" 
				mail.send(message) # Send the email message.
				complete_hash = new_code_hash + new_code_timestamp_hash # Combine the code and time hashes.
				session['complete_hash'] = complete_hash # Save the combined hash.
			except: # Not a cell phone number and cell phone service provider.
				try: # Submitted a validation code.
					complete_hash = session['complete_hash'] # Get the hash to match the required input.
					access_code = request.form["validationCode"] # Retrieve the input.
					current_time_in_minutes = get_time_in_minutes()
					if check_code_and_time_against_hash(access_code, current_time_in_minutes, complete_hash): # The code is on time and is correct.
						return render_template("message.html", message = "Success")
					else: # The code is expired or invalid.
						return render_template("message.html", message = "Invalid or timed out key")
				except KeyError: # No validation code has been sent.
					return render_template("message.html", message = "Invalid connection attempt")
				except: # Unexpected error.
					return render_template("message.html", message = "Connection error")
				session['complete_hash'] = None # Reset the connection hash.
		return render_template("confirm.html") # Display the validation code page to the user.
	else:
		return render_template("home.html") #  Display the main page to the user.

if __name__ == "__main__":
	app.run() # Run the web application.
