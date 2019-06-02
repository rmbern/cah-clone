from flask import \
  Blueprint, session, redirect, render_template, send_from_directory,\
  current_app
from cah.db import get_db
import random

def all_ready():
  db = get_db()
  records = db.execute('SELECT ready FROM players').fetchall()
  return not 0 in [ x['ready'] for x in records ]

def update_judge():
  db = get_db()
  
  # We are going to select a judge randomly,
  # excluding the player who is currently the
  # judge.
  judge_records = db.execute(
    'SELECT name FROM players'
    ' WHERE judge != 1'
  ).fetchall()
  r = random.Random()
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


def update_question():
  db = get_db()
  
  # First, delete the question we just used.
  # TODO: We have nothing handling the exhaustion
  #       of questions. This will most likely
  #       result in a crash.

  # There may be desirable scenarios where we don't
  # delete whatever we find in current_question,
  # notably during the first round where a bogus init
  # value is placed into the database.
  current_question = db.execute(
    'SELECT question FROM current_question'
  ).fetchone()['question']
  
  db.execute(
    'DELETE FROM questions'
    ' WHERE question = ?', (current_question,)
  )

  question_records = db.execute(
    'SELECT question FROM questions'
  ).fetchall()

  r = random.Random()
  q_index = r.randrange(0,len(question_records))
  new_question = question_records[q_index]['question']
  
  db.execute(
    'UPDATE current_question'
    ' SET question = ?', (new_question,))


bp = Blueprint('ready', __name__)
@bp.route('/submit-ready', methods=['POST'])
def ready():
  if 'username' in session:
    player_name = session['username']
    db = get_db()

    db.execute(
      'UPDATE players'
      ' SET ready = 1,'
      '     answer = NULL'
      ' WHERE name = ?',(player_name,))
    
    # Ideally, we would want to select a judge at initialization to
    # keep all of our "one and done" code in a single spot. However,
    # This is the first point at which the database is aware of all 
    # the players in the game.
    if all_ready():
      update_judge()
      update_question()
    db.commit()

    return render_template('wait-for-ready.html', player=player_name)
  else:
    current_app.logger.warning("Player with no username in session "
                               "sent a ready signal!")

    return "You don't exist!"

@bp.route('/ask-if-ready', methods=['GET'])
def redirect_when_all_ready(): # TODO: No redirect...rename
  if all_ready():
    return "READY"
  else:
    return "NOT READY"
