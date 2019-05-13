from flask import jsonify, request
from flask_app import app
from app import util, Account
from requests.exceptions import ConnectionError

UNAUTHORIZED = {"error": "unauthorized", "status_code": 401}
NOT_FOUND = {"error": "not found", "status_code": 404}
APP_ERROR = {"error": "application error", "status_code": 500}
BAD_REQUEST = {"error": "bad request", "status_code": 400}

@app.errorhandler(404)
def error404(e):
    return jsonify(NOT_FOUND), 404

@app.errorhandler(500)
def error500(e):
    return jsonify(APP_ERROR), 500

@app.route('/')
def root():
    return jsonify({"name": "API Trader"})

@app.route('/api/price/<ticker>', methods=['GET'])
def price(ticker):
    try:
        price = util.get_price(ticker)
    except ConnectionError:
        return jsonify(NOT_FOUND), 404
    return jsonify({"ticker": ticker, "price": price})

@app.route('/api/get_api_key', methods=['POST'])
def get_api_key():
    username = request.json['username']
    password = util.hash_pass(request.json['password'])
    account = Account.login(username, password)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    return jsonify({"api_key": account.api_key, "username": account.username})


@app.route('/api/<api_key>/balance', methods=['GET'])
def balance(api_key):
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    return jsonify({"username": account.username, "balance": account.balance})

@app.route('/api/<api_key>/positions', methods=['GET'])
def positions(api_key):
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    positions = account.get_positions()
    json_list = [position.json() for position in positions]
    return jsonify({"username": account.username, "positions": json_list})

@app.route('/api/<api_key>/position_sum', methods=['GET'])
def positions_sum(api_key):
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    positions = account.get_positions()
    tot_sum = 0
    for position in positions:
        tot_sum += util.get_price(position.ticker) * position.shares
    return jsonify({"account_sum": tot_sum})

@app.route('/api/<api_key>/positions/<ticker>', methods=['GET'])
def position_for(api_key, ticker):
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    position = account.get_position_for(ticker)
    return jsonify({"username": account.username, "positions": position.json()})

@app.route('/api/<api_key>/trades', methods=['GET'])
def trades(api_key):
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    trades = account.get_trades_orderby()
    json_list = [trade.json() for trade in trades]
    return jsonify({"username": account.username, "trades": json_list})

@app.route('/api/<api_key>/trades_for/<ticker>', methods=['GET'])
def trades_for(api_key, ticker):
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    trades = account.get_trades_for(ticker)
    json_list = [trade.json() for trade in trades]
    return jsonify({"username": account.username, "trades": json_list})

@app.route('/api/<api_key>/deposit', methods=['PUT'])
def deposit(api_key):
    if not request.json or 'amount' not in request.json:
        return jsonify(BAD_REQUEST), 400
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    amount = request.json['amount']
    if amount < 0:
        return jsonify(BAD_REQUEST), 400
    account.deposit(amount)
    account.save()
    return jsonify({"username": account.username, "balance": account.balance})

@app.route('/api/<api_key>/withdraw', methods=['PUT'])
def withdraw(api_key):
    if not request.json or 'amount' not in request.json:
        return jsonify(BAD_REQUEST), 400
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    amount = request.json['amount']
    if amount < 0:
        return jsonify(BAD_REQUEST), 400
    account.withdraw(amount)
    account.save()
    return jsonify({"username": account.username, "balance": account.balance})

@app.route('/api/<api_key>/buy', methods=['POST'])
def buy(api_key):
    if not request.json or 'amount' not in request.json:
        return jsonify(BAD_REQUEST), 400
    if 'ticker' not in request.json:
        return jsonify(BAD_REQUEST), 400
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    amount = request.json['amount']
    if not isinstance(amount, int or float) or amount < 0:
        return jsonify(BAD_REQUEST), 400
    ticker = request.json['ticker']
    if not isinstance(ticker, str) or len(ticker) > 4:
        return jsonify(BAD_REQUEST), 400
    account.buy(ticker, amount)
    account.save()
    position = account.get_position_for(ticker)
    return jsonify({"username": account.username, "balance": account.balance, "position": position.json()})

@app.route('/api/<api_key>/sell', methods=['POST'])
def sell(api_key):
    if not request.json or 'amount' not in request.json:
        return jsonify(BAD_REQUEST), 400
    if 'ticker' not in request.json:
        return jsonify(BAD_REQUEST), 400
    account = Account.api_authenticate(api_key)
    if not account:
        return jsonify(UNAUTHORIZED), 401
    amount = request.json['amount']
    if not isinstance(amount, int or float) or amount < 0:
        return jsonify(BAD_REQUEST), 400
    ticker = request.json['ticker']
    if not isinstance(ticker, str) or len(ticker) > 4:
        return jsonify(BAD_REQUEST), 400
    account.sell(ticker, amount)
    account.save()
    position = account.get_position_for(ticker)
    return jsonify({"username": account.username, "balance": account.balance, "position": position.json()})
