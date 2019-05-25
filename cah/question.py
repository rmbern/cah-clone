from flask import Blueprint, session, request, render_template
from cah.db import get_db

bp = Blueprint('question', __name__)

@bp.route('/question-phase', methods=['GET'])
def serve_question():
  db = get_db()

  question = db.execute(
    'SELECT question FROM current_question'
  ).fetchone()['question']

  player_record = db.execute(
    'SELECT judge FROM players'
    ' WHERE name = ?', (session['username'],)
  ).fetchone()

  if player_record['judge']:
    return render_template('judge-menu.html', question=question)
  else:
    return render_template('round.html', question=question)
