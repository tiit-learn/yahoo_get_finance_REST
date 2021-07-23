import flask
import json
import os
import requests
import time

from flask_sqlalchemy import SQLAlchemy

DATABASE_NAME = 'database.db'

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./%s' % DATABASE_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Symbol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), unique=True, nullable=False)
    data = db.Column(db.String(120), unique=True, nullable=False)


if not os.path.exists(DATABASE_NAME):
    db.create_all()


def get_json(symbol_name):
    """
    Function return json data of company finance for max time
    """
    url = 'https://query1.finance.yahoo.com/v7/finance/download/%s?period1=0&period2=%s&interval=1d&events=history&includeAdjustedClose=true' % (symbol_name,
                                                                                                                                                 int(time.time()))
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4569.0 Safari/537.36',
        'Host': 'query1.finance.yahoo.com'
    }

    get_csv = requests.get(url, headers=headers)

    if get_csv.status_code == 200:

        rows = get_csv.text.split('\n')

        data_dict = {}
        titles = rows[0].split(',')

        for row in rows[1:]:
            cells = row.split(',')
            data_dict[cells[0]] = {
                titles[1]: cells[1],
                titles[2]: cells[2],
                titles[3]: cells[3],
                titles[4]: cells[4],
                titles[5]: cells[5],
                titles[6]: cells[6],
            }

        json_data = json.dumps(data_dict)

        if get_data_from_db(symbol_name):
            update_in_db(symbol_name, json_data)
        else:
            save_to_db(symbol_name, json_data)
        return json_data
    return json.dumps({})


def save_to_db(symbol, data):
    """
    Function for saving symbol data into DB
    """
    symbol = Symbol(symbol=symbol, data=data)
    db.session.add(symbol)
    db.session.commit()


def update_in_db(symbol_name, json_data):
    """
    Function for updating symbol data into DB
    """
    symbol = Symbol.query.filter_by(symbol=symbol_name).first()
    symbol.data = json_data
    db.session.commit()


def get_data_from_db(symbol_name):
    """
    Function checking for existing symbol data into DB
    """
    symbol = Symbol.query.filter_by(symbol=symbol_name).first()
    if symbol:
        return True
    return False


@ app.route('/')
def index():
    return flask.redirect('/api/1.0/get')


@ app.route('/api/1.0/get', methods=['GET'])
def home():
    default_symbols = []
    return flask.render_template('index.html', symbols=default_symbols)


@ app.route('/api/1.0/get/<string:symbol_name>', methods=['GET'])
def get_data(symbol_name):
    return json.loads(get_json(symbol_name))


@ app.route('/api/1.0/testing', methods=['GET'])
def get_get_test():
    test_symbols()
    return 'Testing'


def test_symbols():
    """
    Testing data function
    """
    symbols_test = {
        'PD': '2019-04-11',
        'ZUO': '2018-04-12',
        'PINS': '2019-04-18',
        'ZM': '2019-04-18',
        'DOCU': '2018-04-27',
        'CLDR': '2017-04-28',
        'RUN': '2015-08-05'
    }
    for symbol in symbols_test:
        data = json.loads(get_json(symbol))
        if data.get(symbols_test[symbol]):
            print(symbol, 'pass')
        else:
            print(symbol, 'fail')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
