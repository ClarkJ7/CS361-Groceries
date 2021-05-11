from flask import Flask, render_template, session, request
import requests
from grocerySort import sort_recipe, combine_groceries

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # retrieve dish name from searchbar
        link = request.form['wikiURL']
        # format dish name for wikipedia link
        link = link.title()
        link = link.replace(" ", "_")
        full_link = 'https://cs361-ul-scraper.herokuapp.com/' + link
        # send to ulScraper API
        response = requests.get(full_link)
        if response.status_code == 200:
            # store ingredients in session variable
            session['ingredients'] = sort_recipe(response.json())
            return render_template('home.html', ingredients=session['ingredients'])
        else:
            return render_template('home.html', warning="Recipe Not Found")
    if request.method == 'GET':
        return render_template('home.html')


@app.route('/reset')
def reset():
    # clear ingredient and groceries session variables
    session.pop('ingredients', None)
    session.pop('groceries', None)
    return render_template('home.html')


@app.route('/add-recipe', methods=['GET', 'POST'])
def add_recipe():
    # check if any ingredients are currently shown
    if session.get('ingredients'):
        # check if any groceries are currently shown
        if session.get('groceries'):
            # add ingredients to current groceries
            session['groceries'] = combine_groceries(session['ingredients'], session['groceries'])
        else:
            session['groceries'] = session['ingredients']
        session.pop('ingredients', None)
        return render_template('home.html', groceries=session['groceries'])
    else:
        return render_template('home.html')


@app.route('/view-list')
def view_list():
    return render_template('viewlist.html', groceries=session['groceries'])


if __name__ == "__main__":
    app.run(debug=True)
