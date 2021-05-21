from flask import Flask, render_template, session, request, url_for, redirect
import requests
from grocerySort import sort_recipe, combine_groceries

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'


@app.route('/', methods=['GET', 'POST'])
def index():
    # Obtain current location of user using Nick Alvey's microservice

    loc_response = requests.get("https://alveyn-cs361-getlocation.herokuapp.com/getlocation")
    if loc_response.status_code == 200:
        session['location'] = loc_response.json()
        session['location_printout'] = session['location']['City'] + ", " + session['location']['Region']
    else:
        session['location_printout'] = "Location ERROR"

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
            return render_template('test.html', ingredients=session['ingredients'], location=session['location_printout'])

        else:
            return render_template('test.html', warning="Recipe Not Found")

    if request.method == 'GET':
        return render_template('test.html', location=session['location_printout'])


@app.route('/reset')
def reset():
    # clear ingredient and groceries session variables
    session.pop('ingredients', None)
    session.pop('groceries', None)
    return render_template('test.html')


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
        return render_template('test.html', groceries=session['groceries'], location=session['location_printout'])
    else:
        return render_template('test.html')


@app.route('/view-list')
def view_list():
    if session.get('groceries'):
        return render_template('viewlist.html', groceries=session['groceries'], location=session['location_printout'])
    else:
        return render_template('test.html')

@app.route('/delete-ingredient/<item>')
def delete_ingredient(item):
    for i in range(len(session['ingredients'])):
        if session['ingredients'][i]["description"] == item:
            session['ingredients'].pop(i)
            session.modified = True
            return render_template('test.html', ingredients=session['ingredients'], location=session['location_printout'])


@app.route('/delete-grocery/<item>')
def delete_grocery(item):
    for i in range(len(session['groceries'])):
        if session['groceries'][i]["description"] == item:
            session['groceries'].pop(i)
            session.modified = True
            return render_template('test.html', ingredients=session['groceries'], location=session['location_printout'])

@app.route('/find-stores')
def find_stores():
    url = "https://www.google.com/maps/search/groceries/@"+session['location']['latitude']+\
          ","+session['location']['longitude']+",12z/data=!3m1!4b1"
    return redirect(url, code=200)


if __name__ == "__main__":
    app.run(debug=True)
