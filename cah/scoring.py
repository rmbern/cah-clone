from flask import Blueprint, render_template
from cah.db import get_db

bp = Blueprint('scoring', __name__)

@bp.route('/scoreboard', methods=['GET'])
def scoreboard():
  db = get_db()
  
  score_records = db.execute(
                     'SELECT name, score FROM players'
                  ).fetchall()

  winning_answer = db.execute(
                      'SELECT answer FROM players'
                      ' WHERE judge = 1'
                  ).fetchone()

  return render_template('scoreboard.html',
                         records=score_records,
                         winning_answer=winning_answer[0])
