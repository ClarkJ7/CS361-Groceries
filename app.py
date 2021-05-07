from flask import Flask, render_template, session, request
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("POST METHOD")
        link = request.form['wikiURL']
        full_link = 'https://cs361-ul-scraper.herokuapp.com/' + link
        response = requests.get(full_link)
        session['ingredients'] = response.json()
        return render_template('home.html', ingredients=session['ingredients'])
    if request.method == 'GET':
        print("GET METHOD")
        return render_template('home.html')


@app.route('/reset')
def reset():
    session.pop('ingredients', None)
    session.pop('groceries', None)
    return render_template('home.html')


@app.route('/addrecipe', methods=['GET', 'POST'])
def add_recipe():
    if session.get('ingredients'):
        if session.get('groceries'):
            session['groceries'].extend(session['ingredients'])
        else:
            session['groceries'] = session['ingredients']
        session.pop('ingredients', None)
        return render_template('home.html', groceries=session['groceries'])
    else:
        return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)