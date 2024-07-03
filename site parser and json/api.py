# для корректной работы: http://127.0.0.1:5000/parse?url=https://www.cifrus.ru/

from flask import Flask, request, jsonify
# from steamSpecialParser import start
from parserK import parser
import csv
import json


def load_csv(filename):
    with open(filename, 'r', encoding='utf-16') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows


app = Flask(__name__)


@app.route('/parse', methods=['GET'])
def parse_url():
    url = request.args.get('url')
    if url:
        try:
            csv_filename = parser(url)
            parsed_data = load_csv(csv_filename)
            print()
            print(parsed_data)
            print()
            with open('data.json', 'w') as json_file:
                json.dump(jsonify({"url": url, "parsed_data": parsed_data}).json, json_file, indent=4)
            return jsonify({"url": url, "parsed_data": parsed_data})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Missing URL parameter"}), 400


if __name__ == '__main__':
    app.run(debug=True)
