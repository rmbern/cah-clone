from flask import Blueprint, session, request, render_template
from cah.db import get_db
import random

bp = Blueprint('question', __name__)

# TODO: Make this a POST
@bp.route('/question-phase')
def ask_question():
  db = get_db()

  answer_records = db.execute(
    'SELECT answer FROM players'
  ).fetchall()

  # Always send the current question for asking!!
  question = db.execute(
    'SELECT question FROM current_question'
  ).fetchone()['question']

  # Select a new question if everyone has answered.
  if not None in map(lambda x: x['answer'], answer_records) \
  or question == "NO QUESTION": # Or no question has been selected.
    # TODO: Only query one question from db
    question_records = db.execute(
      'SELECT question FROM questions'
    ).fetchall()

    r = random.Random()
    q_index = r.randrange(0,len(question_records))
    new_question = question_records[q_index]['question']

    db.execute(
      'UPDATE current_question'
      ' SET question = ?', (new_question,)
    )

    # Set a judge
    judge_records = db.execute(
      'SELECT name from players'
    ).fetchall()
    j_index = r.randrange(0,len(judge_records))
    new_judge = judge_records[j_index]['name']

    db.execute(
      'UPDATE players'
      ' SET judge = 0'
    )

    db.execute(
      'UPDATE players'
      ' SET judge = 1'
      ' WHERE name = ?',(new_judge,)
    )
    db.commit()
  
  player_record = db.execute('SELECT judge FROM players'
                             ' WHERE name = ?', 
                             (session['username'],)).fetchone()

  if player_record['judge'] == 0: # Not judge
    return render_template('round.html',question=question)
  else: # Is judge
    return render_template('judge-menu.html',question=question)
