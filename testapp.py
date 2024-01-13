from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route('/tester', methods=['POST'])
def tester():
    return redirect('https://tonyarkaysia.github.io/isl-cybergateway')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))