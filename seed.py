import os
import sqlite3
import app
import time

DBFILENAME = os.path.join(os.path.dirname(__file__), "app", 'termtrader.db')

def seed(DBFILENAME):
    with sqlite3.connect(DBFILENAME) as conn:
        SQL = "DELETE FROM {};"
        cur = conn.cursor()
        cur.execute(SQL.format('accounts'))
        cur.execute(SQL.format('positions'))
        cur.execute(SQL.format('trades'))
    
    account = app.Account()
    account.username = "james"
    account.balance = 1000000.0
    account.set_password(app.util.hash_pass("password"))
    # account.api_key = '0123456789abcde'
    account.save()

    account = app.Account()
    account.username = "carter"
    account.balance = 900.0
    account.set_password(app.util.hash_pass("password"))
    account.save()

    trade1 = app.Trade()
    trade1.time = time.time() - 24 * 60 * 60
    trade1.ticker = 'tsla'
    trade1.account_pk = 1
    trade1.volume = 10
    trade1.price = app.util.get_price('tsla') - 20.0
    trade1.save()

    trade2 = app.Trade()
    trade2.time = time.time()
    trade2.ticker = 'tsla'
    trade2.account_pk = 1
    trade2.volume = -5
    trade2.price = app.util.get_price('tsla') + 20.0
    trade2.save()

    position1 = app.Position()
    position1.account_pk = 1
    position1.ticker = 'tsla'
    position1.shares = '5'
    position1.save()

    trade3 = app.Trade()
    trade3.time = time.time()
    trade3.ticker = 'gs'
    trade3.account_pk = 1
    trade3.volume = 20
    trade3.price = app.util.get_price('gs') + 20.0
    trade3.save()

    position2 = app.Position()
    position2.account_pk = 1
    position2.ticker = 'gs'
    position2.shares = '20'
    position2.save()

    trade4 = app.Trade()
    trade4.time = time.time()
    trade4.ticker = 'ttd'
    trade4.account_pk = 1
    trade4.volume = 6
    trade4.price = app.util.get_price('ttd') + 20.0
    trade4.save()

    position3 = app.Position()
    position3.account_pk = 1
    position3.ticker = 'ttd'
    position3.shares = '6'
    position3.save()


if __name__ == "__main__":
    seed(DBFILENAME)
