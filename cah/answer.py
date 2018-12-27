from flask import Blueprint, session, request, render_template
from cah.db import get_db

bp = Blueprint('answer', __name__)

@bp.route('/submit-answer', methods=['POST'])
def answer():
  # WARNING!!!!
  # AS THIS STANDS, USER CAN CHANGE THEIR ANSWER AFTER SUBMISSION
  # WITH A SECOND POST METHOD.
  answer = request.form['answer']
  player_name = session['username']
  
  db = get_db()
  db.execute(
    'UPDATE players'
    ' SET answer = ?'
    ' WHERE name = ?',
    (answer, player_name,))
  
  return render_template('answer-wait.html', answer=answer)
