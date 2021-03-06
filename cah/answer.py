from flask import Blueprint, session, request, render_template, current_app
from cah.db import get_db

import json
import random

bp = Blueprint('answer', __name__)

# TODO: Due to the nature of how a round in CAH depends on both answers and
#       questions, it doesn't make much sense to separate question oriented
#       functionality and answer oriented functionality into two separate
#       files. As such, the functions in answer.py and question.py need to
#       be reorganized and renamed.

def all_answered():
  db = get_db()

  answer_records = db.execute(
    'SELECT answer FROM players'
  ).fetchall()

  return not None in [ x['answer'] for x in answer_records ]

def update_answer(answer):
  db = get_db()

  # WARNING!!!!
  # AS THIS STANDS, USER CAN CHANGE THEIR ANSWER AFTER SUBMISSION
  # WITH A SECOND POST CALL.
  player_name = session['username']
  
  db = get_db()
  db.execute(
    'UPDATE players'
    ' SET answer = ?'
    ' WHERE name = ?',
    (answer, player_name,))

@bp.route('/submit-answer', methods=['POST'])
def submit_answer():
  with current_app.app_context():
    db = get_db()
    answer = request.form['answer']
    update_answer(answer)
    db.commit()

  return render_template('answer-wait.html', answer=answer)

@bp.route('/get-answers', methods=['GET'])
def get_answers():
  with current_app.app_context():
    # Construct and return a json object of all answers
    # excluding nulls and the current player's answer.
    db = get_db()
    answer_records = db.execute(
                         'SELECT answer FROM players'
                         ' WHERE name != ?'
                         ' AND answer IS NOT NULL',(session['username'],)
                        ).fetchall()
    
    # TODO: Can the map iterable be passed to json.dumps?
    answers = [ x['answer'] for x in answer_records ]
    return json.dumps(answers)

@bp.route('/all-answered', methods=['GET'])
def send_all_answered():
  if all_answered():
    return 'ALL ANSWERED'
  else:
    return 'NOT ALL ANSWERED'
