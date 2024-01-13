from flask import Flask, request, redirect, render_template



app = Flask(__name__)

@app.route('/')
def tester():
    return redirect('https://tonyarkaysia.github.io/isl-cybergateway')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)