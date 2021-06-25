import flask
import json
import os
import requests


app = flask.Flask(__name__)


def get_json(symbol_name):
    """
    Function return json data of company finance for max time
    """
    get_csv = requests.get(
        'https://query1.finance.yahoo.com/v7/finance/download/%s?period1=1277769600&period2=1624492800&interval=1d&events=history&includeAdjustedClose=true' % symbol_name)
    os.makedirs('output', exist_ok=True)
    file_path = os.path.join('output', symbol_name + '.csv')
    if get_csv.status_code == 200:
        with open(file_path, 'wb') as csv_file:
            csv_file.write(get_csv.content)

        rows = get_csv.text.split('\n')

        csv_dict = {}
        titles = rows[0].split(',')

        for row in rows[1:]:
            cells = row.split(',')
            csv_dict[cells[0]] = {
                titles[1]: cells[1],
                titles[2]: cells[2],
                titles[3]: cells[3],
                titles[4]: cells[4],
                titles[5]: cells[5],
                titles[6]: cells[6],
            }
        return json.dumps(csv_dict, indent=4) + '\n'
    return json.dumps({}, indent=4) + '\n'


@ app.route('/')
def index():
    return flask.redirect('/api/1.0/get')


@ app.route('/api/1.0/get', methods=['GET'])
def home():
    default_symbols = ['PD', 'ZUO', 'PINS',
                       'ZM', 'PVTL', 'DOCU', 'CLDR', 'RUN']
    return flask.render_template('index.html', symbols=default_symbols)


@ app.route('/api/1.0/get/<string:symbol_name>', methods=['GET'])
def get_data(symbol_name):
    return json.loads(get_json(symbol_name))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
