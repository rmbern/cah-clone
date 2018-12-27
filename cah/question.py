from flask import Blueprint, session, request, render_template
from cah.db import get_db
import random

bp = Blueprint('question', __name__)

@bp.route('/question-phase')
def ask_question():
  db = get_db()

  answer_records = db.execute(
    'SELECT answer FROM players'
  )
  # Select a new question if everyone has answered
  if not None in map(lambda x: x['answer'], answer_records):

    question_records = db.execute(
      'SELECT question FROM questions'
    ).fetchall()

    r = random.Random()
    index = r.randrange(0,len(question_records))
    new_question = question_records[index]['question']

    db.execute(
      'UPDATE current_question'
      ' SET question = ?', (new_question,)
    )
  
  # Always send the current question for asking!!
  question = db.execute(
    'SELECT question FROM current_question'
  ).fetchone()['question']

  return render_template('round.html',question=question)
