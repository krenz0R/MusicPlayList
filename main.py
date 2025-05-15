from flask import Flask, render_template, g, request, redirect
import os
import sqlite3

app = Flask(__name__)
DB = 'visits.db' 

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
        g.db.execute('CREATE TABLE IF NOT EXISTS counter(page TEXT PRIMARY KEY, cnt INTEGER)')
        g.db.execute('CREATE TABLE IF NOT EXISTS comments(name TEXT, text TEXT)')
        g.db.execute('CREATE TABLE IF NOT EXISTS poll(option TEXT PRIMARY KEY, votes INTEGER)')
    return g.db
    return g.db

def increment_counter(page):
    db = get_db()
    cur = db.execute('SELECT cnt FROM counter WHERE page=?', (page,))
    row = cur.fetchone()
    if row:
        db.execute('UPDATE counter SET cnt=cnt+1 WHERE page=?', (page,))
    else:
        db.execute('INSERT INTO counter(page,cnt) VALUES(?,1)', (page,))
    db.commit()
    cnt = db.execute('SELECT cnt FROM counter WHERE page=?', (page,)).fetchone()[0]
    return cnt

@app.route('/')
def index():
    music_folder = 'static/music'
    tracks = os.listdir(music_folder)
    cnt = increment_counter('index')
    db = get_db()
    comments = db.execute('SELECT name, text FROM comments').fetchall()
    comments = [{'name': row[0], 'text': row[1]} for row in comments]
    return render_template('index.html', visits=cnt, tracks=tracks, comments=comments)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    db = get_db()
    options = ['Rock', 'Jazz', 'Pop', 'Classical', 'Hip-Hop']

    # гарантируем, что в таблице есть все опции
    for opt in options:
        db.execute('INSERT OR IGNORE INTO poll(option, votes) VALUES (?, 0)', (opt,))
    db.commit()

    if request.method == 'POST':
        choice = request.form['option']
        db.execute('UPDATE poll SET votes = votes + 1 WHERE option = ?', (choice,))
        db.commit()

    # собираем результаты в том же порядке, что и options
    results = []
    for opt in options:
        cnt = db.execute('SELECT votes FROM poll WHERE option = ?', (opt,)).fetchone()[0]
        results.append((opt, cnt))

    return render_template('vote.html', results=results)

@app.route('/comment', methods=['POST'])
def comment():
    name = request.form['name']
    text = request.form['text']
    db = get_db()
    db.execute('INSERT INTO comments(name, text) VALUES (?, ?)', (name, text))
    db.commit()
    return redirect('/')

def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()