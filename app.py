from flask import Flask, request, session, redirect, url_for
from flask_session import Session
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


app.secret_key = 'Gin632Jo'  # Set a secret key for security purposes
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def is_logged_in():
    return session.get('logged_in')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # This block of code executes when a POST request is made (typically when submitting a form)
        username = request.form['username']
        password = request.form['password']

        if username == "prachya" and password == "californialove":
            # If the provided username and password match, set a session variable to indicate a successful login
            session['logged_in'] = True
            # Redirect to an external URL (in this case, a personal profile page)
            return redirect('https://tonyarkaysia.github.io/isl-profile')
        else:
            # If the provided credentials are incorrect, redirect to a retry login page
            return redirect('https://tonyarkaysia.github.io/isl-retry-login')
    
    # This part of the code executes for a GET request or when the form is initially loaded
    # It redirects to a retry login page since no login attempt has been made yet
    return redirect('https://tonyarkaysia.github.io/isl-retry-login') # Render a login template here

@app.route('/add-api-key', methods=['POST'])
def add_api_key():
    apikey = request.form['apikey']
    if apikey == "w-f_JoRyjxgqJKasc6glAQNFqFJIUGE7HwF_Lo0fQEA":  # Replace with real validation
        return redirect('https://tonyarkaysia.github.io/isl-cybergateway')
    else:
        return redirect('https://tonyarkaysia.github.io/isl-retry-login')


if __name__ == '__main__':
    app.run(debug=True)

