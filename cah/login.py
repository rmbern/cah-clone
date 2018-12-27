from flask import \
  Blueprint, request, current_app, redirect, render_template, session
from cah.db import get_db

bp = Blueprint('login', __name__)

@bp.route('/')
def initialize():

  # We want to start each new access to the web server
  # With a 'clean slate'

  # For right now, a player accessing the default route after
  # logging in is UB. 
  session.clear()
  return redirect('/login')

@bp.route('/login', methods=['GET','POST'])
def login():
  db = get_db()
  
  # Modify the database if request is a POST and
  # user has not aleady logged in.
  if request.method == 'POST':
    if 'username' in session:
      # TODO: Use flash correctly!!
      flash('Error! Login attempted when session already exists!')
      print('Error! Login attempted when session already exists!')
    else:
      player_name = request.form['username']
      session['username'] = request.form['username']
      # TODO: Handle when playername is already taken!!
      db.execute(
        'INSERT INTO players'
        ' VALUES (?,0,0,0,NULL)', (player_name,)
      )
      db.commit()

  # From here on out should run for both GET and POST
  # TODO: error handling
  all_player_names = [] # list of strings
  for record in db.execute('SELECT name FROM players').fetchall():
    all_player_names.append(record['name'])
  # already logged in
  if 'username' in session:
    player_name = session['username']
    return render_template('lobby.html',
                            username=player_name,
                            players=all_player_names)

  else: # not already logged in
    return render_template('login.html')
 
