from flask import Flask, render_template, request
import requests

app = Flask(__name__)

ingredients = ["tomato", "chicken", "beer"]

@app.route('/')
def index():
    print("went home")
    return render_template('home.html')

@app.route('/test')
def index_test():
    print("went to test")
    return render_template('home.html', ingredients=ingredients)


if __name__ == "__main__":
    app.run(debug=True, port=5000)