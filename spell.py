# Flask Libraries
from flask import Flask, render_template, url_for, request, redirect
import json
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def get_name():
    if request.method == "POST":
        name = request.form['name']
        return redirect(url_for('show_elements',
                                name=name))
    else:
        return render_template("index.html")


@app.route('/show', methods=['GET'])
def show_elements():
    with open('periodic_table.json') as f:
        data = json.load(f)

    name = str(request.args.get('name').lower()).replace(" ", "")

    list_of_elements = []

    # Find all the elements which are substrings of the given name
    for i in range(0, len(data["elements"])):

        symbol = data["elements"][i]["symbol"]

        r = name.find(symbol.lower())

        if r != -1:
            list_of_elements.append(
                [symbol, data["elements"][i]["name"], r,
                 data["elements"][i]["number"]])

    # Sort in accordance with the symbol
    def takefirst(element):
        return len(element[0])

    # String lengths - greatest to smallest
    list_of_elements.sort(key=takefirst, reverse=True)

    # To store the actual elements
    checklist = []

    def check(name):
        if name == "":
            return True

        for i in range(0, len(list_of_elements)):
            # Find the elements which the name starts with
            if name.startswith(list_of_elements[i][0].lower()):
                # Slice the string from the end of the already done sub-string
                c = check(name[len(list_of_elements[i][0]):len(name)])

                if c is True:
                    checklist.insert(0, list_of_elements[i])
                    return True

        return False

    # Sort in accordance with the index(r) stored
    def index(element):
        return element[2]

    if check(name) is False:

        print("Sorry! We couldn't find a right match :(. These are the" +
              " elements we came across.")

        if(len(list_of_elements) != 0):
            # Prints elements on par with the given input
            list_of_elements.sort(key=index)
            print(list_of_elements)

    else:
        print(checklist)

    return render_template("result.html", name=name, checklist=checklist,
                           list_of_elements=list_of_elements)


if __name__ == "__main__":
    app.run(debug=True)
