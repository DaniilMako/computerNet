from flask import Flask, render_template, request, make_response, jsonify
from steamSpecialParser import start

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders index.html page
    :return:
    """
    return render_template('index.html')


@app.route('/parse', methods=['GET'])
def parsing():
    """Handle the 'parse' route for form submission.

    Extracts the link from the form data and invokes the 'parse' function to obtain the data.
    Converts the data to a CSV string format and generates a response with the CSV file for download.

    :return: Response: Flask response object containing the CSV data as an attachment.
    """
    link = request.args.get("url")
    data = start(link)
    print(data)
    response = jsonify(data)
    print(response)
    return response, 200, {"Content-Type": "application/json"}


# curl -H "Content-Type: application/json" "http://127.0.0.1:5000/parse?url=https://store.steampowered.com/specials"

if __name__ == '__main__':
    app.run()
