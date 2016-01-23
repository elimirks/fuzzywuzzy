from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

class NoteMatch:
    def __init__(self, text):
        self.text = text
        self.lowerText = text.lower()
        self.matchRanges = []

    def _addMatchRange(self, start, end):
        self.matchRanges.append((start, end))

    def findMatches(self, query):
        beginning = 0

        while True:
            index = self.lowerText.find(query, beginning)
            if index == -1:
                break
            beginning = index + 1

            self._addMatchRange(index, index + len(query) - 1)

        return len(self.matchRanges) > 0

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

@app.route('/search/<string:query>/', methods=['GET'])
def search(query):
    notes = [
        NoteMatch('There there.'),
        NoteMatch('Where?'),
    ]

    matches = [i for i in notes if i.findMatches(query)]
    return {'matches': noteMatchesToJson(matches)}

if __name__ == "__main__":
    app.run(debug=True)

