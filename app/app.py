from flask import Flask, request, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = '/tmp/users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        db.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'secret123')")
        db.commit()

@app.route('/')
def home():
    return '<h1>CorpDirectory</h1><form action="/search"><input name="q"><button>Search</button></form>'

@app.route('/search')
def search():
    query = request.args.get('q', '')
    db = get_db()
    # VULNERABLE: string concatenation SQL injection
    sql = "SELECT * FROM users WHERE username = '" + query + "'"
    cursor = db.execute(sql)
    results = cursor.fetchall()
    return f'<h2>Results:</h2><pre>{results}</pre>'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
