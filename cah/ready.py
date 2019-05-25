from flask import \
  Blueprint, session, redirect, render_template, send_from_directory,\
  current_app
from cah.db import get_db
from .answer import update_judge

def all_ready():
  db = get_db()
  records = db.execute('SELECT ready FROM players').fetchall()
  return 0 in [ x['ready'] for x in records ]

bp = Blueprint('ready', __name__)
@bp.route('/submit-ready', methods=['POST'])
def ready():
  if 'username' in session:
    player_name = session['username']
    db = get_db()

    db.execute(
      'UPDATE players'
      ' SET ready = 1'
      ' WHERE name = ?',(player_name,))
    
    # Ideally, we would want to select a judge at initialization to
    # keep all of our "one and done" code in a single spot. However,
    # This is the first point at which the database is aware of all 
    # the players in the game.
    if all_ready():
      update_judge()

    db.commit()

    return render_template('wait-for-ready.html', player=player_name)
  else:
    current_app.logger.warning("Player with no username in session"
                               "sent a ready signal!")

    return "You don't exist!"

@bp.route('/ask-if-ready', methods=['GET'])
def redirect_when_all_ready():
  if all_ready():
    return "NOT READY"
  else: # all are ready
    return "READY"
