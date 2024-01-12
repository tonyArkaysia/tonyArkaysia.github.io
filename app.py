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
        username = request.form['username']
        password = request.form['password']
        if username == "prachya" and password == "californialove":  # Replace with real validation
            session['logged_in'] = True
            # Redirect to an external URL
            return redirect('https://tonyarkaysia.github.io/isl-profile')
        else:
            return "Login Failed"
    return redirect('https://tonyarkaysia.github.io/hq') # Render a login template here


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # Redirect to a specific page after logging out
    return redirect('https://tonyarkaysia.github.io/hq')


@app.route('/protected')
def protected_page():
    if not is_logged_in():
        return redirect(url_for('login'))
    return "This is a protected page."

@app.route('/add-api-key', methods=['POST'])
def add_api_key():
    apikey = request.form['apikey']
    if apikey == "w-f_JoRyjxgqJKasc6glAQNFqFJIUGE7HwF_Lo0fQEA":  # Replace with real validation
        return "API Key is valid"
    else:
        return "Invalid API Key", 403

if __name__ == '__main__':
    app.run(debug=True)





