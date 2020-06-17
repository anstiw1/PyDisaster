# Import libraries
import master_function
import os
import numpy as np
from flask import Flask, request, render_template, jsonify, Response, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


# Initialize the flask app
app = Flask('pydisaster')

# Initialize the first route (home page)
@app.route('/')

# Define what happens on that page: return a string
def home():
    return 'welcome to PyDisaster'


# Initialize the input page: from an html file that we'll display
@app.route('/pydisaster')

# Define what happens: show the html input form
def form():
    return render_template('form.html')

# Initialize the results page: what happens when the user inputs data
@app.route('/submit')

# Define what happens: load form data and return recommendations
def form_submit():
    user_input = request.args
    # Upload photo and take in comment/response.
    response = str(user_input['UserInput'])

    get_exif = master_function.get_exif_data(response)
    get_gps = master_function.map_search(response)

    # Show html output on page
    return render_template('results.html', rec1=get_exif, rec2=get_gps) # Corresponds to template docs

# Run when python script is called (debug=True)
if __name__ == '__main__':
    app.run(debug=True)
