from flask import Blueprint, session, request, render_template
from cah.db import get_db

import json

bp = Blueprint('answer', __name__)

@bp.route('/submit-answer', methods=['POST'])
def answer():
  # WARNING!!!!
  # AS THIS STANDS, USER CAN CHANGE THEIR ANSWER AFTER SUBMISSION
  # WITH A SECOND POST CALL.
  answer = request.form['answer']
  player_name = session['username']
  
  db = get_db()
  db.execute(
    'UPDATE players'
    ' SET answer = ?'
    ' WHERE name = ?',
    (answer, player_name,))
  db.commit()
  
  return render_template('answer-wait.html', answer=answer)

@bp.route('/get-answers', methods=['GET'])
def get_answers():
  # Construct and return a json object of all answers
  db = get_db()
  answer_records = db.execute(
                       'SELECT answer FROM players'
                       ' WHERE name <> ?',(session['username'],)
                      ).fetchall()
  
  # TODO: Can the map iterable be passed to json.dumps?
  answers = list(map(lambda x: x['answer'], answer_records)) 
  return json.dumps(answers)

@bp.route('/all-answered', methods=['GET'])
def all_answered():
  db = get_db()

  answer_records = db.execute(
                       'SELECT answer FROM players'
                   ).fetchall()
  
  if None not in map(lambda x: x['answer'], answer_records):
    return 'ALL ANSWERED'
  else:
    return 'NOT ALL ANSWERED'
