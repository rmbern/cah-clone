from flask import \
  Blueprint, request, current_app, redirect, render_template, session
from cah.db import get_db
import sys
import re
import sqlite3

bp = Blueprint('login', __name__)

@bp.route('/')
def initialize():

  # We want to start each new access to the web server
  # With a 'clean slate'

  # For right now, a player accessing the default route after
  # logging in is UB. 
  return render_template('login.html', error=None)

@bp.route('/login', methods=['POST'])
def login():
  db = get_db()
  
  # TODO: Messy elif chain, needs cleanup.

  # TODO: Change render_template calls to flashes

  # only allow spaces, alphanumeric characters, and underscore
  if not re.fullmatch("( |\w)+", request.form['username']): 
    current_app.logger.warning('Login attempted with non-alphanumeric chars!')
    return render_template('login.html',
                            error="Please try again using A-Z, spaces, and 0-9")

  #input is syntactically valid 
  else:
    session['username'] = request.form['username']
    # TODO: Handle when playername is already taken!!
    try:
      db.execute(
        'INSERT INTO players'
        ' VALUES (?,0,0,0,NULL)', (session['username'],)
      )
      db.commit()
    except sqlite3.IntegrityError: # Name already entered.
      return render_template('login.html',
                              error='Name already in use, please try again!')

  all_player_names = [] # list of strings
  for record in db.execute('SELECT name FROM players').fetchall():
    all_player_names.append(record['name'])
  return render_template('lobby.html',
                          username=session['username'],
                          players=all_player_names)
