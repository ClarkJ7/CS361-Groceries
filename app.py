from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    print("went home")
    return render_template('home.html')

@app.route('/test')
def index_test():
    print("went to test")
    return render_template('test.html')

@app.route('/test/search')
def api_call():
    arg1 = request.args['arg1']

    return 'Link is: ' + arg1



if __name__ == "__main__":
    app.run(debug=True, port=5000)