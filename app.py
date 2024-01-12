from flask import Flask, request, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'Gin632Jo'  # Set a secret key for security purposes
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def is_logged_in():
    return session.get('logged_in')

@app.route('https://tonyarkaysia.github.io/isl-signup', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "prachya" and password == "californialove":  # Replace with real validation
            session['logged_in'] = True
            return redirect(url_for('protected_page'))
        else:
            return "Login Failed"
    return "Login Page"  # Render a login template here

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return "Logged out"

@app.route('https://tonyarkaysia.github.io//isl-profile')
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





