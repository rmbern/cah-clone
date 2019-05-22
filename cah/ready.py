from flask import \
  Blueprint, session, redirect, render_template, send_from_directory, current_app
from cah.db import get_db

bp = Blueprint('ready', __name__)
@bp.route('/submit-ready', methods=['POST'])
def ready():
  if 'username' in session:
    player_name = session['username']
  else:
    # TODO: Use flash correctly!!
    flash('Error! Ready attempted with no session!')
    print('Error! Ready attempted with no session!')
  db = get_db()
  db.execute(
    'UPDATE players'
    ' SET ready = 1'
    ' WHERE name = ?',(player_name,))
  db.commit()

  return send_from_directory('static', 'wait-for-ready.html')

@bp.route('/ask-if-ready', methods=['GET'])
def redirect_when_all_ready():
  db = get_db()
  records = db.execute('SELECT ready FROM players').fetchall()
  if 0 in map(lambda x: x['ready'], records): # someone isn't ready
    return "NOT READY"
  else: # all are ready
    return "READY"
