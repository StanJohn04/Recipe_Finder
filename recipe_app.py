from flask import Flask, jsonify
import funcs

#FLask setup
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


#Flask Routes

@app.route("/")
def home():
    print("Server recieved request for index route")
    return(
        f"Welome to Recipe Finder!<br/>"
        '<br/>'
        '<br/>'
        f"Work in progress...<br/>"
        f"TESTTESTTTESTTESTTESTTESTTEST"

        f"Available Routes:<br/>"
        '<br/>'
        f"--Route: /api/v1.0/recipe_search/<search_term>"
        f"--Description: NO FUNCTIONILTY...WORK IN PROGRESS"
    )


@app.route("/api/v1.0/recipe_search/<search_term>")
def scrape_recipes(search_term):
    # Implement code to return a list of top recipes from the search
    return "Work in progress..."
    # add an input an the end that allows the user to select a recipe
    # from the returned list

    # possibly redirect to app.route("/api/v1.0/recipe_info/<recipe_name>") after entering recipe selection
    # which returns ingredient list and cooking instructions


@app.route("/api/v1.0/recipe_info/<recipe_name>")
def display_recipe(recipe_name):
    # implement code to return the ingredient list and
    # cooking instructions to the screen

    return "Work in progress..."


if __name__ == "__main__":
    app.run(debug=True)
