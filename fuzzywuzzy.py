import json, sqlite3
from flask import Flask, request, url_for, g

import backend.search

# configuration
DATABASE = 'static/fuzzywuzzy.db'
DEBUG = True

# create eur little application :)
app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)

class NoteMatch:
    def __init__(self, text):
        self.text = text
        self.lowerText = text.lower()
        self.matchRanges = []

    def _addMatchRange(self, start, end):
        self.matchRanges.append((start, end))

    def findMatches(self, query):
        for matchWord, index in backend.search.search(query, self.text):
            self._addMatchRange(index, index + len(matchWord))

        return len(self.matchRanges) > 0

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def noteMatchesToJson(matches):
    return [{
        'text': i.text,
        'matchRanges': [
            {
                'start': m[0],
                'end':   m[1],
            } for m in i.matchRanges
        ],
    } for i in matches ]

def getAllNotes():
    result = g.db.execute('select text from notes')
    return [NoteMatch(row[0]) for row in result.fetchall()]

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/add/', methods=['POST'])
def add_entry():
    input_text = request.get_data()
    print("DATA", input_text)
    g.db.execute('insert into notes (text) values (?)',
        [input_text])
    g.db.commit()
    #flash('New entry was successfully posted')
    #return redirect(url_for('root'))
    return "good"

@app.route('/search/<string:query>/', methods=['GET'])
def search(query):
    notes = getAllNotes()

    matches = [i for i in notes if i.findMatches(query)]
    return json.dumps({'matches': noteMatchesToJson(matches)})

if __name__ == "__main__":
    app.run(debug=True)

