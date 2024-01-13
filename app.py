from flask import Flask, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # This block of code executes when a POST request is made (typically when submitting a form)
        username = request.form['username']
        password = request.form['password']

        if username == "prachya" and password == "californialove":
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

